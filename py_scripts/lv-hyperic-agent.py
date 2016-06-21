#!/usr2/ddivilly/PYTHON/bin/python

import os
import sys
from fabric.api import * 

# Get lisy of hosts into a txt file
#os.system("mdb admin_contact=corp.web.admin office_location=LAS.COLO2 return alias | grep alias | awk -F' ' '{print$2}' | sort | grep -v prd | grep -v x  > ~/SCRIPTS/PYTHON/non-prd-internal.txt")

print "---------------------------------------------------------------------------------------"
print "To use this script type: fab -f lv-hyperic-agent.py -p <YourQUALPASS> hosts agent_setup"
print "---------------------------------------------------------------------------------------"

# used to prevent annoying errors when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/SCRIPTS/PYTHON/non-prd-internal.txt', 'r').readlines()

# Fabric function that setups hyperic-lv non-prod agent
def agent_setup():
	with cd('/local/mnt/workspace/'):
	     sudo('tar -zxvf /prj/webadmin/scripts/hyperic/agent_lvnonprod.tar.gz')
	     sudo('chown -R root:bin agent')
             sudo('chmod -R 755 agent') 
	     sudo('/local/mnt/hyperic/agent/bin/hq-agent.sh stop')
      	     sudo('mv /local/mnt/hyperic/agent /local/mnt/hyperic/agent_hypericnp_SD')
	     sudo('cp -r /local/mnt/workspace/agent /local/mnt/hyperic/')
      	     sudo('/local/mnt/hyperic/agent/bin/hq-agent.sh start')
	     sudo('rm -rf /local/mnt/workspace/agent')
	     sudo('rm -rf /local/mnt/hyperic/agent_hypericnp_SD')
	     print "-----------------------------------------"
             print "Hyperic-lv Non-Prod Agent has been setup "
             print "-----------------------------------------"
	
