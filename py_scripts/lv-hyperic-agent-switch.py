#!/usr2/ddivilly/PYTHON/bin/python

import os
import sys
from fabric.api import * 

# Get lisy of hosts into a txt file
#os.system("mdb admin_contact=corp.web.admin office_location=LAS.COLO2 return alias | grep alias | awk -F' ' '{print$2}' | sort | grep -v prd | grep -v x  > ~/SCRIPTS/PYTHON/non-prd-internal.txt")
print "----------------------------------------------------------------"
print "To use this script type: fab -f lv-hyperic-agent-switch.py task "
print "----------------------------------------------------------------"

# used to prevent annoying errors when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/SCRIPTS/PYTHON/fix-agents.txt', 'r').readlines()

# Fabric function that setups hyperic-lv non-prod agent
def agent_setup():
	with cd('/local/mnt/workspace/'):
	     sudo('tar -zxvf /prj/webadmin/scripts/hyperic/agent-switch_USED_AS_2ND_AGENT_HYPERICNP-LV.tgz')
             sudo('chown -R root:bin agent-switch')
             sudo('chmod -R 755 agent-switch')
             #sudo('/local/mnt/hyperic/agent-switch/bin/hq-agent.sh stop')
             sudo('cp -r /local/mnt/workspace/agent-switch /local/mnt/hyperic/agent-switch')
             sudo('rm -rf /local/mnt/hyperic/agent-switch/data')
             sudo('/local/mnt/hyperic/agent-switch/bin/hq-agent.sh start')
             sudo('rm -rf /local/mnt/workspace/agent-switch')
	     print "--------------------------------------------"
             print "Hyperic-lv Non-Prod Agent has been setup on:", env.host_string 
             print "--------------------------------------------"
	
def task():
	execute(hosts)
	execuet(agent_setup)
