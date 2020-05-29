####################################################################################
# Courtesy of Shengfeng (Kent) Wu and Iulian Neamtiu, University of California, 2011
####################################################################################

import os, sys, pdb, commands, re
#input tag list
def main(input): #main function
	try:
		input = str.strip(input)
		if input.find("/") is not -1:
			folder_name = input.replace("/" , "")
			folder_name = str.strip(folder_name)
			f = open(folder_name + "_list","w")
			filename = os.listdir(input) #list of file name
			for elem in filename:
				if elem.find("refine") is -1:
					f.write(elem + "\n")
		else:
			f = open(input + "_list","w")
			filename = os.listdir(input) #list of file name
			for elem in filename:
				if elem.find("refine") is -1:
					f.write(elem + "\n")
	except:
		print("!!!ERROR!!!")


if __name__ == '__main__':
	input = sys.argv[1]
	#pdb.runcall(main,input)
	main(input) #input folder name
