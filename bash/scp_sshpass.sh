#!/bin/bash

hosts=`cat hosts.txt`

#-oStrictHostKeyChecking=no : avoids having to enter 'yes' all the time for RSA fingerprint 

for host in $hosts
        do 
          sshpass -f pwfile scp -oStrictHostKeyChecking=no ./<somefile>.tgz $host:<remote_path>
        done
exit 0
