#!/usr2/ddivilly/PYTHON/bin/python

import os
import sys
from fabric.api import * 

print "---------------------------------------------------------------------"
print "To use this script type: fab -f apply-splunk-duty.py hosts splunk ---" 
print "---------------------------------------------------------------------"

# used to prevent annoying errors when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/SCRIPTS/PYTHON/splunk-hosts.txt', 'r').readlines()

# Fabric function that setups hyperic-lv non-prod agent
def splunk():
    sudo('/usr/local/sbin/duty add splunka.mwssapache')
    print "-----------------------------------------"
    print " Splunk duty has been added to host ---- "
    print "-----------------------------------------"
	
