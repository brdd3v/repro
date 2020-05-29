####################################################################################
# Courtesy of Shengfeng (Kent) Wu and Iulian Neamtiu, University of California, 2011
####################################################################################

import pdb,os,sys,re,commands
import make_list
import create_folder
import refine_vienna

def main(input):
	input = str.strip(input)
	if input.find("/") is not -1:
		input = input.replace("/", "")
		input = str.strip(input)
		create_folder.main(input)
		refine_vienna.main(input)
		make_list.main(input)
	else:
		create_folder.main(input)
		refine_vienna.main(input)
		make_list.main(input)
	

	
if __name__ == '__main__':
	input = sys.argv[1] #Folder name
	#pdb.runcall(main,input)
	main(input)
