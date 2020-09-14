import os, sys, time, re

pid = os.getpid()

pr,pw = os.pipe()

cd = "$ "
curr = cd
prev = None
directory_list = {"$ ":["Desktop","Downloads","temp"] , "Desktop":"", "Downloads":"oof" ,"temp":"none"} #make a dir list for each dir

#maybe use dict

#directory_list[Desktop] gives the list of the directories in desktop

def pipe_message():
	for f in (pr,pw):
		os.set_inheritable(f,True)
#	print("\npipe fds: pr=%d, pw=%d" % (pr,pw))

import fileinput



def switch_commands(argument): 
	
    switcher = { 
        "cd": "Change Directory", 
        "ls": "List Directories", 
        "cd ..": "Parent Directory", 
		"exit":"Now terminating...Goodbye World",
		"Exit":"Now terminating...Goodbye World"
    } 
    return switcher.get(argument, "command not found") 


def update_curr_dir(dir): 
	global cd 
	global curr
	global prev
	#TODO: add cd ..
	#TODO: updating directory is backwards
	#TODO:  Make it sot that you can't cd into the directory you are already on.
	if dir == "..":
		cd = prev
		return
	
	
	if dir == curr:
		print("-bash: cd: '%s' : No such file or directory" % dir) 
		return
		#might not need this 'if' or 'curr' when I use a dict
		
	if dir in directory_list[curr]:  #FIXME: can cd '' in desktop
		cd = dir + " " + cd
		curr = dir
		
	else: 
		print("-bash: cd: '%s' : No such file or directory" % dir)
	

def list_directories():
	global curr
	if type(directory_list[curr]) == str :
		print(directory_list[curr])
		return
	for i in directory_list[curr]:
		print(i, end ="   ")
	print("")
	
	
def after_fork():
	if rc < 0:
		print("Fork Failed")
		sys.exit(1)
	elif rc == 0: #child
		print("Hello User! Please enter a command.\n")
		time.sleep(.5)
		a = ""
		while ( a != "exit"):
			if a == "Exit":
				break
			time.sleep(.5)
			a = input(cd)
			s = switch_commands(a)
			
			if (a[:2] == "cd"):   #for some reason I am not getting out of bounds with "cd"
				update_curr_dir(a[3:])   #I'm ok with that
				
			elif (a == "ls"):
				list_directories()
#				for i in directory_list:
#					print(i, end ="   ")
#				print("")
				
			else:
				print(s + "\n")

#				if (s != "command not found"):
#					break  #break out of loop without exit
				
				
				
		os.close(1)
		os.dup(pw)
		for fd in (pr,pw):
			os.close(fd)
			

	else: #parent
		os.close(0)
		os.dup(pr)
		for fd in (pw,pr):
			os.close(fd)
		for line in fileinput.input():
			print(line)
		
if __name__ == "__main__":
	pipe_message()
	rc = os.fork()
	after_fork()