#!/bin/bash
#!/usr/bin/python

########### READ ME #################################################################################################################
# This script does the following: 
# Checks for registration file in Web Auth S3 bucket. Copies to MWSS Web S3 bucket 
# Downloads the current server.conf from MWSSWEB S3 bucket, updates it and re-uploads to S3 bucket as part new setup for AutoScaling.
# Final part restarts each SPS node in AutoScaling cluster with updated server.conf 
#####################################################################################################################################
# Please note SM team introduces spaces in the naming format for the XML reg file, so observe the naming below.

############# SCRIPT VARIABLES ############################
FILE_NAME=`date | awk '{print $3" "$2" "$6 }'`
FILE_NAME="nonprod $FILE_NAME.xml"
S3_ENV_NAME="nonprod" #change to either sbx or nonprod or prod
TEXT="No file, better luck next time"
CONF1="server.conf"
CONF_DATE="$CONF1`date | awk '{print "_"$3"_"$2"_"$6"_"$4}'`"
REG="new_registration.xml"
ELB="vip-aws-internal-npusw-sps"
SNS_TOPIC="arn:aws:sns:us-west-2:593461941206:mwss-web-sps"
SUBJECT="Failed SPS restart during registraion.Check node"
COMMENT="Restart SPS Node"
DOC_NAME="AWS-RunShellScript"
##########################################################

#Download registration file from the Web Auth S3 bucket to WORKER instance 
./bucket-ops.py -m download -c input_files/web-auth-info.json -d registrations/"$FILE_NAME" -l s3_files/xmldrop/"$FILE_NAME" 2>logs/bucket_error.log
./bucket-ops.py -m download -c input_files/web-auth-info.json -d registrations/"$FILE_NAME" -l s3_files/xmlsave/"$FILE_NAME" 2>logs/bucket_error.log

#Update owner and group for file to "ec2-user"
chown ec2-user:ec2-user /local/mnt/scripts/autoregistration/s3_files/xmldrop/"$FILE_NAME"
chmod 755 /local/mnt/scripts/autoregistration/s3_files/xmldrop/"$FILE_NAME"
chown ec2-user:ec2-user /local/mnt/scripts/autoregistration/s3_files/xmlsave/"$FILE_NAME"
chmod 755 /local/mnt/scripts/autoregistration/s3_files/xmlsave/"$FILE_NAME"

if [ -f s3_files/xmldrop/"$FILE_NAME" ]
then

# Copy $FILE_NAME for upload to MWSS S3 bucket
cp ./s3_files/xmldrop/"$FILE_NAME" ./s3_files/xmldrop/"$REG" 

# Upload registration to MWSSWEB S3 Bucket 
./bucket-ops.py -m upload -c input_files/mwss-web-info.json -d sps-registrations/xmldrop/"$S3_ENV_NAME"/"$REG" -l s3_files/xmldrop/"$REG" 2>logs/bucket_error.log
./bucket-ops.py -m upload -c input_files/mwss-web-info.json -d sps-registrations/xmldrop/"$S3_ENV_NAME"/notify."$S3_ENV_NAME" -l s3_files/xmldrop/"$REG" 2>logs/bucket_error.log

# backup most recently downloaded server.conf 
mv ./s3_files/conf_latest/server.conf*:* ./s3_files/conf_latest/server.conf.previous

# Download current server.conf from S3 bucket 
./bucket-ops.py -m download -c input_files/mwss-web-info.json -d sps-registrations/conf-files/"$S3_ENV_NAME"/"$CONF1" -l s3_files/conf_latest/"$CONF_DATE" 2>logs/server_error.log

# Parse and updated server.conf
./url-reg.py -s s3_files/conf_latest/"$CONF_DATE" -r s3_files/xmldrop/"$REG" 2>logs/serverconf_error.log

# Add updated server.conf to POC folder in S3. 
./bucket-ops.py -m upload -c input_files/mwss-web-info.json -d sps-registrations/conf-files/"$S3_ENV_NAME"/server.conf -l s3_files/conf_latest/"$CONF_DATE" 2>logs/bucket_error.log

#####################################################################################################################################
# Restart each SPS node in AutoScaling cluster with updated "server.conf". Perform health-check before going to next node in Cluster# 
#####################################################################################################################################

SPS_NODES=`sudo aws ec2 describe-instances --region us-west-2 --filters "Name=tag:regenv,Values=sps-intnp" --query 'Reservations[].Instances[].[InstanceId]' --output text`

for node in $SPS_NODES ; do 
        sudo aws ssm send-command --region us-west-2 --instance-ids "$node" --document-name "$DOC_NAME" --comment "$COMMENT" --parameters '{"commands":["./restartSPS_new_reg.sh"],"workingDirectory":["/local/mnt/scripts/registration-restart"],"executionTimeout":["3600"]}' --output text 2>logs/failed_reg_restart.log
        sleep 60
        x=1
        while [ `sudo aws elb describe-instance-health  --region us-west-2 --load-balancer-name $ELB --output text | grep -ic OutOfService` -ge 1 ] && [ $x -le 100 ]; do
                logger "SPS Node $node currently OutOfService during new registration"
                sleep 20
                if [ `sudo aws elb describe-instance-health  --region us-west-2 --load-balancer-name $ELB --output text | grep -ic OutOfService` -ge 1 ]; then
                   x=$(( $x + 1 ))
                   if [ $x -eq 100 ]; then
                   logger "SPS Node $node has failed during new registration"
                   sudo aws ec2 describe-instances  --region us-west-2 --instance-ids "$node" --output text | grep TAGS > Fail.txt
                   sudo aws sns publish  --region us-west-2 --topic-arn $SNS_TOPIC --subject "$SUBJECT" --message file://Fail.txt
                   exit 1
                   else 
                    continue 
                  fi
                fi
            done
        done

############       
##CLEAN-UP##
############

#After download, delete file from the Web Auth S3 bucket
./bucket-ops.py -m delete -c input_files/web-auth-info.json -r registrations/"$FILE_NAME" 2>logs/bucket_error.log

# Delete REG and NOTIFY files from MWSS S3 bucket.

./bucket-ops.py -m delete -c input_files/mwss-web-info.json -r sps-registrations/xmldrop/"$S3_ENV_NAME"/"$REG" 2>logs/bucket_error.log
./bucket-ops.py -m delete -c input_files/mwss-web-info.json -r sps-registrations/xmldrop/"$S3_ENV_NAME"/notify."$S3_ENV_NAME" 2>logs/bucket_error.log

else
touch s3_files/xmldrop/noxmlfile.txt
chmod 777 s3_files/xmldrop/noxmlfile.txt
echo $TEXT >> s3_files/xmldrop/noxmlfile.txt
fi