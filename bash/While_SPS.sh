# Script that makes sure SPS Tomcat has stopped
#!/bin/bash

while [ `sudo netstat -tulpn | grep -c '8100\|8200\|8300'` -ge 1 2>/dev/null ]; do
        logger "Waiting for SPS to STOP"
        echo "Waiting for SPS to STOP"
          sleep 3
        if [ `sudo netstat -tulpn | grep -c '8100\|8200\|8300'` -ge 1 2>/dev/null ]; then
          continue
        fi
        logger "SPS has been successfully stopped."
        echo "SPS has been successfully stopped."
done

exit 0
