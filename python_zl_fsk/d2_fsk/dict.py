data_process_dict={
	'&lt;':'<',
	'&gt;':'>',
	'&apos;':"'",
	'&quot;':'\"',
	',':'，',
	'(':'（',
	')':'）',
	':':'：',
	' ':'',
	}

computer_rule_dict={
	# 1_字段抽取数据累加
	"content_sum":{},
	# 2_字段抽取数据判断
	"if_content":{},
	# 3_字段抽取数据判断累加再判断
	"if_content_sum_if":[],
	# 4_字段互斥、字段互为否定
	"if_no_exist_entity":{},
	# 5_字段累加判断
	"if_entity_sum_if":[],
	# 6_一些字段共现，另一些字段互斥
	"exist_and_not_exist":{},
}

# 1 超声检查
extract_rule_1_csjc_jcsj={
	"101_检查时间": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"102_检查所见": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"104_是否肝肿大_是": {
		"replace_words": {},
		"search_with": [["","肝脏?肿大",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"106_胆囊描述": {
		"replace_words": {},
		"search_with": [["","胆囊：.+","。胰腺："],
						["","【胆囊】.+","。【.+】"],
						["","【胆囊：】.+","。【.+：】"],
						["","胆----.+","。胰----"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"107_胰腺描述": {
		"replace_words": {},
		"search_with": [["","胰腺：[^：.]+","。脾脏："],
						["","【胰腺】.+","。【.+】"],
						["","【胰腺：】.+","。【.+：】"],
						["","胰----.+","。.+----"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"109_脾脏长径": {
		"replace_words": {},
		"search_with": [["脾门厚[\d\.]*mm，长径","[\d\.]*","mm"],
                      ["脾门厚约[\d\.]*mm，长径","[\d\.]*","mm"],
                      ["脾门厚[\d\.]*mm，长径约","[\d\.]*","mm"],
                      ["脾门厚约[\d\.]*mm，长径约","[\d\.]*","mm"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"110_脾脏厚径": {
		"replace_words": {},
		"search_with": [["脾门厚","[\d\.]*","mm"],
                      ["脾门厚约","[\d\.]*","mm"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"111_脾脏描述": {
		"replace_words": {},
		"search_with": [["","脾脏：[^：.]+","。后腹膜淋巴结："],
						["","脾脏：[^：.]+","。肾脏："],
						["","【脾脏】.+","。【.+】"],
						["","【脾脏：】.+","。【.+：】"],
						["","脾----.+","。.+----"]],
		"search_without": [["","脾----.+","。.+----"]],
		"search_region": [["","","",0,()]],
	},
	"112_左肾大小_长": {
		"replace_words": {},
		"search_with": [["左肾","[\d\.]*","mm"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"112_左肾大小_宽": {
		"replace_words": {},
		"search_with": [["左肾[\d\.]*mm×","[\d\.]*","mm"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"112_左肾大小_单位": {
		"replace_words": {},
		"search_with": [["左肾[\d\.]*mm×[\d\.]*","mm",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"113_右肾大小_长": {
		"replace_words": {},
		"search_with": [["右肾","[\d\.]*","mm"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"113_右肾大小_宽": {
		"replace_words": {},
		"search_with": [["右肾[\d\.]*mm×","[\d\.]*","mm"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"113_右肾大小_单位": {
		"replace_words": {},
		"search_with": [["右肾[\d\.]*mm×[\d\.]*","mm",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"114_肾脏形态": {
		"replace_words": {},
		"search_with": [["","左、?右肾大小形态正常",""],
						["","双肾大小形态正常",""],
						["","左肾大小形态正常",""]],
		"search_without": [["左、?","右肾大小形态正常",""]],
		"search_region": [["","","",0,()]],
	},
	"115_肾实质回声": {
		"replace_words": {},
		"search_with": [["","肾脏?实质回声正常",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"117_淋巴结大小": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","淋巴结","大小约[\d\*x]*mm",15,()]],
	},
	"118_甲状腺描述": {
		"replace_words": {},
		"search_with": [["","甲状腺：[^：.]+","。甲状旁腺："],
						["","【甲状腺】.+","。【.+】"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
}

computer_rule_1_csjc_jcsj={
	# 1_字段抽取数据累加
	"content_sum":{},
	# 2_字段抽取数据判断
	"if_content":{},
	# 3_字段抽取数据判断累加再判断
	"if_content_sum_if":[],
	# 4_字段互斥、字段互为否定
	"if_no_exist_entity":{
		"104_是否肝肿大_否":["104_是否肝肿大_是"],
	},
	# 5_字段累加判断
	"if_entity_sum_if":[],
	# 6_一些字段共现，另一些字段互斥
	"exist_and_not_exist":{},
}

extract_rule_1_csjc={
	"103_检查结论": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"105_肝脏描述_肝脂肪浸润": {
		"replace_words": {},
		"search_with": [["","肝脏?脂肪浸润",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"105_肝脏描述_脂肪肝": {
		"replace_words": {},
		"search_with": [["","脂肪肝",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"105_肝脏描述_肝硬化": {
		"replace_words": {},
		"search_with": [["","肝硬化",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"105_肝脏描述_其他": {
		"replace_words": {},
		"search_with": [["","肝多发囊肿",""],["","肝内钙化灶",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"108_是否脾肿大_是": {
		"replace_words": {},
		"search_with": [["","脾脏?肿大",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 没数据
	"116_淋巴结肿大区域_颌下": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 没数据
	"116_淋巴结肿大区域_颏下": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 没数据
	"116_淋巴结肿大区域_颈部": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"116_淋巴结肿大区域_锁骨上": {
		"replace_words": {},
		"search_with": [["","锁骨上淋巴结肿大",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"116_淋巴结肿大区域_腹股沟": {
		"replace_words": {},
		"search_with": [["","腹股沟见淋巴结",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
}

computer_rule_1_csjc={
	# 1_字段抽取数据累加
	"content_sum":{},
	# 2_字段抽取数据判断
	"if_content":{},
	# 3_字段抽取数据判断累加再判断
	"if_content_sum_if":[],
	# 4_字段互斥、字段互为否定
	"if_no_exist_entity":{
		"108_是否脾肿大_否":["108_是否脾肿大_是"],
	},
	# 5_字段累加判断
	"if_entity_sum_if":[],
	# 6_一些字段共现，另一些字段互斥
	"exist_and_not_exist":{},
}

# 2 心电图
extract_rule_2_xdt_jcsj={
	"104_心率（次/分）": {
		"replace_words": {},
		"search_with": [["心率：","[\d]*","bpm"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"105_矫正QT（QTc）期间（ms）": {
		"replace_words": {},
		"search_with": [["QT/QTc：","[\d/]*","ms"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
}

extract_rule_2_xdt={
	"101_检查时间": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"102_检查所见": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"103_检查结论": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"106_ST": {
		"replace_words": {},
		"search_with": [["(\d、)","ST.+","(\d、)"]],
		"search_without": [["(\d、)","ST[^$]+","(\d、)"]],
		"search_region": [["","","",0,()]],
	},
	"107_异常心律": {
		"replace_words": {},
		"search_with": [["(\d、)",".*异常.*","(\d、)"]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"108_心电图提示_正常": {
		"replace_words": {},
		"search_with": [["","窦性心律",""],["","正常心电图",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"108_心电图提示_心律失常": {
		"replace_words": {},
		"search_with": [["","窦性心动过速",""],
						["","心房颤动",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 无数据
	"108_心电图提示_心肌缺血": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"108_心电图提示_心室/房肥大": {
		"replace_words": {},
		"search_with": [["提示","[左|右]心室肥大",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
}

# 3 胸部CT
extract_rule_3_xbct={
	"101_检查时间": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"102_检查所见": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"103_检查结论": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 依赖下面字段判断
	"104_是否有淋巴结肿大_是": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 依赖下面字段判断
	"104_是否有淋巴结肿大_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"104_淋巴结肿大部位_纵膈": {
		"replace_words": {},
		"search_with": [["","纵隔淋巴结肿大",""],
						["","纵隔(内见)?多发稍大淋巴结",""],
						["","纵隔内多发稍大淋巴结",""],
						["","纵隔内?多发小淋巴结",""],
						["","纵隔内见多发小?淋巴结",""],
						["","纵隔(内见)?小淋巴结",""],
						["","纵隔内及双侧腋下多发较大淋巴结",""],
						["","纵隔内及右侧颈根部见肿大淋巴结",""],
						["","纵隔及右侧颈根部多发肿大淋巴结",""],
						["","纵隔内稍肿大淋巴结",""],
						["","纵隔内?(可见)?多发淋巴结",""],
						["","纵隔内可见数枚肿大淋巴结",""],
						["","纵隔内多发淋巴结，部分增大",""],
						["","纵隔淋巴结影增多、稍增大",""],
						["","纵隔区淋巴结稍大",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"104_淋巴结肿大部位_腋窝": {
		"replace_words": {},
		"search_with": [["","腋[下窝]淋巴结肿大",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 无数据
	"104_淋巴结肿大部位_颈部": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"104_淋巴结肿大部位_其他": {
		"replace_words": {},
		"search_with": [["","隆突下淋巴结肿大",""],
						["","肺门可见多发淋巴结影",""],
						["","肺门多发淋巴结",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"105_是否有肺动脉增宽_是": {
		"replace_words": {},
		"search_with": [["","肺动脉主干略?增宽",""],
						["","肺动脉主干略粗",""],
						["","肺动脉干略增粗",""],
						["","肺动脉主干及分支增粗",""],
						["","肺动脉主干较同层主动脉增宽",""],
						["","肺动脉干增粗",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 根据上面字段判断
	"105_是否有肺动脉增宽_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"106_是否有心包积液_是": {
		"replace_words": {},
		"search_with": [["","心包腔?积液",""],
						["","心包少许积液",""],
						["","心包下见少许液体",""],
						["","心包少量积液",""],
						["","心包上隐窝积液",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 无数据
	"106_是否有心包积液_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"107_是否有肺间质病变_是": {
		"replace_words": {},
		"search_with": [["","肺间质性改变",""],
						["","肺间质略增厚",""],
						["","肺间质性炎症",""],
						["","肺间质性水肿",""]],
		"search_without": [["","",""]],
		"search_region": [["","肺","局部轻度间质性改变",25,()]],
	},
	# 根据上面字段判断
	"107_是否有肺间质病变_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"108_是否有肺实质病变_是": {
		"replace_words": {},
		"search_with": [["","肺实质病变",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 根据上面字段判断
	"108_是否有肺实质病变_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"109_是否有胸腔积液_单侧": {
		"replace_words": {},
		"search_with": [["","左侧胸腔积液",""],
						["","左侧胸腔少量积液",""],
						["","右侧少量胸腔积液",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"109_是否有胸腔积液_双侧": {
		"replace_words": {},
		"search_with": [["","两侧少许胸腔积液",""],
						["","两侧胸腔见?积液",""],
						["","两侧少量胸腔积液",""],
						["","两侧胸腔见少量积液",""],
						["","[双两]侧胸腔少量积液",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"109_是否有胸腔积液_否": {
		"replace_words": {},
		"search_with": [["","[双两]侧胸腔未见明显积液",""],
						["","两侧胸腔少量积液已吸收",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"110_是否有胸膜增厚_是": {
		"replace_words": {},
		"search_with": [["","胸膜稍?增厚",""],
						["","胸膜局部增厚",""],
						["","胸膜毛糙增厚",""],
						["","胸膜下局部小叶间隔增厚",""],
						["","胸膜下局部间质增厚",""],
						["","胸膜下小叶间隔稍?增厚",""],
						["","胸膜牵拉增厚",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"110_是否有胸膜增厚_否": {
		"replace_words": {},
		"search_with": [["","[双两]侧胸膜未见明显增厚",""],
						["","两侧胸膜未见异常",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
}

computer_rule_3_xbct={
	# 1_字段抽取数据累加
	"content_sum":{},
	# 2_字段抽取数据判断
	"if_content":{},
	# 3_字段抽取数据判断累加再判断
	"if_content_sum_if":[],
	# 4_字段互斥、字段互为否定
	"if_no_exist_entity":{
		"104_是否有淋巴结肿大_否":["104_淋巴结肿大部位_纵膈","104_淋巴结肿大部位_腋窝",
								"104_淋巴结肿大部位_颈部","104_淋巴结肿大部位_其他"],
		"104_是否有淋巴结肿大_是":["104_是否有淋巴结肿大_否"],
		"105_是否有肺动脉增宽_否":["105_是否有肺动脉增宽_是"],
		"106_是否有心包积液_否":["106_是否有心包积液_是"],
		"107_是否有肺间质病变_否":["107_是否有肺间质病变_是"],
		"108_是否有肺实质病变_否":["108_是否有肺实质病变_是"],
	},
	# 5_字段累加判断
	"if_entity_sum_if":[],
	# 6_一些字段共现，另一些字段互斥
	"exist_and_not_exist":{},
}

# 4 腹部CT
extract_rule_4_fbct={
	"101_检查时间": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"102_检查所见": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"103_检查结论": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 没数据
	"104_肝脏大小_长（cm）": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 没数据
	"104_肝脏大小_宽（cm）": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 没数据
	"105_脾脏大小_长（cm）": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 没数据
	"105_脾脏大小_宽（cm）": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"106_是否有胰腺周围渗出_是": {
		"replace_words": {},
		"search_with": [["","胰腺?周围?渗出",""],
						["","胰周脂肪间隙模糊伴散在渗出",""],
						["","胰腺饱满，边缘轮廓毛糙，周围脂肪间隙模糊，可见渗出",""],
						["","胰腺体部密度不均伴气体影，与邻近肠管分界不清，周围脂肪间隙模糊，可见渗出",""],
						["","胰腺饱满伴密度不均，边缘轮廓毛糙，周围可见明显渗出",""],
						["","胰周脂肪间隙模糊伴少许渗出积液",""],
						["","胰腺体部见金属影，术区见渗出",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 根据上面字段判断
	"106_是否有胰腺周围渗出_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 右肾小结石，右侧输尿管上段小结石伴上游尿路积水扩张   这个是否算？
	"107_是否有肾积水_是": {
		"replace_words": {},
		"search_with": [["","肾(轻度)?积水",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 根据上面字段判断
	"107_是否有肾积水_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 没找到数据
	"108_是否有肠道水肿_是": {
		"replace_words": {},
		"search_with": [["","肠壁(增厚)?水肿",""],
						["","肠壁和膀胱壁见较均匀水肿",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 根据上面字段判断
	"108_是否有肠道水肿_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"109_是否有肠梗阻_是": {
		"replace_words": {},
		"search_with": [["","肠梗阻",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 根据上面字段判断
	"109_是否有肠梗阻_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"110_是否有腹膜后淋巴结_是": {
		"replace_words": {},
		"search_with": [["","后腹膜见?多发淋巴结",""],
						["","后腹膜见?多发小淋巴结",""],
						["","后腹膜、两侧髂血管旁见多发肿大淋巴结",""],
						["","后腹膜区多发淋巴结",""],
						["","后腹膜多发肿大淋巴结",""],
						["","后腹膜淋巴结",""],
						["","后腹膜区?多发转移性?淋巴结",""],
						["","后腹膜可见多发大小不一淋巴结",""],
						["","后腹膜多发大小不一淋巴结",""],
						["","后腹膜似见增大淋巴结",""],
						["","后腹膜可疑淋巴结",""],
						["","后腹膜区?可见多发淋巴",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"110_是否有腹膜后淋巴结_否": {
		"replace_words": {},
		"search_with": [["","后腹膜盆腔未见明显肿大淋巴结",""],
						["","后腹膜及盆腔内未见肿大淋巴结",""],
						["","腹膜后未见明显肿大淋巴结",""],
						["","后腹膜未见增大淋巴结",""],
						["","后腹膜未见明显肿大淋巴结",""],
						["","后腹膜未见明显肿大的淋巴结",""],
						["","后腹膜无明显肿大淋巴结",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 没数据
	"111_是否有腹部血管异常_是": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 没数据
	"111_是否有腹部血管异常_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"111_腹部血管异常描述": {
		"replace_words": {},
		"search_with": [["","腹部肠系膜血管周围多发较小淋巴结",""],
						["","左上腹多发迂曲扩张的血管影",""],
						["","左上腹局段空肠富血管小结节",""],
						["","腹腔内多发侧支小血管",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	"112_是否有腹水_是": {
		"replace_words": {},
		"search_with": [["","腹水",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
	# 根据上面字段判断
	"112_是否有腹水_否": {
		"replace_words": {},
		"search_with": [["","",""]],
		"search_without": [["","",""]],
		"search_region": [["","","",0,()]],
	},
}

computer_rule_4_fbct={
	# 1_字段抽取数据累加
	"content_sum":{},
	# 2_字段抽取数据判断
	"if_content":{},
	# 3_字段抽取数据判断累加再判断
	"if_content_sum_if":[],
	# 4_字段互斥、字段互为否定
	"if_no_exist_entity":{
		"106_是否有胰腺周围渗出_否":["106_是否有胰腺周围渗出_是"],
		"107_是否有肾积水_否":["107_是否有肾积水_是"],
		"108_是否有肠道水肿_否":["108_是否有肠道水肿_是"],
		"109_是否有肠梗阻_否":["109_是否有肠梗阻_是"],
		"111_是否有腹部血管异常_否":["111_腹部血管异常描述"],
		"111_是否有腹部血管异常_是":["111_腹部血管异常描述_否"],
		"112_是否有腹水_否":["112_是否有腹水_是"],
	},
	# 5_字段累加判断
	"if_entity_sum_if":[],
	# 6_一些字段共现，另一些字段互斥
	"exist_and_not_exist":{},
}

# 5 超声心动图
extract_rule_5_csxdt = {
    "118_主动脉瓣描述_1": {
        "replace_words": {},
        "search_with": [["", "主动脉瓣环(显著)?钙化", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "118_主动脉瓣描述_2": {
        "replace_words": {},
        "search_with": [["", "主动脉瓣增厚", ""], ["", "主动脉瓣膜增厚", ""], ["", "主动脉瓣稍增厚", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "118_主动脉瓣描述_3": {
        "replace_words": {},
        "search_with": [["", "", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "主动脉瓣(口)?", "开放(轻度)?受限", 10, ()]],
    },
    "118_主动脉瓣描述_4": {
        "replace_words": {},
        "search_with": [["", "", ""]],
        "search_without": [["未见", "主动脉瓣(轻度)?反流", ""], ["未见", "主动脉瓣反流", ""], ["未见", "主动脉瓣返流", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "118_主动脉瓣描述_5": {
        "replace_words": {},
        "search_with": [["", "", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "主动脉瓣", "关闭时对合不良", 20, ()]],
    },
    # 没数据
    "119_主动脉瓣描述_9": {
        "replace_words": {},
        "search_with": [["", "主动脉瓣", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "120_二尖瓣描述_1": {
        "replace_words": {},
        "search_with": [["", "二尖瓣环(显著)?钙化", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 二尖瓣增厚钙化
    "120_二尖瓣描述_2": {
        "replace_words": {},
        "search_with": [["", "二尖瓣增厚", ""], ["", "二尖瓣稍增厚", ""], ["", "二尖瓣膜增厚", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "120_二尖瓣描述_3": {
        "replace_words": {},
        "search_with": [["", "", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "二尖瓣(口)?", "开放(轻度)?受限", 10, ()]],
    },
    "120_二尖瓣描述_4": {
        "replace_words": {},
        "search_with": [["", "", ""]],
        "search_without": [["未见", "二尖瓣(轻度)?反流", ""], ["未见", "二尖瓣反流", ""], ["未见", "二尖瓣返流", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "120_二尖瓣描述_5": {
        "replace_words": {},
        "search_with": [["", "", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "二尖瓣", "未完成关闭", 30, ()]],
    },
    # 没数据
    "121_二尖瓣描述_9": {
        "replace_words": {},
        "search_with": [["", "二尖瓣", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 无数据
    "122_三尖瓣描述_1": {
        "replace_words": {},
        "search_with": [["", "三尖瓣环(显著)?钙化", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 无数据
    "122_三尖瓣描述_2": {
        "replace_words": {},
        "search_with": [["", "三尖瓣增厚", ""], ["", "三尖瓣膜增厚", ""], ["", "三尖瓣稍增厚", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 无数据
    "122_三尖瓣描述_3": {
        "replace_words": {},
        "search_with": [["", "", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "三尖瓣(口)?", "开放(轻度)?受限", 10, ()]],
    },
    "122_三尖瓣描述_4": {
        "replace_words": {},
        "search_with": [["", "", ""]],
        "search_without": [["未见", "三尖瓣(轻度)?反流", ""], ["未见", "三尖瓣反流", ""], ["未见", "三尖瓣返流", ""]],
        "search_region": [["", "三尖瓣", "微量反流", 10, ()]],
    },
    # 无数据
    "122_三尖瓣描述_5": {
        "replace_words": {},
        "search_with": [["", "三尖瓣关闭不全", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 没数据
    "123_三尖瓣描述_9": {
        "replace_words": {},
        "search_with": [["", "三尖瓣", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "124_三尖瓣跨瓣压差": {
        "replace_words": {},
        "search_with": [["跨瓣压差", "\d+", "mmHg"], ["跨瓣压差", "\d+", "mHg"]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "125_估测肺动脉收缩压": {
        "replace_words": {},
        "search_with": [["肺动脉收缩压为", "\d+", "mmHg"], ["肺动脉收缩压为", "\d+", "mHg"],
                        ["肺动脉收缩压为", "\d+", " mmHg"], ["肺动脉收缩压", "\d+", "mmHg"]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "126_是否肺动脉增宽_1": {
        "replace_words": {},
        "search_with": [["", "肺动脉增宽", ""], ["", "肺动脉稍增宽", ""], ["", "肺动脉增宽为", ""],
                        ["", "肺动脉为增宽", ""], ["", "肺动脉主干(明显)?增宽", ""], ["", "肺动脉增宽达", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "126_是否肺动脉增宽_0": {
        "replace_words": {},
        "search_with": [["", "肺动脉不增宽", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 无数据
    "127_肺动脉瓣描述_1": {
        "replace_words": {},
        "search_with": [["", "肺动脉瓣环(显著)?钙化", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 无数据
    "127_肺动脉瓣描述_2": {
        "replace_words": {},
        "search_with": [["", "肺动脉瓣增厚", ""], ["", "肺动脉瓣稍增厚", ""], ["", "肺动脉瓣膜增厚", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 无数据
    "127_肺动脉瓣描述_3": {
        "replace_words": {},
        "search_with": [["", "", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
        "search_region": [["", "肺动脉瓣(口)?", "开放(轻度)?受限", 10, ()]],
    },
    "127_肺动脉瓣描述_4": {
        "replace_words": {},
        "search_with": [["", "", ""]],
        "search_without": [["未见", "肺动脉瓣(轻度)?反流", ""], ["未见", "肺动脉瓣反流", ""], ["未见", "肺动脉瓣返流", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 无数据
    "127_肺动脉瓣描述_5": {
        "replace_words": {},
        "search_with": [["", "肺动脉瓣关闭不全", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 无数据
    "128_肺动脉瓣描述_9": {
        "replace_words": {},
        "search_with": [["", "肺动脉瓣", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "129_左室舒张功能": {
        "replace_words": {},
        "search_with": [["", "左室舒张功能(中度)?减退", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "130_是否心包积液_1": {
        "replace_words": {},
        "search_with": [["", "心包积液", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    "130_是否心包积液_0": {
        "replace_words": {},
        "search_with": [["", "未见(明显)?心包积液", ""]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
    # 这几个值的最大值？ 5、右室游离壁近心尖处无回声区0.5cm，右室前壁无回声区0.3cm，左室侧壁无回声区0.5cm。
    "131_线性无回声区最大距离": {
        "replace_words": {},
        "search_with": [["线性无回声区", r"[\d\.]*", "cm"]],
        "search_without": [["", "", ""]],
        "search_region": [["", "", "", 0, ()]],
    },
}

computer_rule_5_csxdt={
	# 1_字段抽取数据累加
	"content_sum":{},
	# 2_字段抽取数据判断
	"if_content":{},
	# 3_字段抽取数据判断累加再判断
	"if_content_sum_if":[],
	# 4_字段互斥、字段互为否定
	"if_no_exist_entity":{
		"123_是否肺动脉增宽_否":["123_是否肺动脉增宽_是","123_是否肺动脉增宽_否"],
		"126_是否心包积液_否":["126_是否心包积液_是"],
	},
	# 5_字段累加判断
	"if_entity_sum_if":[],
	# 6_一些字段共现，另一些字段互斥
	"exist_and_not_exist":{},
}
