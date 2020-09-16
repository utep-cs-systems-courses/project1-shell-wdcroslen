#! /usr/bin/env python

import os, sys, time, re

curr = os.getcwd()
spl = curr.split("/")
short = spl[-1]
#execute = ["wc", "shell2.py"] #default args for using execve()

dir_list = spl #probably don't need this

#maybe continuously update dir list and only allow redirects if in current list

def ls():
	directory_list = os.listdir(curr)
	for i in directory_list:
		print(i, end = "   ")
	print("")
	return

def lsdir(directory):
	change = False
	original = curr
	directory_list = os.listdir(curr)
	if directory.startswith("/"):
		change = True
		split = directory.split("/")
		directory = split[-1]
		index = 0
		while(index != len(split)-1): #change directory based on usr input
			if split[index] == '':
				index +=1
			os.chdir(split[index]) 
			index = index + 1
	
	if directory.endswith(".txt"):
		fdOut = os.open(directory + ".txt", os.O_CREAT | os.O_WRONLY)
		
	else:
		fdOut = os.open(directory + ".txt", os.O_CREAT | os.O_WRONLY)
						
	
	for a in directory_list:
		a = a + "\n"
		os.write(fdOut, a.encode()) # write to output file
	i = 0
	if (change): 
		while(i < len(split)-1): #return to current dir
			os.chdir("..")
			i = i +1
	return


def update_curr_dir(): 
	curr = os.getcwd()
	spl = curr.split("/")
	short = spl[-1]

def get_current():
	global curr
	curr = os.getcwd()
	os.write(1, (curr + "\n").encode())
	return

def get_short():
	global curr
	global short
	curr = os.getcwd()
	spl = curr.split("/")
	short = "\033[1;35;40m %s\x1b[0m" % spl[-1]
#	try:
#		short = [str(n) for n in input(short).split()]
#	except EOFError:
#		sys.exit(1)
	os.write(1, (short + "$ ").encode())
	return


def loop_shell():
	global short
	
	while True:
		if 'PS1' in os.environ:
			os.write(1,(os.environ['PS1']).encode())
			try:
				user_input = [str(n) for n in input().split()]
			except EOFError: 
				sys.exit(1)
		else:
			get_short()
			try:
				user_input = [str(n) for n in input().split()]
			except EOFError: 
				sys.exit(1)
			
#		user_input = ""
#		user_input = input()
		if user_input[0] == 'exit':
			sys.exit(1)
			
		if "cd" in user_input:
			try:
				os.chdir(user_input[1])
			except FileNotFoundError:
				os.write(1, ("-bash: cd: %s: No such file or directory\n" % directory).encode())
			
			continue
			
		else:
			rc = os.fork()  
		
			if '&' in user_input:
				user_input.replace("&",'')
				
			if user_input[0] == 'exit':
				quit(1)
				
			if rc < 0:
				os.write(2, ("fork failed, returning %d\n" % rc).encode())
				sys.exit(1)

			elif rc == 0:
				redirect(user_input)
				execChild(user_input)
				
			else:                           # parent (forked ok)
				if not '&' in user_input:
					childPidCode = os.wait() 
					

def parse2(cmdString):
	outFile = None
	inFile = None
	cmd = ''
	cmdString = re.sub(' +', ' ', cmdString)
	
	if '>' in cmdString:
		[cmd, outFile] = cmdString.split('>',1)
		outFile = outFile.strip()
		
	if '<' in cmd:
		[cmd, inFile] = cmd.split('<', 1)
		inFile = inFile.strip()
    
	elif outFile != None and '<' in outFile:
		[outFile, inFile] = outFile.split('<', 1)
		
		outFile = outFile.strip()
		inFile = inFile.strip()
	return cmd.split(), outFile, inFile


def redirect(args):
	if '>' in args or '<' in args:
		cmd,outFile,inFile = parse2(args)
		
	if '>' in args:
		os.close(1)
		os.open(outFile, os.O_CREAT | os.O_WRONLY)
		os.set_inheritable(1,True)
		
		execute = [cmd,outFile]
		execChild(execute)
		
	if '<' in args:
		os.close(0) 
		os.open(outFile, os.O_RDONLY)
		os.set_inheritable(1,True)
		
		execute = [cmd,outFile]
		execChild(execute)
	
	
def execChild(execute):
	for dir in re.split(":", os.environ['PATH']): # try each directory in the path
		program = "%s/%s" % (dir, execute[0])
		try:
			os.execve(program, execute, os.environ) # try to exec program
		except FileNotFoundError:
			pass 
#	return
#		time.sleep(2) 
	os.write(2, ("-bash: %s: command not found\n" % execute[0]).encode())
	quit(1)
	
	
if __name__ == "__main__":
	loop_shell()
	