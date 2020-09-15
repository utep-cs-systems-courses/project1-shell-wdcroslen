import os, sys, time, re

curr = os.getcwd()
spl = curr.split("/")
short = spl[-1]

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
	os.write(1, (short + "$ ").encode())
	return


def loop_shell():
	global short
	
	while True:
		if 'PS1' in os.environ:
			os.write(1,(os.environ['PS1']).encode())
		else:
			get_short()
		user_input = ""
		user_input = input()
		
		background = False  #if & in user_input don't wait
		if "&" in user_input:
			background = True
#			user_input.remove("&")
			
		elif "cd" in user_input and not background:
			directory = user_input.split("cd")[1].strip()
			try:
				os.chdir(directory)
			except FileNotFoundError:
				os.write(1, ("-bash: cd: %s: No such file or directory\n" % directory).encode())
			
			continue

		elif user_input == 'ls':
			ls()
			continue

		elif user_input == 'exit':
			quit(1)

		elif "pwd" in user_input:
			get_current()
			continue
			
		elif user_input.startswith("ls >") and background:
			redirect = user_input.split("ls >")[1].strip()
			lsdir(redirect)
			continue
		
		else:
			rc = os.fork()

			if rc < 0:
				os.write(2, ("fork failed, returning %d\n" % rc).encode())
				sys.exit(1)

			elif rc == 0:
#				if '&' in user_input:
#					user_input.replace("&",'')
					
				if "python" in user_input or "wc" in user_input:
					if "python" in user_input:
						file = user_input.split("python")[1].strip()
						args = ["python",file]
					elif "wc" in user_input:
						file = user_input.split("wc")[1].strip()
						args = ["wc", file]
					for dir in re.split(":", os.environ['PATH']): # try each directory in the path
						program = "%s/%s" % (dir, args[0])
						try:
							os.execve(program, args, os.environ) # try to exec program
							continue
						except FileNotFoundError:
							pass 
				
				time.sleep(2)   
				os.write(2, ("\nChild: Could not execute\n").encode())
				quit(1)

			else:
				if not background: #background tasks
					os.wait()
					continue
				else:
					user_input.replace("&",'')
					
				if user_input == 'ls':
					ls()
					continue
					
				elif "cd" in user_input:
					directory = user_input.split("cd")[1].strip()
					try:
						os.chdir(directory)
					except FileNotFoundError:
						os.write(1, ("-bash: cd: %s: No such file or directory\n" % directory).encode())
					continue	
				
				elif user_input.startswith("ls >"):
					redirect = user_input.split("ls >")[1].strip()
					lsdir(redirect)
					continue
		if not background:
			os.write(1, ("-bash: %s: command not found\n" % user_input).encode())

		

if __name__ == "__main__":
	loop_shell()
	