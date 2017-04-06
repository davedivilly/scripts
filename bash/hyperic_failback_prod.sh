#!/bin/bash

#############################################################################################################################################
# Checks Hyperic DB health and fails back Hyperic App Server config to Master DB in the event of Primary DB restore                         #
# This script will run as a CRONJOB on Hyperic App Servers, using a file created in /etc/cron.d/hyperic_prod_failback                       #
#                                                                                                                                           #
# Date 22th July 2015                                                                                                                       #
# Copyright (c) Qualcomm Incorporated  All rights reserved. Before making any changes to this script please notify mwss.web.team            #
#############################################################################################################################################

############################
# Function to test the host
############################

host=`hostname`
if [ "webmon05" = $host ] || [ "webmon06" = $host ]
then

db_backend=dbpghypprd01

else

db_backend=dbpghypprd02

fi

#######################################
# Function to test Master/Slave Health
#######################################

health(){

i=1 # counter that repeats test condition 3 times, to confirm Master DB is restored and running.
while [ $i -le 3 ]
do

        sudo -u hyperic /usr/bin/psql -x -d HQ -h $db_backend -p 5411 -U appadmin -c "SELECT 1 as success" -o /usr2/hyperic/Hyperic_App_Health_$host.txt 2>/dev/null

        if [ 1 -eq `grep -c success /usr2/hyperic/Hyperic_App_Health_$host.txt` ]; then

                echo "Hyperic App failback **PROD**  has been triggered. If mail is received more than 3 times, check hq_server.conf and notify PostGres DBA." | mail -s "HypericApp failback triggered on `hostname`" mwss.web.team@qualcomm.com
                sleep 15

        else
                sudo -u hyperic rm -f /usr2/hyperic/Hyperic_App_Health_$host.txt
                exit 0

fi

        i=$((i+1))
done
}

#######################################
#Test Hyperic is running on this Server.
#######################################

if [ 0 -eq `ps U hyperic | grep -c server` ]; then
        exit 0
else
        health
fi

#################################################################################
# Stop Hyperic and CRONJOB swap Hyperic CONF files from Slave to Master         #
#                                                                               #
# Cron Entry: */5 * * * * root bash /usr2/hyperic/hyperic_failback_prod.sh      #
#################################################################################

sed -i 's/^/#/' /etc/cron.d/hyperic_prod_failback  # Stops Cronjob looping after failback #
sed -i 's/^#//' /etc/cron.d/hyperic_prod_failover  # Enables failover Cronjob #
sudo -u hyperic /local/mnt/hyperic-prod/server-5.8.4-EE/bin/hq-server.sh stop

sleep 30

sudo -u hyperic cp /local/mnt/hyperic-prod/server-5.8.4-EE/conf/hq-server.conf.DO.NOT.DELETE.PRIMARY /local/mnt/hyperic-prod/server-5.8.4-EE/conf/hq-server.conf
sudo -u hyperic /local/mnt/hyperic-prod/server-5.8.4-EE/bin/hq-server.sh start

echo "### Primary DB **PROD** (dbpghypprd01) is back online and Hyperic has failed-back to using it ###"  | mail -s "Hyperic Failback Finished"  mwss.web.team@qualcomm.com

exit 0
