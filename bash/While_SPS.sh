# Script that makes sure SPS Tomcat has stopped
#!/bin/bash

x=1
while [ `netstat -tulpn | grep -c '8100\|8200\|8300'` -ge 1 ] && [ $x -le 100 ]; do
        logger "Waiting for SPS to STOP"
        echo "Waiting for SPS to STOP"
          sleep 3
        if [ `netstat -tulpn | grep -c '8100\|8200\|8300'` -ge 1 ]; then
          x=$(( $x + 1 ))
          if [ $x -eq 100 ]; then
           logger "Loop detected. Processes have not shutdown after 5 mins. Aborting Script"
           echo "Loop detected. Processes have not shutdown after 5 mins. Aborting Script"
           exit 1
             else
              continue  #Starts loop again
          fi
        fi
        logger "SPS has been successfully stopped."
        echo "SPS has been successfully stopped."
       done
 exit 0
