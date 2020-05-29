####################################################################################
# Courtesy of Shengfeng (Kent) Wu and Iulian Neamtiu, University of California, 2011
####################################################################################

import pdb,sys,os,commands,re,shlex

#refine vienna's schema(try to solve the DATA TYPE problem) I add INTEGER

def main(input):
	mono_folder = input
	cmd_0 = "mkdir " + str.strip(input) + "/refine"
	p_0 = commands.getoutput(cmd_0)
	
	#pdb.set_trace()
	fl = open(str.strip(input) + "/refine/vienna_list", 'w')
	for version in os.listdir(mono_folder):
		#pdb.set_trace()
		if version != "refine" and version != "list":
			cmd_1 = "mkdir " + mono_folder + "/refine/" + version 
			p_1 = commands.getoutput(cmd_1)
			os.chdir(mono_folder)
			for elem in os.listdir(version):
				try:
					if elem.split('.')[1] == 'sql':
						f_0 = open(version + "/" + elem, 'r')
						refine_f0 = f_0.read()
						f_0.close()
						cmd_3 = "rm -rf " + version + "/" + elem
						p_3 = commands.getoutput(cmd_3)

						f_0 = open(version + "/" + elem, 'w')
						if refine_f0.find("))") is not -1:
							refine_f0 = refine_f0.replace("))", ");\n")
						for content in refine_f0:
							f_0.write(content)
						f_0.close()

						#pdb.set_trace()
						f = open(version + "/" + elem, 'r')
						cmd = "pwd"
						p = commands.getoutput(cmd)
						print p
						ff = open("refine/" + version + "/" + elem.split(".")[-2] + ".sql" , 'w')
						line = f.next()

						#pdb.set_trace()
						while 1:
							if line.find("create table") is not -1:
								lline = line.split(",")
								tmp = []
								for e_lline in lline:
									if e_lline.find("primary key") is -1 and e_lline.find(";") is -1:
										revise_el = e_lline + " INTEGER, "
										tmp.append(revise_el)
									elif e_lline.find(";") is not -1:
										tmp_elline = e_lline.split(")")[0] + " INTEGER);\n"
										tmp.append(tmp_elline)
									else:
										tmp.append(e_lline + ", ")
								for elemm in tmp:
									ff.write(elemm)

							try:
								line = f.next()
							except:
								break

						#pdb.set_trace()
						ff.close()
						f.close()
						fl.write(elem + "\n")
						cmd = "pwd"
						p = commands.getoutput(cmd)
						print p
				
						os.chdir("../")
					
				except:	
					print "OPEN " + str.strip(input) + "/" + elem + " ERROR???"	
	fl.close()

if __name__ == '__main__':
	input = sys.argv[1] #folder
	main(input)
	#pdb.runcall(main,input)
