# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 15:59:09 2022

@author: LuPengFei
"""

'''
风湿科：form_diagnose_info_temp

'''
import numpy as np
import pandas as pd
import datetime
    
from fsk_hive_sql_4 import in_hospitaldate_first
from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def get_temp_data():
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
#    sql_temp = '''
#SELECT
#	* 
#FROM
#	form_diagnose_info_51_temp 
#WHERE
#	( diagnose_type = 4 OR diagnose_type = 2 ) 
#	AND isprimary = 1 
#	AND in_hospital_time > '2020-11-30'
#	AND inpatient_number in (select distinct inpatient_number from form_diagnose_info_51_temp where trim(diagnose_code) in ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))
#   AND TRIM(inhospital_dept_name) in ('免疫学专业','日间病房(南)','风湿科(南)','其他业务科室','风湿科（A类）(南)','A类11F病房')
#'''
    sql_temp = '''
SELECT
	a.* 
FROM
	form_diagnose_info_51_temp a
left join qs_drz_patient b
on a.patient_no = b.patient_no and a.empi = b.empi
WHERE
	( a.diagnose_type = 4 OR a.diagnose_type = 2 ) 
	AND a.isprimary = 1 
	AND a.in_hospital_time > '%s'
	AND a.inpatient_number in (select distinct inpatient_number from form_diagnose_info_51_temp where trim(diagnose_code) in ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))
   AND TRIM(a.inhospital_dept_name) in ('免疫学专业','日间病房(南)','风湿科(南)','其他业务科室','风湿科（A类）(南)','A类11F病房')
	 AND b.in_hospital_datetime <= a.in_hospital_time
'''% in_hospitaldate_first
    df_temp = mysql.get_sql2df(sql_temp)
    
    return df_temp


def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from form_focus_diagnosis_followup where hospital_code = '42502657200';"
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
    
def delete_first_inpatientnumber(da):
    # da:hive原始数据
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_admission = "select * from qs_drz_patient;"
     df_admission = mysql.get_sql2df(sql_admission) 
     inp_list = df_admission['inpatient_number'].values.tolist()
     
     # 排除
     da['is_in'] = [a in inp_list for a in da['inpatient_number']]
     da = da[da['is_in']==False]
     da = da.reset_index(drop=True) 
     
     return da


# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    
    
    # 过滤第一次住院
    da = delete_first_inpatientnumber(da)
    
    # 优先保留 diagnose_type = 4，若无则保留 diagnose_type = 2
    da = da.sort_values(by=['empi','patient_no','inpatient_number','diagnose_type'],ascending=[True,True,True,False])
    da = da.reset_index(drop=True)
    

    zd = ['empi', 'patient_no','inpatient_number']
    da = da.drop_duplicates(subset=zd,keep='first')  
    da = da.reset_index(drop=True) 
    
    return da

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    df_curr = get_current_data()
    
    #找差集
    zd = ['empi', 'patient_no','inpatient_number','encounter_id']
    #zd = ['empi', 'inpatient_number','isprimary','diagnose_code']
    df_temp_0 = df_temp[zd]
    df_curr_0 = df_curr[zd]
  

    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df_curr_0["encounter_id"] = [int(i) for i in df_curr_0["encounter_id"]]
    df1 = df_temp_0.append(df_curr_0)
    df1['patient_no'] = df1.patient_no.astype(str) 
    df1['inpatient_number'] = df1.inpatient_number.astype(str) 
    df1['encounter_id'] = df1.encounter_id.astype(str) 

    
    df1 = df1.drop_duplicates(subset=zd,keep=False)
    df1 = df1[df1['id0']<n0]
        
    idx = df1.index.tolist()
    
    n0 = len(df_temp.columns.tolist())
    a0 = [i for i in range(n0)]
    res = df_temp.iloc[idx,a0]
    res = res.reset_index(drop=True)
        
    return res

def generate_input(data):

    
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
      
    for i in range(len(data)):
        
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        patient_name = data['patient_name'][i]       
        inpatient_number = data['inpatient_number'][i]
        encounter_id = data['encounter_id'][i]        
        registration_datetime  = data['in_hospital_time'][i]
        visit_datetime   = None
        category_name = None
        primary_diagnosis = data['diagnose_name'][i]
        primary_diagnosis_code = data['diagnose_code'][i]
        hospital_code = '42502657200'
        create_date =   time_str  
        delete_flag = 0
        type_ = 1
        visit_deptcode = data['inhospital_dept_code'][i]
        visit_deptname = data['inhospital_dept_name'][i]        
        tp = ( empi,
                patient_no,
                patient_name,      
                inpatient_number,
                encounter_id ,
                registration_datetime,
                visit_datetime,
                category_name,
                primary_diagnosis,
                primary_diagnosis_code,
                hospital_code,
                create_date, 
                delete_flag,
                type_,
                visit_deptcode,
                visit_deptname)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_focus_diagnosis_followup(
                empi,
                patient_no,
                patient_name,      
                inpatient_number,
                encounter_id ,
                registration_datetime,
                visit_date,
                category_name,
                primary_diagnosis,
                primary_diagnosis_code,
                hospital_code,
                create_date, 
                delete_flag,
                type,
                visit_deptcode,
                visit_deptname) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    '''
    return sql, d_insert

def generate_check_sql():
    pass

def sql_list():
    
    # 建表
    sql_create = '''
    '''
    #sql_create = sql_create.replace('\n', '')
    # 清空表
    sql_clear = '''
    truncate table form_diagnose_info_51_temp;
    '''
    return sql_create, sql_clear


def insert_data2mysql_3_2(is_clear_temp = False): 
    
    data = compare_data()
    sql, data_sql = generate_input(data=data)
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    
    sql_create, sql_clear = sql_list()    
 
    try:
        mysql.insert_data_many(data_sql,sql)

        # 清空表
        if is_clear_temp:
            mysql = db_pymysql(host=host_56
                                 ,user=user_56
                                 ,password=password_56
                                 ,database=database_56
                                 ,charset='utf8')
            mysql.execute_sql(sql_clear)
        
        return sql, data_sql
    except:
        return sql, data_sql

if __name__ == '__main__':
#    a = get_temp_data()
#    a,b = process_admission_history(df_temp)
#    b = preprocess(a) 
#    a,c = insert_data2mysql_3_2()
#    a = get_current_data()
    c = compare_data()