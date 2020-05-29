####################################################################################
# Courtesy of Shengfeng (Kent) Wu and Iulian Neamtiu, University of California, 2011
####################################################################################

import pdb,sys,os,commands,re,shlex,subprocess
#input a tag list
#output are out_*.sql for each version in ex_c_sql folders
#create a list of whole table name
#create refine_taglist
def main(input):
	whole_tname = set()
	ft_dict = {}
	tag_list = []
	try:
		f = open(input,'r')
		retrieve_error = [] #record error retrieve tag name
		cmd_1 = "mkdir ex_c_sql"
		p_1 = commands.getoutput(cmd_1)
		while 1:
			line = f.readline()
			if not line:
				break
			else:
				tag_list.append(str.strip(line))
				os.chdir("ex_c_sql")
				cmd_2 = "mkdir " + str.strip(line)
				p_2 = commands.getoutput(cmd_2)
				cmd_6 = "cp ../cpcpp2d ../cpcpp2d.sh " + "../" + str.strip(line) + "/cppfile"
				p_6 = commands.getoutput(str.strip(cmd_6))
				print cmd_6
				print p_6
				#pdb.set_trace()	
				try:	
					tname_s = bm(str.strip(line))
					while tname_s: #tname_s will empty
						tname = tname_s.pop()
						whole_tname.add(tname)
				except:
#					c = "pwd"
#					p = commands.getoutput(c)
#					print p
					tag_list.pop(-1)
					os.chdir("../../ex_c_sql")
					cmd_3 = "rm -rf " + str.strip(line)
					p_3 = commands.getoutput(cmd_3)
				#pdb.set_trace()			
				try:
#					pdb.set_trace()
					tmp_dict = bm_s(str.strip(line))
					if tmp_dict:
						for elem in tmp_dict:
#							if elem.split("_")[1].find(".sql") is -1:			
#								tmp_elem = "out_" + elem.split("_")[1] + ".sql"
#								elem = tmp_elem
							
							if elem not in ft_dict:
								ft_dict[elem] = tmp_dict[elem]
							else:
								tmpp_set = ft_dict[elem] 
								tmppp_set = tmp_dict[elem]
								ft_dict[elem] = tmpp_set | tmppp_set
				except:
					os.chdir("/extra/wus/myprogram")
					os.chdir("../../ex_c_sql")
					cmd_4 = "rm -rf " + str.strip(line)
					p_4 = commands.getoutput(cmd_4)
					
				os.chdir("/extra/wus/myprogram")
		f.close()
		
		if whole_tname:
			f = open("/extra/wus/myprogram/ex_c_sql/whole_tname_list",'w')	
			for elem in whole_tname:
				f.write(elem + "\n")
		#pdb.set_trace()			
		if ft_dict:
			f = open("/extra/wus/myprogram/ex_c_sql/whole_tname_list_s",'w')	
			for elem in ft_dict:
				f.write(elem + "\n")
				for elemm in ft_dict[elem]:
					f.write(elemm + "\n")
		if tag_list:
			f = open("/extra/wus/myprogram/ex_c_sql/refine_taglist",'w')	
			for elem in tag_list:
				f.write(elem + "\n")
	except:
		print("??????read data error??????")

def bm_s(line):
	line = line
	ft_dict = {}
	path = "/extra/wus/myprogram/" + str.strip(line) + "/schema"
	try:
		os.chdir(path)
		f = open('all_tname_log_s','r')
		lline = f.readline()
		while 1:
			#pdb.set_trace()			
			if lline == "\n":
				try:
					lline = f.next()
				except:
					break
			if lline.find(".sql") is not -1:
				if lline.split("_")[1].find(".sql") is -1:
					file_name = "out_" + lline.split("_")[1] + ".sql"
				else:
					file_name = str.strip(lline)
				try:
					lline = f.next()
				except:
					break
			else:
				tmp_tname = set()
				while lline.find(".sql") is -1:
					if lline and lline != "\n":
						tmp_tname.add(str.strip(lline))
					try:
						lline = f.next()
					except:
						break
				#pdb.set_trace()			
				if tmp_tname:
					if file_name in ft_dict.keys():
						tmp_set = tmp_tname
						ft_dict[file_name] = ft_dict[file_name] | tmp_set
						try:
							lline = f.next()
						except:
							break
					else:
						ft_dict[file_name] = tmp_tname
						if lline.split("_")[1].find(".sql") is -1:
							file_name = "out_" + lline.split("_")[1] + ".sql"
						else:
							file_name = str.strip(lline)
						try:
							lline = f.next()
						except:
							break
				
		#pdb.set_trace()			

		if ft_dict:
			return ft_dict
	except:
		return ft_dict

#create cppfile & folders for each version, then copy .cpp to from mozila folders to folders of each version in myprogram 
def bm(line):
	line = line
	tname_set = set()
	path = "/extra/wus/myprogram/" + str.strip(line) + "/schema"
	os.chdir(path)
	f = open('all_tname_log','r')
	for elem in f:
		tname_set.add(str.strip(elem))
	cmd = "/extra/wus/myprogram/" + str.strip(line) + "/cppfile"
	os.chdir(cmd)
	cmd_0 = "find -name  " + "\"" + "out_*.sql" + "\"" +" > sqlfile"
	p_0 = commands.getoutput(cmd_0)
	cmd_1 = "sh cpcpp2d.sh sqlfile"
	p_1 = commands.getoutput(cmd_1)

	try:
		f = open("sqlfile","r")
		while 1:
			c_line = f.readline()
			if not c_line:
				break
			else:
				cmd = str.strip(c_line) + " /extra/wus/myprogram/ex_c_sql/" + str.strip(line)
				p = commands.getoutput(cmd)
				print cmd
				print p
		print("!!!!!!End of Line!!!!!!")

	except:
		print "read error!!!"

	if tname_set:
		return tname_set

if __name__ == '__main__':
	input = sys.argv[1]
	main(input) #r_Tag or num or mono_list
	#pdb.runcall(main,input)
	#pdb.runcall(bm,line)
