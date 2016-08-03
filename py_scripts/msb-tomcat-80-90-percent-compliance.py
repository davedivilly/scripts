#!/usr2/ddivilly/PYTHON/bin/python

import os
import sys
from fabric.api import *

# Get list of hosts into a txt file
#os.system("mdb admin_contact=corp.web.admin alias=*crptcs* return name | grep name | awk '{print$2}' | sort  > ~/tmp/tomcat_msb.txt")

print "---------------------------------------------------------------------------"
print "To use this script type: fab -f msb-tomcat-80-90-percent-compliance.py task"
print "---------------------------------------------------------------------------"

# used to prevent annoying errors when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/tmp/tomcat_msb.txt', 'r').readlines()

# Fabric function that setups hyperic-lv non-prod agent
#
#  NOTE: crptcsstg7.qualcomm.com breaks this functions as it returns a string, due to there being non TcServer instances on this hosts.
#  Delete the hosts from the tomcat_msb.txt file and commment out the "os.system" line for this to run successfully.

def tomcat_msb():
        with settings(warn_only=True):
                a = sudo('grep -ir STRICT_SERVLET_COMPLIANCE /local/mnt/tcServer/vfabric-tc-server-standard-2.9.7.RELEASE/*/bin/setenv.sh | grep -v STRICT_SERVLET_COMPLIANCE=true | wc -l',quiet=True)
                b = sudo('grep -ir x-frame-option /local/mnt/tcServer/vfabric-tc-server-standard-2.9.7.RELEASE/*/conf/web.xml | grep -v DENY | wc -l',quiet=True)
                c = int(float(a)) + int(float(ba))
                print "---------------------------------------"
                print " Total is :", c
                print " Tomcat_MSB 80 - 90% compliance numbers "
                print "---------------------------------------"

def task():
        execute(hosts)
        execute(tomcat_msb)
