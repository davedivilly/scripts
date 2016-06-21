#!/usr2/ddivilly/PYTHON/bin/python

import os
import sys
from fabric.api import * 

# Get lisy of hosts into a txt file
#os.system("mdb admin_contact=corp.web.admin office_location=LAS.COLO2 return alias | grep alias | awk -F' ' '{print$2}' | sort | grep -v prd | grep -v x  > ~/tmp/non-prd-internal.txt")

print "---------------------------------------------------------------------------------"
print "To use this script type: fab -f fixhostagent.py -p <YourQUALPASS> hosts fix_agent"
print "---------------------------------------------------------------------------------"

# used to prevent annoying errors when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/SCRIPTS/PYTHON/host.txt', 'r').readlines()

# Fabric function that setups hyperic-lv non-prod agent
def fix_agent():
	sudo('/local/mnt/hyperic/agent/bin/hq-agent.sh stop')
	sudo('mv /local/mnt/hyperic/agent /local/mnt/hyperic/agent_old_2')
	sudo('cp -r /local/mnt/hyperic/agent_old_2/agent /local/mnt/hyperic/')
	sudo('/local/mnt/hyperic/agent/bin/hq-agent.sh start')
	sudo('cat /local/mnt/hyperic/agent/conf/agent.properties | grep agent.setup.camIP')

