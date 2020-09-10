import os, sys, time, re

pid = os.getpid()

pr,pw = os.pipe()

def pipe_message():
	for f in (pr,pw):
		os.set_inheritable(f,True)
	print("\npipe fds: pr=%d, pw=%d" % (pr,pw))

import fileinput



def switch_commands(argument): 
	
    switcher = { 
        "cd": "Change Directory", 
        "ls": "List Directories", 
        "cd ..": "Parent Directory", 
		"exit":"Now terminating...Goodbye World",
		"Exit":"Now terminating...Goodbye World"
    } 
    return switcher.get(argument, "Err Command Not Found") 

def after_fork():
	if rc < 0:
		print("Fork Failed")
		sys.exit(1)
	elif rc == 0: #child
		print("Hello User! Please enter a command.")
		os.close(1)
		os.dup(pw)
		for fd in (pr,pw):
			os.close(fd)
		a = ""
		while ( a != "exit"):
			if a == "Exit":
				break
			a = input("$")
			print(switch_commands(a))

	else: #parent
		os.close(0)
		os.dup(pr)
		for fd in (pw,pr):
			os.close(fd)
		for line in fileinput.input():
			print(line)
		
if __name__ == "__main__":
	print("hi")
	pipe_message()
	rc = os.fork()
	after_fork()