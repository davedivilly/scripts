# This script is used to rename index.html file to remove from the ELB and restart SPS Service and add it back to ELB 
# The ELB Name is passed in as a single argument to the script

###################################################################################
#                             Rename index.html                             #
###################################################################################

### Variables for ELB  #############
ELBFILEPATH="/local/mnt/secure-proxy/proxy-engine/examples/siteminderagent/forms/images"
ELBFILEName="index.html"
ELBFILENameBak="index.html.bak"
#ELBName="internal-vip-aws-internal-npusw-sps" # change based on SPS env

####### Update for the SPS Home Directory ###########
SPS_HOME="/local/mnt/secure-proxy"
SPS_CTL="proxy-engine/sps-ctl"
## SPS Config Files 
SPS_SERVER_CONF_S3="s3_files/server.conf"
SPS_SERVER_CONF_PATH=$SPS_HOME/proxy-engine/conf
SPS_SERVER_CONF_FILE=$SPS_SERVER_CONF_PATH/server.conf
BACKUP_FILES=$SPS_SERVER_CONF_FILE # Data to backup
DEST="/local/mnt/backup" # Backup location
## Create archive filename
DAY=$(date +"%m-%d-%y")
TIME=$(date +"%T")
HOSTNAME=$(hostname -s)
ARCHIVE_FILE="$HOSTNAME-$DAY-$TIME.tgz"
## Getting Instance ID of the EC2 Instance ##########
INSTANCEID=$(curl -fs http://169.254.169.254/latest/meta-data/instance-id/)
SUBJECT="Failed SPS Services Shutdown during registration.Check node"
SNS_TOPIC="arn:aws:sns:us-west-2:120216090522:mwss-web-sps"
ELBTimeout="300"
SPS_USER="ec2-user"
ENV="prod"

#############################
#  Take SPS node out of ELB #
#############################

mv $ELBFILEPATH/$ELBFILEName $ELBFILEPATH/$ELBFILENameBak
logger "index.html file renamed"
echo "index.html file renamed"
logger "Sleeping for" $ELBTimeout
echo "Sleeping for" $ELBTimeout

#Padding for ELBTimeout 
sleep $ELBTimeout
logger "After Sleep"
echo "Stopping SPS now ..."

# Updating the server.conf file from S3
# Print start status message.
echo "Backing up $BACKUP_FILES to $DEST/$ARCHIVE_FILE"
logger "Backing up $BACKUP_FILES to $DEST/$ARCHIVE_FILE"
date

# Backup the files using tar.
tar czf $DEST/$ARCHIVE_FILE $BACKUP_FILES

# Print end status message.
echo "Backup finished"
logger "Backup finished"
chown ec2-user:ec2-user /local/mnt/secure-proxy/httpd/logs/*
sudo -u $SPS_USER $SPS_HOME/$SPS_CTL stop
logger "sps stop command issued .."
echo "sps stop command issued .."

##########################################################
# make sure SPS has shutdown before start-up CMD is issued 
###########################################################

x=1
while [ `netstat -tulpn | grep -c '8100\|8200\|8300\|8000\|8500'` -ge 1 ] && [ $x -le 100 ]; do
        logger "Waiting for SPS to STOP"
        echo "Waiting for SPS to STOP"
          sleep 3
        if [ `netstat -tulpn | grep -c '8100\|8200\|8300\|8000\|8500'` -ge 1 ]; then
          x=$(( $x + 1 ))
          if [ $x -eq 100 ]; then
           logger "Loop detected. Processes have not shutdown after 5 mins. Aborting Script"
           echo "Loop detected. Processes have not shutdown after 5 mins. Aborting Script"
           sudo aws ec2 describe-instances --region us-west-2 --instance-ids "$INSTANCEID" --output text | grep TAGS > Fail.txt
           sudo aws sns publish  --region us-west-2 --topic-arn $SNS_TOPIC --subject "$SUBJECT" --message file://Fail.txt
           exit 1
             else
              continue
          fi
        fi
      logger "SPS has been successfully stopped."
      echo "SPS has been successfully stopped."
  done

################################
# Copy updated file to SPS Server
################################

echo "Copying updated server.conf file from S3 bucket folder"
logger "Copying updated server.conf file from S3 bucket folder"
./bucket-ops.py -m download -c /local/mnt/scripts/registration-restart/input_files/mwss-web-info.json -d sps-registrations/conf-files/$ENV/server.conf -l /local/mnt/secure-proxy/proxy-engine/conf/server.conf

chown ec2-user:ec2-user /local/mnt/secure-proxy/proxy-engine/conf/server.conf
chmod 755 /local/mnt/secure-proxy/proxy-engine/conf/server.conf

###################################
# Start SPS node and add back to ELB
###################################

logger "sps start file renamed"
echo "sps start file renamed"
sudo -u $SPS_USER $SPS_HOME/$SPS_CTL startssl
logger "sps start file renamed"
echo "sps start file renamed"
mv $ELBFILEPATH/$ELBFILENameBak $ELBFILEPATH/$ELBFILEName
logger "index.html.bak file renamed to index.html"
echo "index.html.bak file renamed to index.html"
sleep 10
exit 0