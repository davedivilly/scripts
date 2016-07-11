#!/bin/bash

#############################################################################################################################################
# Checks Hyperic DB health and fails-over Hyperic App Server config to Slave DB in the event of Primary DB failure                          #
# This script will run as a CRONJOB on Hyperic App Servers, using a file created in /etc/cron.d/hyperic_cron                                #
#############################################################################################################################################

############################
# Function to test the host
############################

host=`hostname`
if [ "webmon05" = $host ] || [ "webmon06" = $host ]
then

db_backend=dbpghypprd05

else

db_backend=dbpghypprd06

fi

#######################################
# Function to test Master/Slave Health
#######################################

health(){

i=1 # counter that repeats test condition 3 times, to confirm DB is definitely unavailable.
while [ $i -le 3 ]
do

        sudo -u hyperic /usr/bin/psql -x -d HQ -h $db_backend -p 5437 -U appadmin -c "SELECT 1 as success" -o /usr2/hyperic/Hyperic_App_Health_$host.txt 2>/dev/null

        if [ 1 -eq `grep -c success /usr2/hyperic/Hyperic_App_Health_$host.txt` ]; then

                sudo -u hyperic rm -f /usr2/hyperic/Hyperic_App_Health_$host.txt
                exit 0

        else
                echo "Hyperic App failover has been triggered. If mail is received more than 3 times, check hq_server.conf and notify PostGres DBA." | mail -s "HypericApp failover triggered on `hostname`" ddivilly@qualcomm.com
                sleep 15
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
# Stop Hyperic and CRONJOB swap Hyperic CONF files from Master to Slave         #
#                                                                               #
# Cron Entry: */5 * * * * root bash /usr2/hyperic/hyperic_failover_nonprod.sh   #
#################################################################################

sed -i 's/^/#/' /etc/cron.d/hyperic_cron  # Stops Cronjob looping after failover #
sudo -u hyperic /local/mnt/hyperic-nonprod/server-5.8.4-EE/bin/hq-server.sh stop

sleep 30

sudo -u hyperic cp /local/mnt/hyperic-nonprod/server-5.8.4-EE/conf/hq-server.conf.DO.NOT.DELETE.SLAVE /local/mnt/hyperic-nonprod/server-5.8.4-EE/conf/hq-server.conf
sudo -u hyperic /local/mnt/hyperic-nonprod/server-5.8.4-EE/bin/hq-server.sh start

echo "SLAVE(dbpghypprd06)PostGres DB is now the PRIMARY DB after failover event. Consult with PostGres DBA on manual fail-back to dbpghypprd05(PRIMARY). ### Re-enable CRONJOB (/etc/cron.d/hyperic_cron) as part of manual fail-back ###"  | mail -s Hyperic_App_Failover_Event  ddivilly@qualcomm.com lbujas@qualcomm.com mwss.web.team@qualcomm.com

exit 0
