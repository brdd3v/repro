####################################################################################
# Courtesy of Shengfeng (Kent) Wu and Iulian Neamtiu, University of California, 2011
####################################################################################

import pdb,os,sys,re,commands
#create cppfile for each release and create cppfile folder and move .m into cppfile

def main(input):
	input = str.strip(input)
	f = open(input, 'r')
	while 1:
		line = f.readline()
		if not line:
			break
		else:
			line = str.strip(line)
			os.chdir(line)
			cmd_0 = "mkdir cppfile"
			p_0 = commands.getoutput(cmd_0)
			cmd_1 = "mv *.m cppfile"
			p_1 = commands.getoutput(cmd_1)
			os.chdir("../")
	
if __name__ == '__main__':
	input = sys.argv[1] 
	#pdb.runcall(main,input)
	main(input) #list
