#!/usr2/ddivilly/PYTHON/bin/python

import os
import sys
from fabric.api import * 

# Get list of hosts into a txt file
os.system("mdb admin_contact=corp.web.admin alias=*crptcs* return name | grep name | awk '{print$2}' | sort  > ~/tmp/tomcat_msb.txt")

print "---------------------------------------------------------------------------------------------------------"
print "To use this script type: fab -f msb-tomcat-80-90-percent-compliance.py -p <YourQUALPASS> hosts tomcat_msb"
print "---------------------------------------------------------------------------------------------------------"

# used to prevent annoying errors when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/tmp/tomcat_msb.txt', 'r').readlines()

# Fabric function that setups hyperic-lv non-prod agent
def tomcat_msb():
	sudo('grep -ir STRICT_SERVLET_COMPLIANCE /local/mnt/tcServer/vfabric-tc-server-standard-2.9.7.RELEASE/*/bin/setenv.sh | grep -v STRICT_SERVLET_COMPLIANCE=true | wc -l')
	sudo('grep -ir x-frame-option /local/mnt/tcServer/vfabric-tc-server-standard-2.9.7.RELEASE/*/conf/web.xml | grep -v DENY | wc -l')
        print "---------------------------------------"
        print "Tomcat_MSB 80 - 90% compliance numbers "
        print "---------------------------------------"
	
