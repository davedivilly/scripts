#!/usr2/ddivilly/PYTHON/bin/python

import os
import sys
from fabric.api import * 

# Get lisy of hosts into a txt file
#os.system("mdb admin_contact=corp.web.admin office_location=LAS.COLO2 return alias | grep alias | awk -F' ' '{print$2}' | sort | grep -v prd | grep -v x  > ~/tmp/non-prd-internal.txt")

print "----------------------------------------------------------------------------------------------"
print "To use this script type: fab -f which-hyperic.py -p <YourQUALPASS> hosts hyperic_check"
print "----------------------------------------------------------------------------------------------"

# used to prevent annoying errors when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/tmp/non-prd-internal.txt', 'r').readlines()

# Fabric function that setups hyperic-lv non-prod agent
def hyperic_check():
	sudo('cat /local/mnt/hyperic/agent/conf/agent.properties | grep agent.setup.camIP')
	
