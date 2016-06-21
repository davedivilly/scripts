#!/usr2/ddivilly/PYTHON/bin/python

from __future__ import with_statement
from fabric.contrib.console import confirm
from fabric.api import * 
import os
import sys

# Get lisy of hosts into a txt file
#os.system("mdb admin_contact=corp.web.admin office_location=LAS.COLO2 return alias | grep alias | awk -F' ' '{print$2}' | sort | grep -v prd | grep -v x |grep switch  > ~/SCRIPTS/PYTHON/remove_restart.txt")

print "---------------------------------------------------"
print "To use this script type: fab -f agent-check.py task"
print "---------------------------------------------------"

# used to prevent annoying errors when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/SCRIPTS/PYTHON/fix-agents.txt', 'r').readlines()

# Fabric function that tests if "agent-switch" directory exists
def test():
	with settings(warn_only=True):
        	result = sudo('rm -f /local/mnt/hyperic/agent-old-SD-agent_TO_BE_DELETED.tgz', capture=True)
    	if result.failed and not confirm("DELETE failed. Continue anyway?"):
        	abort("Aborting at user request.")

# name the function here in order to execute it 
def task():
    execute(hosts)
    execute(test)
