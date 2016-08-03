#!/usr2/ddivilly/PYTHON/bin/python

from __future__ import with_statement
from fabric.contrib.console import confirm
from fabric.api import *
from fabric.main import main
import os
import sys
import time

# Removes the need to type "fab -f " etc. Just call the script as normal #

if __name__ == '__main__':
        sys.argv = ['fab', '-f', __file__, 'task']
        main()

# used to prevent warnings when default is used "/bin/bash -l -c"
env.shell = "/bin/bash -c"

# Warns only on errors.
#env.warn_only = True

# Skips over unavailable hosts
env.skip_bad_hosts = True

# fabric functon that reads host txt file
def hosts():
    env.hosts = open('/usr2/ddivilly/SCRIPTS/PYTHON/agent-cleanup/sd2n.txt','r').readlines()

# Fabric function that tests if 2 agents exists on a host and cleans up unnecessary directories #
def test_1():
        with settings(warn_only=True):
                a = run('ps -ef | grep -c "hyperic/agent/"',quiet=True)
                b = run('ps -ef | grep -c "hyperic/agent-switch/"',quiet=True)
                if int(a) <= 2 and int(b) >= 3 :
                        print "----------------------------------------------------------------------"
                        print "Success. Only one agent installed on:",env.host_string,": agent-switch"
                        print "----------------------------------------------------------------------"
                        print "\n"
                        d = run("ls -al /local/mnt/hyperic/ | grep -v agent-switch$ | awk -F' ' '{print$9}'",quiet=True)
                        print "------------------------------------------------------------------"
                        print "Deleting any unecessary Agent directories in /local/mnt/hyperic/ : \n", d
                        print "------------------------------------------------------------------"
                        print "\n"
                        time.sleep(3)
                        sudo('find /local/mnt/hyperic/* -maxdepth 0 -type d ! -name "agent-switch" -exec rm -rf {} \;',quiet=True)
                        print "\n"
                        print "Restarting currently installed Agent .."
                        print "\n"
                        sudo('/local/mnt/hyperic/agent-switch/bin/hq-agent.sh stop',quiet=True)
                        sudo('rm -rf /local/mnt/hyperic/agent-switch/data',quiet=True)
                        sudo('/local/mnt/hyperic/agent-switch/bin/hq-agent.sh start',quiet=True)
                elif int(a) >= 3 and int(b) <= 2 :
                        execute(test_2)
                elif int(a) >= 3 and int(b) >= 3:
                        execute(test_3)
                elif int(a) <= 2 and int(b) <= 2 and not confirm("No Agent installed. Continue anyway?"):
                        abort("Aborting at user request.")
def test_2():
        with settings(warn_only=True):
                a = run('ps -ef | grep -c "hyperic/agent/"',quiet=True)
                b = run('ps -ef | grep -c "hyperic/agent-switch/"',quiet=True)
                if int(a) >= 3 and int(b) <= 2 :
                        print "\n"
                        print "----------------------------------------------------------------"
                        print "Success. Only one agent installed on:",env.host_string,": agent "
                        print "----------------------------------------------------------------"
                        print "\n"
                        d = run("ls -al /local/mnt/hyperic/ | grep -v agent$ | awk -F' ' '{print$9}'",quiet=True)
                        print "------------------------------------------------------------------"
                        print "Deleting any unecessary Agent directories in /local/mnt/hyperic/ : \n", d
                        print "------------------------------------------------------------------"
                        time.sleep(3)
                        sudo('find /local/mnt/hyperic/* -maxdepth 0 -type d ! -name "agent" -exec rm -rf {} \;',quiet=True)
                        print "\n"
                        print "Restarting currently installed Agent .."
                        print "\n"
                        sudo('/local/mnt/hyperic/agent/bin/hq-agent.sh stop',quiet=True)
                        sudo('rm -rf /local/mnt/hyperic/agent/data',quiet=True)
                        sudo('/local/mnt/hyperic/agent/bin/hq-agent.sh start',quiet=True)
def test_3():
        with settings(warn_only=True):
                a = run('ps -ef | grep -c "hyperic/agent/"',quiet=True)
                b = run('ps -ef | grep -c "hyperic/agent-switch/"',quiet=True)
                if int(a) >= 3 and int(b) >= 3:
                        print "\n"
                        print "------------------------------------------------"
                        print "There are 2 agents runing on this host ........."
                        print "\n"
                        print "THERE CAN BE ONLY ONE .........................."
                        print "\n"
                        print "The Kurgen will now remove the unnecessary agent"
                        print "------------------------------------------------"
                        print "\n"
                        time.sleep(3)
                        sudo('/local/mnt/hyperic/agent/bin/hq-agent.sh stop',quiet=True)
                        sudo('rm -rf /local/mnt/hyperic/agent',quiet=True)
                        print "\n"
                        print "-----------------------------------------"
                        print "2nd Agent removed from :", env.host_string
                        print "-----------------------------------------"
                        print "\n"
                        d = run("ls -al /local/mnt/hyperic/ | grep -v agent-switch$ | awk -F' ' '{print$9}'",quiet=True)
                        print "\n"
                        print "------------------------------------------------------------------"
                        print "Deleting any unecessary Agent directories in /local/mnt/hyperic/: \n", d
                        print "------------------------------------------------------------------"
                        sudo('find /local/mnt/hyperic/* -maxdepth 0 -type d ! -name "agent-switch" -exec rm -rf {} \;',quiet=True)
                        print "\n"
                        print "Restarting currently installed Agent .."
                        print "\n"
                        sudo('/local/mnt/hyperic/agent-switch/bin/hq-agent.sh stop',quiet=True)
                        sudo('rm -rf /local/mnt/hyperic/agent-switch/data',quiet=True)
                        sudo('/local/mnt/hyperic/agent-switch/bin/hq-agent.sh start',quiet=True)
# call the function(sub-task)here in order to execute it
def task():
    execute(hosts)
    execute(test_1)
