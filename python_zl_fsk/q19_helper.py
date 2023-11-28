# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 13:59:53 2023

@author: LuPengFei
"""

'''
读取肾活检数据
'''

import numpy as np
import pandas as pd
from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

#data0 = pd.read_excel("20230104_肾活检导入模板.xlsx")
#data0['住院号'] = [str(i) for i in data0['住院号']]

def get_temp_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from entry_renal_biopsy where record_id in (select max(record_id) from entry_renal_biopsy) and deal_statue = 0;"
     df_curr = mysql.get_sql2df(sql_curr)
     
     return df_curr
 
data0 = get_temp_data()


# -- 1 通过住院号，匹配hive中empi
# 生成hivesql，根据住院号匹配其他信息

sql_1 = '''
select 
distinct 
a.patientno as patient_no
,d.empi as empi
,a.patientname as patient_name
,a.encounterid as encounter_id
,a.inpatientnumber as inpatient_number
,a.outpatientnumber as outpatient_number
from cdr_V_MedicalRecordMain a
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) d 
ON a.PatientNo = d.PatientNo 
where a.inpatientnumber in (Replace1) and a.bigdata_data_tag  = 1
'''

replace1 = ''
zyh = data0['inpatient_number'].values.tolist()
for i in zyh:
    replace1 = replace1 + str(i) + ','
replace1 = replace1[0:-1]
sql_1 = sql_1.replace('Replace1',replace1)

# 抽取数据
from fsk_hive_connect import db_hive

dbhive = db_hive()
success,data_hive = dbhive.excute_sql2df(sql_1)

# 关联
data = pd.merge(data0, data_hive, left_on='inpatient_number', right_on='inpatient_number' , how='left', sort=False)

# -- 2 数据转换处理

# (1)狼疮性肾炎病理分型
lcxblfx_values = data['p1_lcxsyblfx'].values.tolist()
lcxblfx_values_u = list(set(lcxblfx_values))

def trans_lcxblfx(val):
    
    # 狼疮性肾炎病理分型

    if val == "I":
        return '11'
    elif val == "II":
        return '12'
    elif val == "III":
        return '13'
    elif val == "IV":
        return '14'
    elif val == "III/IV":
        return '13,14'
    elif val == "V":
        return '15'
    elif val == "VI":
        return '16'
    elif val == "III+V":
        return '17'
    elif val == "V+III":
        return '17'
    elif val == "IV+V":
        return '18'
    elif val == "V+IV":
        return '18'
    elif val == "足细胞病":
        return '19'    
    elif val == "血栓性微血管病":
        return '20'   
    elif val == "其他":
        return '99'    
    elif val == "不详":
        return "NA"  
    else:
        return None

# 毛细血管内细胞增多评分

def trans_mxxgnxbzdpf(val):
    
    if val == '0':
        return 'NA'
    elif val == '1':
        return '1'
    elif val == '2':
        return '2'
    elif val == '3':
        return '3'
    else:
        return None

# 中性粒细胞浸润/核碎裂评分
def trans_zxlxbjrhslpf(val):
    
    if val == '0':
        return 'NA'
    elif val == '1':
        return '1'
    elif val == '2':
        return '2'
    elif val == '3':
        return '3'
    else:
        return None 

# 细胞性和/或纤维细胞性新月体评分
def trans_xbxxwxbxxytpf(val):
    
    if val == '0':
        return 'NA'
    elif val == '2':
        return '1'
    elif val == '4':
        return '2'
    elif val == '6':
        return '3'
    else:
        return None   

# 纤维素样坏死评分
def trans_xwsyhspf(val):
    
    if val == '0':
        return 'NA'
    elif val == '2':
        return '1'
    elif val == '4':
        return '2'
    elif val == '6':
        return '3'
    else:
        return None 

# 内皮下透明物质沉积/透明血栓/铁丝圈评分
def trans_tsqpf(val):

    if val == '0':
        return 'NA'
    elif val == '1':
        return '1'
    elif val == '2':
        return '2'
    elif val == '3':
        return '3'
    else:
        return None    

# 间质炎性细胞浸润评分
def trans_jzyxxbjrpf(val):

    if val == '0':
        return 'NA'
    elif val == '1':
        return '1'
    elif val == '2':
        return '2'
    elif val == '3':
        return '3'
    else:
        return None

#  肾⼩球硬化（球性/节段性硬化）评分
def trans_sqyhpf(val):

    if val == '0':
        return 'NA'
    elif val == '1':
        return '1'
    elif val == '2':
        return '2'
    elif val == '3':
        return '3'
    else:
        return None

# 纤维性新⽉体评分
def trans_xwxxytpf(val):

    if val == '0':
        return 'NA'
    elif val == '1':
        return '1'
    elif val == '2':
        return '2'
    elif val == '3':
        return '3'
    else:
        return None 

# 间质纤维化评分
def trans_jzxwhpf(val):

    if val == '0':
        return 'NA'
    elif val == '1':
        return '1'
    elif val == '2':
        return '2'
    elif val == '3':
        return '3'
    else:
        return None

# 肾⼩管萎缩评分
def trans_sxgwspf(val):

    if val == '0':
        return 'NA'
    elif val == '1':
        return '1'
    elif val == '2':
        return '2'
    elif val == '3':
        return '3'
    else:
        return None 

# 免疫荧光

def trans_myyg(val):
    
    val = str(val)
    res = []
    
    if 'IgG' in val:
        res.append('1')
    if 'IgM' in val:
        res.append('2')
    if 'IgA' in val:
        res.append('3')
    if 'C3' in val:
        res.append('4')
    if 'C1q' in val:
        res.append('5')
    if 'kappa' in val:
        res.append('6')
    if 'lambda' in val:
        res.append('7')
    
    if len(res) == 0:
        return None
    elif len(res) > 0:
        return ",".join(res)

#data['a'] = [trans_myyg(val) for val in data['免疫荧光']]

def trans_time(time_):
    try:
        a = time_.replace('/','-')
        a = a.replace('-1-','-01-')        
        a = a.replace('-2-','-02-')   
        a = a.replace('-3-','-03-')   
        a = a.replace('-4-','-04-')   
        a = a.replace('-5-','-05-')   
        a = a.replace('-6-','-06-')   
        a = a.replace('-7-','-07-')   
        a = a.replace('-8-','-08-')   
        a = a.replace('-9-','-09-')     
        
        if len(a) == 9:
            a = a[0:8] + '0' + a[8]
        return a
    except:
        return None

# 沉积物形态
def trans_p26_cjwxt(val):
    
    if val == '颗粒状':
        return '1'
    elif val == '团块状':
        return '2'
    elif val == '线状':
        return '3'
    elif val == '不详':
        return 'NA'
    else:
        return None

# 沉积物部位
def trans_p27_cjwbw(val):
    
    if val == '系膜区':
        return '1'
    elif val == '毛细血管袢':
        return '2'
    elif val == '混合型':
        return '3'
    elif val == '不详':
        return 'NA'
    else:
        return None

# 沉积物分布
def trans_p28_cjwfb(val):
    
    if val == '弥漫':
        return '1'
    elif val == '弥漫节段':
        return '2'
    elif val == '球性':
        return '3'
    elif val == '局灶节段':
        return '4'
    elif val == '不详':
        return 'NA'
    else:
        return None

# 转换
data['ts_exam_var'] = [trans_time(i) for i in data['ts_exam']]
data['ts_exam'] = [trans_time(i) for i in data['ts_exam']]

data['p1_lcxsyblfx'] = [trans_lcxblfx(i) for i in data['p1_lcxsyblfx']]
data['p6_mxxgnxbzdpf'] = [trans_mxxgnxbzdpf(i) for i in data['p6_mxxgnxbzdpf']]
data['p8_zxlxbjrhslpf'] = [trans_zxlxbjrhslpf(i) for i in data['p8_zxlxbjrhslpf']]
data['p10_xbxhhxwxbxxytpf'] = [trans_xbxxwxbxxytpf(i) for i in data['p10_xbxhhxwxbxxytpf']]
data['p12_xwsyhspf'] = [trans_xwsyhspf(i) for i in data['p12_xwsyhspf']]
data['p14_npxtmwzcjpf'] = [trans_tsqpf(i) for i in data['p14_npxtmwzcjpf']]
data['p16_jzyxxbjrpf'] = [trans_jzyxxbjrpf(i) for i in data['p16_jzyxxbjrpf']]
data['p18_sxqyhpf'] = [trans_sqyhpf(i) for i in data['p18_sxqyhpf']]
data['p20_xwxxytpf'] = [trans_xwxxytpf(i) for i in data['p20_xwxxytpf']]
data['p22_jzxwhpf'] = [trans_jzxwhpf(i) for i in data['p22_jzxwhpf']]
data['p24_sxqwspf'] = [trans_sxgwspf(i) for i in data['p24_sxqwspf']]
data['p25_myyg'] = [trans_myyg(i) for i in data['p25_myyg']]

data['p26_cjwxt'] = [trans_p26_cjwxt(i) for i in data['p26_cjwxt']]
data['p27_cjwbw'] = [trans_p27_cjwbw(i) for i in data['p27_cjwbw']]
data['p28_cjwfb'] = [trans_p28_cjwfb(i) for i in data['p28_cjwfb']]



        
    
    