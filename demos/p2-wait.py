#! /usr/bin/env python3

import os, sys, time

pid = os.getpid()

os.write(1, ("\nAbout to fork (pid:%d)\n" % pid).encode())

rc = os.fork()

if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)
elif rc == 0:                   # child
    os.write(1, ("Child: My pid==%d.  Parent's pid=%d\n" % 
                 (os.getpid(), pid)).encode())
    time.sleep(1)               # block for 1 second
    os.write(1, "Child   ....terminating now with exit code 0\n".encode())
    sys.exit(0)
else:                           # parent (forked ok)
    os.write(1, ("Parent: My pid=%d.  Child's pid=%d\n" % 
                 (pid, rc)).encode())
    childPidCode = os.wait() #Guessing wait returns PID of what you waited on
    os.write(1, ("Parent: Child %d terminated with exit code %d\n" % 
                 childPidCode).encode())

	
#	"""
#	Trace:  
#		pid = 1
#		#write
#		
#		{Parent}
#		rc = fork() ## which = 2 because its the pid of the forked program
#		
#		else:
#			#write
#			cPC = wait() which = 2 because its the pid of the waited program
#		
#		#After wait go to child
#		
#		
#		{Child}
#		rc = 0 ## succesful fork
#		
#		elif: 
#			#write
#			#sleep one second
#			#write:
#			#exit (Is this necessary?)
			#after exit go back to wait in parent
#		
#		{Parent}
#		#write
#
#	"""