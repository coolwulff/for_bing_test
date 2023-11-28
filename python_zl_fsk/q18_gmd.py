# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 16:49:09 2022

@author: wdky
"""

import numpy as np
import pandas as pd
import datetime

data = pd.read_excel("风湿骨密度_筛选患者.xlsx")

# 转换日期
def trans_date(val):
    # 将 12/13/2019 转换为 YYYY-MM-DD
    if val:
        return val[6:10] + '-' + val[0:2] + '-' + val[3:5]
    return None

data['SPINE_SCANDATE'] = [trans_date(val) for val in data['SPINE_SCANDATE']]


# 读取风湿数据
from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def get_formbasicinfo_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     #sql_curr = "select * from form_basic_info where hospital_code = '42502657200';"
     sql_curr = '''
SELECT
	a.* 
	,b.in_hospital_datetime as ryrq
	,b.out_hospital_datetime as cyrq
	,b.inpatient_number
FROM
	form_basic_info a
join qs_drz_patient b
on a.empi = b.empi and a.patient_no = b.patient_no
WHERE
	a.hospital_code = '42502657200';
'''
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
 
data_basicinfo = get_formbasicinfo_data()
zd_use = ['empi', 'patient_no', 'encounter_id', 'patient_name','birth', 'ryrq','cyrq','inpatient_number']
data_basicinfo = data_basicinfo[zd_use]

# 姓名、出生日期匹配
#data_basicinfo['SPINE_SCANDATE'] = ''
#data_basicinfo['SPINE_TSCORE'] = ''
#data_basicinfo['HIP_TSCORE'] = ''
#data_basicinfo['HIPNECK_TSCORE'] = ''
#
#for i in range(len(data_basicinfo)):
#    name_ = data_basicinfo.patient_name[i]
#    birth_ = str(data_basicinfo.birth[i])
#    
#    temp0 = data[(data['PATIENT_NAME'] == name_) & (data['csrq'] == birth_)]
#    if len(temp0) == 1:
#        data_basicinfo['SPINE_SCANDATE'][i] = temp0['SPINE_SCANDATE']
#        data_basicinfo['SPINE_TSCORE'][i] = ''
#        data_basicinfo['HIP_TSCORE'][i] = ''
#        data_basicinfo['HIPNECK_TSCORE'][i] = ''
    
data['empi'] = ''
data['patient_no'] = ''
data['encounter_id'] = ''
data['ryrq'] = ''
data['cyrq'] = ''
data['inpatient_number'] = ''
data['is_use'] = 0
data['type'] = 0
data = data.reset_index(drop=True)

data_basicinfo['birth'] = [str(a) for a in data_basicinfo['birth']]
for i in range(len(data)):
    name_ = data['PATIENT_NAME'][i]
    birth_ = str(data['csrq'][i])
    
    temp0 = data_basicinfo[(data_basicinfo['patient_name'] == name_) & (data_basicinfo['birth'] == birth_)]
    if len(temp0) == 1:
        data['empi'][i] = temp0['empi'].values[0]
        data['patient_no'][i] = temp0['patient_no'].values[0]
        data['encounter_id'][i] = temp0['encounter_id'].values[0]
        data['ryrq'][i] = temp0['ryrq'].values[0]
        data['cyrq'][i] = temp0['cyrq'].values[0]
        data['inpatient_number'][i] = temp0['inpatient_number'].values[0]
        data['is_use'][i] = 1
        
        # 判断 SPINE_SCANDATE 大于 ryrq
        strftime1 = datetime.datetime.strptime(str(data['ryrq'][i])[0:10], "%Y-%m-%d")
        strftime2 = datetime.datetime.strptime(data['SPINE_SCANDATE'][i], "%Y-%m-%d") 
        strftime3 = datetime.datetime.strptime(str(data['cyrq'][i])[0:10], "%Y-%m-%d")
        if strftime2 < strftime1:
            data['is_use'][i] = 0
        
        if strftime2 >= strftime1 and strftime3 > strftime2:
            data['type'][i] = 1
            
# 筛选能匹配到的
data2 = data[data['is_use']==1]
data2['hospital_code'] = '42502657200'
data2 = data2.reset_index(drop=True)

