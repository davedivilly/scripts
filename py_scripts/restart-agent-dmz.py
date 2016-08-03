#!/usr2/ddivilly/PYTHON/bin/python
import os
import sys
from fabric.api import * 

# Get lisy of hosts into a txt file
#os.system("mdb admin_contact=corp.web.admin office_location=LAS.COLO2 return alias | grep alias | awk -F' ' '{print$2}' | sort | grep -v prd | grep -v x |grep switch  > ~/SCRIPTS/PYTHON/remove_restart.txt")

print "-----------------------------------------------------"
print "To use this script type: fab -f restart-agent.py task"
print "-----------------------------------------------------"

# used to prevent annoying errors when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/SCRIPTS/PYTHON/sd2n.txt', 'r').readlines()

# Fabric function that setups hyperic-lv non-prod agent
def restart():
	sudo('/local/mnt/hyperic/agent/bin/hq-agent.sh stop')
	sudo('sed -i -e s/agent.setup.unidirectional=no/agent.setup.unidirectional=yes/g /local/mnt/hyperic/agent/conf/agent.properties')
	sudo('rm -rf /local/mnt/hyperic/agent/data')
	sudo('/local/mnt/hyperic/agent/bin/hq-agent.sh start')
	print "-------------------------------------------"
        print "SD agent restarted on : ", env.host_string
        print "-------------------------------------------"

def task():
	execute(hosts)
	execute(restart)
