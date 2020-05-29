####################################################################################
# Courtesy of Shengfeng (Kent) Wu and Iulian Neamtiu, University of California, 2011
####################################################################################

import os, sys, pdb, commands, re
#input refined tag list
#must to create cppfile directory first, and put all .cpp into it. has done by read_tag now(bm.py)
#try to use os.listdir to open a directory, then open each file from it.
#create has_schema_log & no_schema_log in ./
#create schema folder, collect table name from each .sql, write all table name in one log, write all drop in one log
#revise it into function
#finish parsing the 'select'& 'drop' & 'insert' statement
#for dupliate tables,compare there attributes, if not the same, add version name append to its table's name(moz_anno_v#)

def main(input): #main function
	read_data = []
	read_data_s = []
	read_data_d = []
	cts1 = ""
	result = ""
	try:
		f = open(input,'r')
		while 1:
			t_line = f.readline()
			if not t_line:
				break
			else:
				ns = []
				hs = []
				ns_s = []
				hs_s = []
				ns_d = []
				hs_d = []
				hs_i = []
				ns_i = []
				op_path = str.strip(t_line) + "/cppfile"
				try:
					count = 0
					op_dir = os.listdir(op_path)
					for cpps in op_dir:  #for each cpp in the cppfile directory
						count += 1
						print t_line
						print count
						print cpps
						cpps = str.strip(cpps)
						op_f = open("/extra/wus/myprogram/"+str.strip(t_line)+"/cppfile/" + cpps,'r') #path to those .cpp
					#	op_f_s = open("/extra/wus/myprogram/"+str.strip(t_line)+"/cppfile/" + cpps,'r') #path to those .cpp
					#	op_f_d = open("/extra/wus/myprogram/"+str.strip(t_line)+"/cppfile/" + cpps,'r')
					#	op_f_i = open("/extra/wus/myprogram/"+str.strip(t_line)+"/cppfile/" + cpps,'r')
						#pdb.set_trace()
						(read_data, cts1) = ex_st_ct(op_f)
						#(read_data_s, ctss) = ex_st_s(op_f_s)
						#(read_data_d, ctsd) = ex_st_d(op_f_d)	
						#(read_data_i, ctsi) = ex_st_i(op_f_i)
						#	extract schema
						#	#pdb.set_trace	
						if read_data is not -1:
							hs.append(cpps)  #has schema log
							p = cpps.split(".")[1]	#parse input name & take the first elem
							#create .sql with table schema
							#it may catch duplicate table(same table name), use v# represent it
							a = open("/extra/wus/myprogram/"+str.strip(t_line)+"/cppfile/out_" + p + ".sql" , 'w')
							che_schema = cts1.split("\n")
							v_num = 0
							tmp_tnlist = []
							tmp_dict = {} 
							#use built-in iter function for list
							i = iter(che_schema)
							#pdb.set_trace()
							while 1:
								#pdb.set_trace
								try: 
									elem = i.next() #the first one
								except:
									print "!!!!!!Go over the che_schema!!!!!!"
									break
								#pdb.set_trace
								if elem.find("create table") is not -1:
									tmp_sqls = []
									tmp_sqls_2 = []
									re_line = elem.split("(")[0]
									re_tname = re_line.split()[-1]
									#pdb.set_trace
									if re_tname not in tmp_tnlist:
										tmp_tnlist.append(re_tname)
										while elem.find(";") is -1:
											tmp_sqls.append(elem)
											a.write(elem + "\n")
											try:
												elem = i.next()
											except:
												print "!!!!!!Go over the che_schema!!!!!!"
												break
										tmp_sqls.append(elem)
										tmp_dict[re_tname] = tmp_sqls	
										a.write(elem + "\n")
									else:
										while elem.find(";") is -1:
											tmp_sqls_2.append(elem)
											try:
												elem = i.next()
											except:
												print "!!!!!!Go over the che_schema!!!!!!"
												break
										tmp_sqls_2.append(elem)
										#pdb.set_trace
										if tmp_dict[re_tname] != tmp_sqls_2:
											v_num += 1
											n_tname = re_tname + "_v" + str(v_num)
											tmp_str = ''.join(tmp_sqls_2)
											tmp_str = tmp_str.replace(re_tname, n_tname)
											tmp_str = tmp_str.split("\n")
											tmp_dict[n_tname] = tmp_str
											for line in tmp_str:
												a.write(line + "\n")	
												
										
						else: 
							ns.append(cpps)	#no schema log
							print ("no schema in " + cpps)
					
							##pdb.set_trace	
						#	extract select statement
#						if read_data_s is not -1:
#							hs_s.append(cpps)  #has schema log
#							p_s = cpps.split(".")[0]	#parse input name & take the first elem
#							#create .sql with table schema
#							a_s = open("/extra/wus/myprogram/"+str.strip(t_line)+"/cppfile/select_" + p_s + ".sql" , 'w')
#							for elem in ctss:
#								a_s.write(elem)
#						else: 
#							ns_s.append(cpps)	#no schema log
#							print ("no select statement in " + cpps)
#				
#						#extract drop statement
#						if read_data_d is not -1:
#							hs_d.append(cpps)  #has schema log
#							p_d = cpps.split(".")[0]	#parse input name & take the first elem
#							#create .sql with table schema
#							a_d = open("/extra/wus/myprogram/"+str.strip(t_line)+"/cppfile/drop_" + p_d + ".sql" , 'w')
#							for elem in ctsd:
#								a_d.write(elem)
#						else: 
#							ns_d.append(cpps)	#no schema log
#							print ("no drop statement in " + cpps)
#
#						#extract insert statement
#						if read_data_i is not -1:
#							hs_i.append(cpps)  #has schema log
#							p_i = cpps.split(".")[0]	#parse input name & take the first elem
#							#create .sql with table schema
#							a_i = open("/extra/wus/myprogram/"+str.strip(t_line)+"/cppfile/insert_" + p_i + ".sql" , 'w')
#							for elem in ctsi:
#								a_i.write(elem)
#						else: 
#							ns_i.append(cpps)	#no schema log
#							print ("no drop statement in " + cpps)
					##pdb.set_trace
					# write into hs_log & ns_log
					if hs:
						hs_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/has_schema_log","w")
						for elem in hs:
							hs_log.write(elem+ "\n")
					if ns:
						ns_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/no_schema_log","w")
						for elem in ns:
							ns_log.write(elem + "\n")
					
#					if hs_s:
#						hs_s_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/has_select_log","w")
#						for elem in hs_s:
#							hs_s_log.write(elem+ "\n")
#					if ns_s:
#						ns_s_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/no_select_log","w")
#						for elem in ns_s:
#							ns_s_log.write(elem + "\n")
#					
#					if hs_d:
#						hs_d_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/has_drop_log","w")
#						for elem in hs_d:
#							hs_d_log.write(elem+ "\n")
#					if ns_d:
#						ns_d_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/no_drop_log","w")
#						for elem in ns_d:
#							ns_d_log.write(elem + "\n")
#					
#					if hs_i:
#						hs_i_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/has_insert_log","w")
#						for elem in hs_i:
#							hs_i_log.write(elem+ "\n")
#					if ns_i:
#						ns_i_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/no_insert_log","w")
#						for elem in ns_i:
#							ns_i_log.write(elem + "\n")
						
						op_f.close()
#						op_f_s.close()
#						op_f_d.close()
#						op_f_i.close()
				except:
					print "??????No Such Directory??????"
	
		print "!!!!!!Mission complete!!!!!!"
	except:
		print("read " + input +" error")

#extract the statement that includes CREATE TABLE
def ex_st_ct(obj):	
	op_f = obj
	read_data = []
	line = op_f.readline()
	while 1:
		if not line:
			break
		elif line.find("self executeSQL:@\"create table") is not -1 and line.find("select") is -1:
			if line.find("CREATE TABLE %s (%s)") is -1:
				che = line.split("(")[0]
				che = line.split()[-1]
				if che != "IF":
					if che != ");":
						while line.find(";") is -1:
							read_data.append(line)
							try:
								line = op_f.next() # wat if op_f.next() is ""
							except:
								break
						read_data.append(line)	#append the last found line
		try:
			line = op_f.next()
		except:
			break
#	pdb.set_trace()
#	print read_data
	if read_data:
		cts = ''.join(read_data)	#convert to str
		schemaPattern = re.compile(r'".*"\D?\D?;?')
		result = schemaPattern.findall(cts)	#type(result) = list 
	#	pdb.set_trace()	
		cts1 = ''.join(result)	#convert to str
		cts1 = cts1.replace('\"]','')
		cts1 = cts1.replace('\"','')
		cts1 = cts1.replace(';',";\n\n")

	#	pdb.set_trace()
		return (read_data, cts1)
	else:
		return (-1,-1)

#extract the statement that includes INSERT
def ex_st_i(obj):	
	op_f = obj
	read_data = []
	line = op_f.readline()
	while 1:
		if not line:
			break
		elif line.find("INSERT INTO") is not -1:
			while line.find(";") is -1:
				read_data.append(line)
				try:
					line = op_f.next() # wat if op_f.next() is ""
				except:
					break
			read_data.append(line)	#append the last found line
		try:
			line = op_f.next()
		except:
			break
#	#pdb.set_trace
#	print read_data
	if read_data:
		cts = ''.join(read_data)	#convert to str
		schemaPattern = re.compile(r'".*"\D?\D?;?')
		result = schemaPattern.findall(cts)	#type(result) = list 
	#	#pdb.set_trace	
		cts1 = ''.join(result)	#convert to str
		cts1 = cts1.replace('\n','')
		cts1 = cts1.replace('"),',';\n\n')
		cts1 = cts1.replace('"','')
	#	cts1 = cts1.replace('INSERT','\n\nINSERT')
	#	cts1 = cts1.replace('"','')
	#	cts1 = cts1.replace(';',";\n\n")

		return (read_data, cts1)
	else:
		return (-1,-1)

#extract the select statement
def ex_st_s(obj):	
	op_f = obj
	read_data = []	
	##pdb.set_trace
	line = op_f.readline()
	while 1:
#	for line in op_f:
		#print line
		##pdb.set_trace
		if not line:
			break
		elif line.find("//") is -1 and line.find("#") is -1:#kill comment
			if line.find("\"/*\"") is -1 and line.find("/*") is not -1:	#kill /*...*/
				while line and line.find("*/") is -1:
					line = op_f.next()
			if line.find("\"UPDATE") is not -1: #kill update statement
				while line and line.find(");") is -1:
					line = op_f.next()
#					if line.find(");") is not -1:
#						line = op_f.next()
#						break

			elif line.find("\"DELETE") is not -1: #kill delete statement
				while line and line.find(");") is -1:
					line = op_f.next()
#					if line.find(");") is not -1:
#						line = op_f.next()
#						break
			
			elif line.find("\"EXISTS") is not -1: #kill exists statement
				while line and line.find(");") is -1:
					line = op_f.next()
#					if line.find(");") is not -1:
#						line = op_f.next()
#						break
		
			elif line.find("\"INSERT") is not -1: #kill insert statement
				while line and line.find(");") is -1:
					line = op_f.next()
#					if line.find(");") is not -1:
#						line = op_f.next()
#						break
			
			elif line.find("static char* tagTable[] = {") is not -1: #kill a bug function
				while line and line.find("};\n") is -1:
					line = op_f.next()
			
			elif line.find("static JSConstDoubleSpec install_constants[] =\n") is not -1:
				while line and line.find("};\n") is -1:
					line = op_f.next()

			elif line.find("char *strkeys[] =\n") is not -1:
				while line and line.find("};\n") is -1:
					line = op_f.next()
			
			elif line.find("(\"SELECT\")") is -1 and line.find("\"SELECT ") is not -1:
				while line.find("\"),") is -1 and line.find(");") is -1 and line.find("\" ),") is -1:
					if line and line.find("#define") is not -1:	#kill bug
						while line.find(")\n") is -1 and line.find(") \\\n") is -1:
							line = op_f.next()
						line = op_f.next()
					elif line and line.find("\"UPDATE") is not -1: #kill bug
						while line.find(";") is -1:
							line = op_f.next()
						line = op_f.next()
					elif line and line.find("\"DELETE") is not -1:
						while line.find(";") is -1:
							line = op_f.next()
						line = op_f.next()
					elif line and line.find("\"EXISTS") is not -1:
						while line.find(";") is -1:
							line = op_f.next()
						line = op_f.next()
					elif line and line.find("\"INSERT") is not -1:
						while line.find(";") is -1:
							line = op_f.next()
						line = op_f.next()
					elif line and line.find("//") is -1:
						read_data.append(line)
						line = op_f.next() # wat if op_f.next() is ""
					else:
						break
				
				if line.find("\"INSERT INTO moz_cache") is -1:	#kill bug
					if line.find(");"):
						line = line.replace(');','),')
					if line.find("\" ),"):
						line = line.replace('\" ),','\"),')
					read_data.append(line)	#append the last found line
				else:
					line = op_f.next()
		try:	
			line = op_f.next()
		except:
			break

#   #pdb.set_trace
#   print read_data
	if read_data:
		cts = ''.join(read_data)    #convert to str
		schemaPattern = re.compile(r'".*"\)?,?')
		result = schemaPattern.findall(cts) #type(result) = list 
		##pdb.set_trace    
		cts1 = ''.join(result)  #convert to str
	#   cts1 = cts1.replace('),',';\n\n')
		cts1 = cts1.replace('""','')
		cts1 = cts1.replace('",','"),')
		cts1 = cts1.replace('"),',";\n\n")
		cts1 = cts1.replace('"','')
						
		return (read_data, cts1)
	else:
		return (-1,-1)

def ex_st_d(obj):
	
	op_f = obj
	read_data = []
	line = op_f.readline()
	while 1:
		if not line:
			break
		elif line.find("\"DROP TABLE") is not -1:
			while line.find(");") is -1:
				read_data.append(line)
				try:
					line = op_f.next() # wat if op_f.next() is ""
				except:
					break
			read_data.append(line)	#append the last found line
		try:
			line = op_f.next()
		except:
			break


#	#pdb.set_trace
#	print read_data
	if read_data:
		cts = ''.join(read_data)	#convert to str
		schemaPattern = re.compile(r'".*"\)?\)?;?')
		result = schemaPattern.findall(cts)	#type(result) = list 
		##pdb.set_trace	
		cts1 = ''.join(result)	#convert to str
		cts1 = cts1.replace('));',';\n\n')
	#	cts1 = cts1.replace('""','')
	#	cts1 = cts1.replace('",','"),')
	#	cts1 = cts1.replace('"),',";\n\n")
		cts1 = cts1.replace('"','')
		
		return (read_data, cts1)
	else:
		return (-1,-1)

#extract the name of the table from those out_*.sql in the folder
def ex_tname(input):

	try:
		f = open(input,'r')
		while 1:
			t_line = f.readline()
			if not t_line:
				break
			else:
				op_path = str.strip(t_line) + "/cppfile"
				op_dir = os.listdir(op_path)
				cmd = "mkdir /extra/wus/myprogram/"+str.strip(t_line)+"/schema"  #create a folder named schema to collect table name from each .sql
				mk = commands.getoutput(cmd)
				print cmd
				#pdb.set_trace()
				atl = [] #record all table name
				atl_s = [] #record all table name with .sql name
				atld = []
				atl_ds = []
				#pdb.set_trace()
				for sqls in op_dir:  #for each cpp in the cppfile directory
					sqls = str.strip(sqls)
					t_sqls = sqls.split(".")[1]
					t = 'sql'
					if not sqls:
						break
					elif t_sqls == t:  #string compare cannot use 't_sqls is t'
						if sqls.find("out_") is not -1:
							op_t = open("/extra/wus/myprogram/"+str.strip(t_line)+"/cppfile/" + sqls,'r') #path to those .cpp
							read_data = []
							atl_s.append("\n" + sqls + "\n")
							for line in op_t:
								if not line:
									break
								elif line.find("create table") is not -1: #-1 is not found
									line = line.split("(")[0]
									line = line.split()[-1]
									if line != "IF":
										if line != "%s":
											if line != ");":
												read_data.append(line)
												atl.append(line)
												atl_s.append(line)
							op_t.close()	
						elif sqls.find("drop_") is not -1:
							op_d = open("/extra/wus/myprogram/"+str.strip(t_line)+"/cppfile/" + sqls,'r') #path to those .cpp
							atl_ds.append("\n" + sqls + "\n")
							for line in op_d:
								if not line:
									break
								elif line.find("DROP") is not -1: #-1 is not found
									atl_ds.append(line)
									line = line.split()[2]
									atld.append(line)
							op_d.close()
				# collect all table names in log 
#				if atl:
#					all_tname_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/schema/all_tname_log","w")
#					for elem in atl:
#						all_tname_log.write(elem+"\n")
				filter_duplicate = set()
				if atl:
					all_tname_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/schema/all_tname_log","w")
					for elem in atl:
						filter_duplicate.add(elem)
					for elem in filter_duplicate:
						all_tname_log.write(elem+"\n")
					
					
					# collect all tables name map with each .sql
				if atl_s:
					all_tname_log_s = open("/extra/wus/myprogram/"+str.strip(t_line)+"/schema/all_tname_log_s","w")
					for elem in atl_s:
						all_tname_log_s.write(elem+"\n")


				# collect all drop .sql
				if atld:
					all_drop_log = open("/extra/wus/myprogram/"+str.strip(t_line)+"/schema/all_drop_log","w")
					for elem in atld:
						all_drop_log.write(elem+"\n")
				if atl_ds:
					all_drop_log_s = open("/extra/wus/myprogram/"+str.strip(t_line)+"/schema/all_drop_log_s","w")
					for elem in atl_ds:
						all_drop_log_s.write(elem+"\n")
		
		print "!!!!!!ex_tname complete!!!!!!"	
	except:
		print("read sql data error")

if __name__ == '__main__':
	input = sys.argv[1]
	#op_folders(input)
	#pdb.runcall(op_folders,input)
	#pdb.runcall(main,path)
	#pdb.runcall(ex_tname,path)
	#pdb.runcall(main,input)
	#pdb.runcall(ex_tname,input) #can run line by line with out put #pdb.set_trace after each line exclusivily to this function by using 'n'
	main(input) #r_Tag
	ex_tname(input)	#r_Tag
