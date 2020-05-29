####################################################################################
# Courtesy of Shengfeng (Kent) Wu and Iulian Neamtiu, University of California, 2011
####################################################################################

import pdb,sys,os,commands,re,shlex,subprocess
#input a folder name
def main(input):
	version_name = os.listdir(str.strip(input))
	os.chdir(str.strip(input))
	try:
		for elem in version_name:
			elem_0 = elem.split("_")[-1]
			elem_0 = elem_0.split(".")[-2]
			cmd_0 = "mkdir Database." + elem_0 + ".m"
			p_0 = commands.getoutput(cmd_0)
			
			cmd_1 = "cp " + elem + " out_Database.sql" 
			p_1 = commands.getoutput(cmd_1)
			
			cmd_2 = "mv out_Database.sql" + " Database." + elem_0 + ".m" 
			p_2 = commands.getoutput(cmd_2)
			
			cmd_3 = "rm -rf " + elem 
			p_3 = commands.getoutput(cmd_3)

		os.chdir("../")
	except:
		print("!!!read error!!!")

if __name__ == '__main__':
	input = sys.argv[1]
	main(input)
	#pdb.runcall(main,input)
	#pdb.runcall(bm,line)
