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
		while(index != len(split)-1):
			if split[index] == '':
				index +=1
			os.chdir(split[index])
			#back two times
			index = index + 1
	# itf it starts with / then check if first word in lisdir 
	
	#temp original dir
	#if yes then change current directory 
	
	#else create file in current directory
	
	if directory.endswith(".txt"):
		fdOut = os.open(directory + ".txt", os.O_CREAT | os.O_WRONLY)
		
	else:
		fdOut = os.open(directory + ".txt", os.O_CREAT | os.O_WRONLY)
						
	
	for a in directory_list:
		a = a + "\n"
		os.write(fdOut, a.encode()) # write to output file
	i = 0
	if (change):
		while(i < len(split)-1):
			os.chdir("..")
		
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

		if "cd" in user_input:
			directory = user_input.split("cd")[1].strip()
			try:
				os.chdir(directory)
			except FileNotFoundError:
				os.write(1, ("-bash: cd: %s: No such file or directory\n" % directory).encode())
			continue

		if user_input == 'ls':
			ls()
			continue

		if user_input == 'exit':
			quit(1)

		if "pwd" in user_input:
			get_current()
			continue
			
		if user_input.startswith("ls >"):
			redirect = user_input.split("ls >")[1].strip()
			lsdir(redirect)
			if redirect in dir_list:
				print("nice")
			continue
		
		elif "wc" in user_input or "python" in user_input:
			rc = os.fork()

			if rc < 0:
				os.write(2, ("fork failed, returning %d\n" % rc).encode())
				sys.exit(1)

			elif rc == 0:
				if "python" in user_input:
					file = user_input.split("python")[1].strip()
					args = ["python",file]
				else:
					file = user_input.split("wc")[1].strip()
					args = ["wc", file]
				for dir in re.split(":", os.environ['PATH']): # try each directory in the path
					program = "%s/%s" % (dir, args[0])
					try:
						os.execve(program, args, os.environ) # try to exec program
						continue
					except FileNotFoundError:
						pass 

				os.write(2, ("Child:    Could not exec %s\n" % args[0]).encode())
				quit(1)

			else:
				os.wait()
			continue

		os.write(1, ("-bash: %s: command not found\n" % user_input).encode())

		#TODO add redirect
		
		"""
		fdOut = os.open("p0-output.txt", os.O_CREAT | os.O_WRONLY)
		fdIn = os.open("p0-io.py", os.O_RDONLY)
		"""

if __name__ == "__main__":
	loop_shell()
	