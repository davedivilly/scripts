#!/bin/bash

while [ `sudo netstat -tulpn | grep -c '8100\|8200\|8300'` -ge 1 2>/dev/null ]; do
        echo "Waiting for SPS to STOP"
          sleep 3
        if [ `sudo netstat -tulpn | grep -c '8100\|8200\|8300'` -ge 1 2>/dev/null ]; then
          continue
        fi
        echo "SPS has been successfully stopped."
done

exit 0
