import re,json,xlrd,datetime
#from d1_胃病.dict import data_process_dict,extract_rule_dict,computer_rule_dict

class Extract(object):
	def __init__(self,data,args):
		# super(Struct, self).__init__(*args))
		self.data=data
		self.replace_words=args['replace_words']
		self.search_with=args['search_with']
		self.search_without=args['search_without']
		self.search_region=args['search_region']

	def main(self):
		entity=[]
		if self.replace_words!={}:
			for k,v in self.replace_words.items():
				self.data=self.data.replace(k,v)
		if self.search_with[0][1] != '':
			self.struct_search_with(self.data,entity,self.search_with)
		if self.search_without[0][1] != '':
			self.struct_search_without(self.data,entity,self.search_without)
		if self.search_region[0][1] != '':
			self.struct_search_region(self.data,entity,self.search_region)
		return entity

	def struct_search_with(self,line,entity,search_with):
		zhuanyi=['*','d']
		for one in search_with:
			if one[0] in zhuanyi:
				if one[2] in zhuanyi:
					rule='\\' + one[0] + one[1] + '\\' + one[2]
				else:
					rule='\\' + one[0] + one[1] + one[2]
			else:
				if one[2] in zhuanyi:
					rule= one[0] + one[1] + '\\' + one[2]
				else:
					rule= one[0] + one[1] + one[2]
			for m in re.finditer(rule,line):
				l1=len(re.findall('[\(|\)|\\\]',one[0]))
				l2=len(re.findall('[\(|\)|\\\]',one[2]))
				if one[0] in zhuanyi:
					if one[2] in zhuanyi:
						entity.append({'entity':re.sub('\\'+one[0]+'|\\'+one[2],'',m.group()),'start':m.start()+len(one[0]),'end':m.end()-len(one[2])})
					else:
						entity.append({'entity':re.sub('\\'+one[0]+'|'+one[2],'',m.group()),'start':m.start()+len(one[0]),'end':m.end()-len(one[2])+l2})
				else:
					if one[2] in zhuanyi:
						entity.append({'entity':re.sub(one[0]+'|\\'+one[2],'',m.group()),'start':m.start()+len(one[0])-l1,'end':m.end()-len(one[2])})
					else:
						# entity.append({'entity':re.sub(one[0]+'|'+one[2],'',m.group()),'start':m.start()+len(one[0])-l1,'end':m.end()-len(one[2])+l2})
						entity.append({'entity':re.sub(one[0]+'|'+one[2],'',m.group()),
									'start':m.start()+len(re.sub(one[1]+one[2],'',m.group())),
									'end':m.end()-len(re.sub(one[0]+one[1],'',m.group()))})

	def struct_search_without(self,line,entity,search_without):
		zhuanyi=['*','d']
		for one in search_without:
			if one[0] in zhuanyi:
				if one[2] in zhuanyi:
					rule='\\' + one[0] + one[1] + '\\' + one[2]
				else:
					rule='\\' + one[0] + one[1] + one[2]
			else:
				if one[2] in zhuanyi:
					rule= one[0] + one[1] + '\\' + one[2]
				else:
					rule= one[0] + one[1] + one[2]
			data_temp=line
			for m in re.finditer(rule,line):
				data_temp=data_temp.replace(m.group(),'￥'*len(m.group()))
			for m in re.finditer(one[1],data_temp):
				entity.append({'entity':m.group(),'start':m.start(),'end':m.end()})

	def struct_search_region(self,line,entity,search_region):
		for one in search_region:
			for e0 in re.finditer(one[1],line):
				entity_t=[]
				one[4]+=('。',)#,',','，'
				if one[0]!='':
					region_data=line[max(e0.start()-one[3],0):e0.start()]
					for e1 in re.finditer(one[0],region_data):
						e1_region_data=region_data[e1.end():]
						sn=0
						for s in one[4]:
							if s in e1_region_data:
								sn=1
								break
						if sn==0:
							r_len=len(region_data)
							entity_t.append({'entity':e1.group(),'start':e0.start()-r_len+e1.start(),'end':e0.start()-r_len+e1.end()})
				if one[2]!='':
					region_data=line[e0.end():min(e0.end()+one[3],len(line))]
					for e1 in re.finditer(one[2],region_data):
						e1_region_data=region_data[:e1.start()]
						sn=0
						for s in one[4]:
							if s in e1_region_data:
								sn=1
								break
						if sn==0:
							r_len=len(region_data)
							entity_t.append({'entity':e1.group(),'start':e0.end()+e1.start(),'end':e0.end()+e1.end()})
				if entity_t!=[]:
					entity_t.append({'entity':e0.group(),'start':e0.start(),'end':e0.end()})
					entity.extend(entity_t)

class Struct_data(object):
	def __init__(self, data,data_replace,extract_rule,computer_rule):
		# super(Struct_data, self).__init__(*args))
		self.data=data
		self.data_replace=data_replace
		self.extract_rule=extract_rule
		self.computer_rule=computer_rule

	def main(self):
		result=[]
		for line in self.data:
			if self.data_replace!={}:
				for k,v in self.data_replace.items():
					line=line.replace(k,v)
			entity_result={}
			for entity_k,extract_rule_v in self.extract_rule.items():
				if extract_rule_v['search_with']==[["","",""]] \
					and extract_rule_v['search_without']==[["","",""]] \
					and extract_rule_v['search_region']==[["","","",0]]:
					continue
				e=Extract(line,extract_rule_v)
				entity=e.main()
				if entity!=[]:
					entity_result[entity_k]= entity
			# if entity_result!={}:
			# 1_字段抽取数据累加
			if self.computer_rule['content_sum'] != {}:
				self.content_sum(entity_result,self.computer_rule['content_sum'])
			# 2_字段抽取数据判断
			if self.computer_rule['if_content'] != {}:
				self.if_content(entity_result,self.computer_rule['if_content'])
			# 3_字段抽取数据判断累加再判断
			if self.computer_rule['if_content_sum_if'] != []:
				self.if_content_sum_if(entity_result,self.computer_rule['if_content_sum_if'])
			# 4_字段互斥、字段互为否定
			if self.computer_rule['if_no_exist_entity'] != {}:
				self.if_no_exist_entity(entity_result,self.computer_rule['if_no_exist_entity'])
			# 5_字段累加判断
			if self.computer_rule['if_entity_sum_if'] != []:
				self.if_entity_sum_if(entity_result,self.computer_rule['if_entity_sum_if'])
			# 6_一些字段共现，另一些字段互斥
			if self.computer_rule['exist_and_not_exist'] != {}:
				self.exist_and_not_exist(entity_result,self.computer_rule['exist_and_not_exist'])
			result.append({'data':line,'result':entity_result})
		return result

	# 1_字段抽取数据累加
	def content_sum(self,entity_result,content_sum):
		sum_dict={}
		for one in content_sum.keys():
			sum_dict[one]=0
		for k in entity_result:
			for one,k_list in content_sum.items():
				if k in k_list:
					for v in entity_result[k]:
						if '.' in v['entity']:
							sum_dict[one]+=float(v['entity'])
						else:
							sum_dict[one]+=int(v['entity'])
		for one,v in sum_dict.items():
			entity_result[one]=[{'entity':str(v),'start':0,'end':0}]

	# 2_字段抽取数据判断
	def if_content(self,entity_result,if_content):
		for k,v in if_content.items():
			if v[0] in entity_result:
				# 1 小于
				if v[1]=='' and v[2]=='' and v[3]!='':
					for one in entity_result[v[0]]:
						if float(one['entity'])<float(v[3]):
							if k in entity_result:
								entity_result[k].append({'entity':one['entity'],'start':0,'end':0})
							else:
								entity_result[k]=[{'entity':one['entity'],'start':0,'end':0}]
				# 2 小于 等于
				elif v[1]=='' and v[2]!='' and v[3]!='':
					for one in entity_result[v[0]]:
						if float(one['entity'])==float(v[2]) or float(one['entity'])<float(v[3]):
							if k in entity_result:
								entity_result[k].append({'entity':one['entity'],'start':0,'end':0})
							else:
								entity_result[k]=[{'entity':one['entity'],'start':0,'end':0}]
				elif v[1]!='' and v[2]!='' and v[3]!='':
					# 3 大于等于 小于 [ )
					if float(v[1])==float(v[2]):
						for one in entity_result[v[0]]:
							if float(v[1])<=float(one['entity']) and float(one['entity'])<float(v[3]):
								if k in entity_result:
									entity_result[k].append({'entity':one['entity'],'start':0,'end':0})
								else:
									entity_result[k]=[{'entity':one['entity'],'start':0,'end':0}]
					# 4 大于 小于等于 ( ]
					elif float(v[2])==float(v[3]):
						for one in entity_result[v[0]]:
							if float(v[2])<float(one['entity']) and float(one['entity'])<=float(v[3]):
								if k in entity_result:
									entity_result[k].append({'entity':one['entity'],'start':0,'end':0})
								else:
									entity_result[k]=[{'entity':one['entity'],'start':0,'end':0}]
				# 5 大于等于
				elif v[1]!='' and v[2]!='' and v[3]=='':
					for one in entity_result[v[0]]:
						if float(v[1])<float(one['entity']) or float(one['entity'])==float(v[2]):
							if k in entity_result:
								entity_result[k].append({'entity':one['entity'],'start':0,'end':0})
							else:
								entity_result[k]=[{'entity':one['entity'],'start':0,'end':0}]
				# 6 大于
				elif v[1]!='' and v[2]=='' and v[3]=='':
					for one in entity_result[v[0]]:
						if float(v[1])<float(one['entity']):
							if k in entity_result:
								entity_result[k].append({'entity':one['entity'],'start':0,'end':0})
							else:
								entity_result[k]=[{'entity':one['entity'],'start':0,'end':0}]
				# 7 大于 小于
				elif v[1]!='' and v[2]=='' and v[3]!='':
					for one in entity_result[v[0]]:
						if float(v[1])<float(one['entity']) and float(one['entity'])<float(v[3]):
							if k in entity_result:
								entity_result[k].append({'entity':one['entity'],'start':0,'end':0})
							else:
								entity_result[k]=[{'entity':one['entity'],'start':0,'end':0}]
				# 7 等
				elif v[1]=='' and v[2]!='' and v[3]=='':
					for one in entity_result[v[0]]:
						if float(v[2])==float(one['entity']):
							if k in entity_result:
								entity_result[k].append({'entity':one['entity'],'start':0,'end':0})
							else:
								entity_result[k]=[{'entity':one['entity'],'start':0,'end':0}]

	# 3_字段抽取数据判断累加再判断
	def if_content_sum_if(self,entity_result,if_content_sum_if):
		for one in if_content_sum_if:
			one1=one['in_entity']
			one2=one['if_content']
			one3=one['if_out_entity']
			t=0
			# 1 大于
			if one2[0]!='' and one2[1]=='' and one2[2]=='':
				for k,v in entity_result.items():
					if k in one1:
						for v1 in v:
							if float(one2[0])<float(v1['entity']):
								if '.' in v1['entity']:
									t+=float(v1['entity'])
								else:
									t+=int(v1['entity'])
			# 2 大于 等于
			elif one2[0]!='' and one2[1]!='' and one2[2]=='':
				for k,v in entity_result:
					if k in one1:
						for v1 in v:
							if float(one2[0])<float(v1['entity']) or float(v1['entity'])==float(one2[1]):
								if '.' in v1['entity']:
									t+=float(v1['entity'])
								else:
									t+=int(v1['entity'])
			elif one2[0]!='' and one2[1]!='' and one2[2]!='':
				# 3 大于等于 小于 [ )
				if one2[0]==one2[1]:
					for k,v in entity_result:
						if k in one1:
							for v1 in v:
								if float(one2[0])<=float(v1['entity']) and float(v1['entity'])<float(one2[2]):
									if '.' in v1['entity']:
										t+=float(v1['entity'])
									else:
										t+=int(v1['entity'])
				# 4 大于 小于等于 ( ]
				elif one2[1]==one2[2]:
					for k,v in entity_result:
						if k in one1:
							for v1 in v:
								if float(one2[0])<float(v1['entity']) and float(v1['entity'])<=float(one2[2]):
									if '.' in v1['entity']:
										t+=float(v1['entity'])
									else:
										t+=int(v1['entity'])
			# 5 小于 等于
			elif one2[0]=='' and one2[1]!='' and one2[2]!='':
				for k,v in entity_result:
					if k in one1:
						for v1 in v:
							if float(one2[1])==float(v1['entity']) or float(v1['entity'])<float(one2[2]):
								if '.' in v1['entity']:
									t+=float(v1['entity'])
								else:
									t+=int(v1['entity'])
			# 6 大于 小于
			elif one2[0]!='' and one2[1]=='' and one2[2]!='':
				for k,v in entity_result:
					if k in one1:
						for v1 in v:
							if float(one2[0])<float(v1['entity']) and float(v1['entity'])<float(one2[2]):
								if '.' in v1['entity']:
									t+=float(v1['entity'])
								else:
									t+=int(v1['entity'])
			# 7 小于
			elif one2[0]=='' and one2[1]=='' and one2[2]!='':
				for k,v in entity_result:
					if k in one1:
						for v1 in v:
							if float(v1['entity'])<float(one2[2]):
								if '.' in v1['entity']:
									t+=float(v1['entity'])
								else:
									t+=int(v1['entity'])
			# 8 等于
			elif one2[0]=='' and one2[1]!='' and one2[2]=='':
				for k,v in entity_result:
					if k in one1:
						for v1 in v:
							if float(v1['entity'])==float(one2[1]):
								if '.' in v1['entity']:
									t+=float(v1['entity'])
								else:
									t+=int(v1['entity'])
			for o3 in one3:
				# 1 大于
				if o3[1]!='' and o3[2]=='' and o3[3]=='':
					if float(o3[1])<t:
						entity_result[o3[1]]=[{'entity':str(t),'start':0,'end':0}]
				# 2 大于等于
				elif o3[1]!='' and o3[2]!='' and o3[3]=='':
					if float(o3[1])<t or t==float(o3[2]):
						entity_result[o3[1]]=[{'entity':str(t),'start':0,'end':0}]
				elif o3[1]!='' and o3[2]!='' and o3[3]!='':
					# 3 大于等于 小于 [ )
					if o3[1]==o3[2]:
						if float(o3[1])<=t and t<float(o3[2]):
							entity_result[o3[1]]=[{'entity':str(t),'start':0,'end':0}]
					# 4 大于 小于等于 ( ]
					elif o3[2]==o3[3]:
						if float(o3[1])<t and t<=float(o3[3]):
							entity_result[o3[1]]=[{'entity':str(t),'start':0,'end':0}]
				# 5 小于 等于
				elif o3[1]=='' and o3[2]!='' and o3[3]!='':
					if float(o3[2])==t or t<float(o3[3]):
						entity_result[o3[1]]=[{'entity':str(t),'start':0,'end':0}]
				# 6 小于
				elif o3[1]=='' and o3[2]=='' and o3[3]!='':
					if t<float(o3[3]):
						entity_result[o3[1]]=[{'entity':str(t),'start':0,'end':0}]
				# 7 大于 小于
				elif o3[1]!='' and o3[2]=='' and o3[3]!='':
					if float(o3[1])<t and t<float(o3[3]):
						entity_result[o3[1]]=[{'entity':str(t),'start':0,'end':0}]
				# 8 等于
				elif o3[1]=='' and o3[2]!='' and o3[3]=='':
					if t==float(o3[2]):
						entity_result[o3[1]]=[{'entity':str(t),'start':0,'end':0}]

	# 4_字段互斥、字段互为否定
	def if_no_exist_entity(self,entity_result,if_no_exist_entity):
		for one,one_list in if_no_exist_entity.items():
			t=0
			for k in one_list:
				if k in entity_result:
					t=1
			if t==0:
				entity_result[one]=[{'entity':'true','start':0,'end':0}]

	# 5_字段累加判断
	def if_entity_sum_if(self,entity_result,if_entity_sum_if):
		for one in if_entity_sum_if:
			t=0
			for k in one['in_entity']:
				if k in entity_result:
					t+=1
			for v in one['if_out_entity']:
				# 1 大于 (
				if v[1]!='' and v[2]=='' and v[3]=='':
					if float(v[1])<t:
						entity_result[v[0]]=[{'entity':'true','start':0,'end':0}]
				# 2 大于等于 [
				elif v[1]!='' and v[2]!='' and v[3]=='':
					if float(v[1])<t or float(v[2])==t:
						entity_result[v[0]]=[{'entity':'true','start':0,'end':0}]
				elif v[1]!='' and v[2]!='' and v[3]!='':
					# 3 大于等于 小于 [ )
					if v[1]==v[2]:
						if float(v[1])<=t and t<float(v[3]):
							entity_result[v[0]]=[{'entity':'true','start':0,'end':0}]
					# 4 大于 小于等于 ( ]
					elif v[2]==v[3]:
						if float(v[1])<t and t<=float(v[3]):
							entity_result[v[0]]=[{'entity':'true','start':0,'end':0}]
				# 5 小于等于 ]
				elif v[1]=='' and v[2]!='' and v[3]!='':
					if t==float(v[2]) or t<float(v[3]):
						entity_result[v[0]]=[{'entity':'true','start':0,'end':0}]
				# 6 大于 小于 ( )
				elif v[1]!='' and v[2]=='' and v[3]!='':
					if float(v[1])<t and t<float(v[3]):
						entity_result[v[0]]=[{'entity':'true','start':0,'end':0}]
				# 7 小于 )
				elif v[1]=='' and v[2]=='' and v[3]!='':
					if t<float(v[2]):
						entity_result[v[0]]=[{'entity':'true','start':0,'end':0}]
				# 8 等于 =
				elif v[1]=='' and v[2]!='' and v[3]=='':
					if t==float(v[2]):
						entity_result[v[0]]=[{'entity':'true','start':0,'end':0}]

	# 6_一些字段共现，另一些字段互斥
	def exist_and_not_exist(self,entity_result,exist_and_not_exist):
		for one,one_dict in exist_and_not_exist.items():
			t=0
			for k in one_dict['exist_entity']:
				if k not in entity_result:
					t=1
			for k in one_dict['not_exist']:
				if k in entity_result:
					k=1
			if k==0:
				entity_result[one]=[{'entity':'true','start':0,'end':0}]

def excel_data():
	# for line in self.data:

	data=xlrd.open_workbook('d1_胃病/胃组织病理报告文本.xlsx')
	sheet=data.sheet_by_name('cdr_V_OTHERREPORT')
	rows=sheet.nrows
	print(rows)
	data_one='检查结论'
	data_dict={'检查部位':0,'检查所见':1,'检查结论':2}
	data_out=open('d1_胃病/胃组织病理报告文本_'+data_one+'.txt','w',encoding='utf-8')
	data=[]
	for r in range(rows):
		if r==0:
			continue
		line=sheet.cell_value(r,data_dict[data_one])
		data.append(line)
	s=Struct_data(data,data_process_dict,extract_rule_dict,computer_rule_dict)
	result=s.main()
	r=0
	for one in result:
		r+=1
		if one['result']!={}:
			print('第{}条数据：\n{}'.format(r,one['data']))
			# print(json.dumps(one['entity'], ensure_ascii=False, indent=4, sort_keys=False))
			data_out.write('第{}条数据：\n{}'.format(r,one['data']))
			data_out.write(json.dumps(one['result'], ensure_ascii=False, indent=4, sort_keys=False))

if __name__ == '__main__':
	# s=Struct_data([],data_replace_dict,entity_dict,[])
	# s.main()
	# excel_data()

	data=xlrd.open_workbook('d1_胃病/胃组织病理报告文本.xlsx')
	sheet=data.sheet_by_name('cdr_V_OTHERREPORT')
	rows=sheet.nrows
	print(rows)
	data_one='检查结论'
	data_dict={'检查部位':0,'检查所见':1,'检查结论':2}
	data_out=open('d1_胃病/胃组织病理报告文本_'+data_one+'.txt','w',encoding='utf-8')
	data=[]
	for r in range(rows):
		if r==0:
			continue
		line=sheet.cell_value(r,data_dict[data_one])
		data.append(line)
	s=Struct_data(data,data_process_dict,extract_rule_dict,computer_rule_dict)
	result=s.main()
	r=0
	for one in result:
		r+=1
		if one['result']!={}:
			print('第{}条数据：\n{}'.format(r,one['data']))
			# print(json.dumps(one['entity'], ensure_ascii=False, indent=4, sort_keys=False))
			data_out.write('第{}条数据：\n{}'.format(r,one['data']))
			data_out.write(json.dumps(one['result'], ensure_ascii=False, indent=4, sort_keys=False))
