
#TODO: I need to work on the redirect
#TODO: After looking at someone elses I need to remove my lists for cd and use my actual system
	#I can do this by using direct = os.listdir(os.getcwd())
	#path = "/var/www/html/"
  	#dirs = os.listdir( path )

import os, sys, time, re

pid = os.getpid()

pr,pw = os.pipe()

cd = "usr"
curr = cd
prev = None #prev doesnt work going back multiple directories
#maybe I can have a dict called prev and prev[] tells you what the previous one is
directory_list = {"usr":["Desktop","Downloads","temp"] , "Desktop":"", "Downloads":"oof" ,"temp":"none","none":"","oof":""} #make a dir list for each dir

prev_list = {"Desktop":"usr", "Downloads":"usr" ,"temp":"usr","none":"usr/temp","oof":"usr/Downloads"} #make a dir list for each dir

#TODO: Do I need a files list separately so you can ls them but not cd?


#maybe need to read and write this info to a file for if I create a dir or a file
#Actually no I just need to update the list.

#directory_list[Desktop] gives the list of the directories in desktop

def pipe_message():
	for f in (pr,pw):
		os.set_inheritable(f,True)
#	print("\npipe fds: pr=%d, pw=%d" % (pr,pw))

import fileinput



def switch_commands(argument): #TODO FIXME? : regardless I might not need this method
	
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
	if dir == "" or dir == " ":
		print("-bash: cd: '%s' : No such file or directory" % dir) 
		return
	
	if dir == "..":
		if cd == "usr":
			return
		spl = cd.split("/")
		curr = spl[-2]
		last = spl[-1]
		cd = prev_list[last]
		return
	
	if dir == curr:
		print("-bash: cd: '%s' : No such file or directory" % dir) 
		return
		#might not need this 'if' or 'curr' when I use a dict
		
	if dir in directory_list[curr]:  #FIXME: can cd '' in desktop
		prev = cd
		cd = cd + "/" + dir
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
			a = input(cd + "$ ")
			s = switch_commands(a)
			
			if (a[:2] == "cd"):   #for some reason I am not getting out of bounds with "cd"
				update_curr_dir(a[3:])   #I'm ok with that
				
			elif (a == "ls"):
				list_directories()
				
			else:
				print(s + "\n")

				
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