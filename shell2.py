import os, sys, time, re

curr = os.getcwd()
spl = curr.split("/")
short = spl[-1]


def ls():
	directory_list = os.listdir(curr)
	for i in directory_list:
		print(i, end = "   ")
	print("")
	return


def update_curr_dir(): 
	curr = os.getcwd()
	spl = curr.split("/")
	short = spl[-1]


def get_current():
	global curr
	curr = os.getcwd()
	os.write(1, (curr + "$ ").encode())
	return

def get_short():
	global curr
	curr = os.getcwd()
	spl = curr.split("/")
	short = spl[-1]
	os.write(1, (curr + "$ ").encode())
	return


def loop_shell():
	
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
				os.write(1, ("No such file or directory.\n").encode())
			continue

		if user_input == 'ls':
			ls()
			continue

		if user_input == 'exit':
			sys.exit()

		if "cwd" in user_input:
			get_current()
			continue
			
		#TODO add redirect and execute

if __name__ == "__main__":
	loop_shell()
	