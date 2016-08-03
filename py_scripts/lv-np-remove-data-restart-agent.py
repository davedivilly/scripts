#!/usr2/ddivilly/PYTHON/bin/python

import os
import sys
from fabric.api import * 

# Get lisy of hosts into a txt file
#os.system("mdb admin_contact=corp.web.admin office_location=LAS.COLO2 return alias | grep alias | awk -F' ' '{print$2}' | sort | grep -v prd | grep -v x |grep switch  > ~/SCRIPTS/PYTHON/remove_restart.txt")

print "-----------------------------------------------------------------------"
print "To use this script type: fab -f lv-np-remove-data-restart-agent.py task"
print "-----------------------------------------------------------------------"

# used to prevent annoying errors when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/SCRIPTS/PYTHON/remove_restart.txt', 'r').readlines()

# Fabric function that setups hyperic-lv non-prod agent
def remove_restart():
	sudo('/local/mnt/hyperic/agent-switch/bin/hq-agent.sh stop')
	sudo('rm -rf /local/mnt/hyperic/agent-switch/data')
	sudo('/local/mnt/hyperic/agent-switch/bin/hq-agent.sh start')
	print "-----------------------------------"
        print "Data DIR removed & Agent restarted "
        print "-----------------------------------"
        
def task():
	execute(hosts)
	execute(remove_restart)
	
