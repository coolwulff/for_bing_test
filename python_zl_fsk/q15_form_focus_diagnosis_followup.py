# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 18:02:05 2022

@author: LuPengFei
"""

'''
form_focus_diagnosis_followup
解决门诊号不唯一问题：增加encounter_id
展示层逻辑：若有就诊时间时期则展示，若无则展示挂号时间
'''

import numpy as np
import pandas as pd
import datetime
    

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def get_temp_data():
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    #sql_temp = "select * from form_focus_diagnosis_followup_temp where primary_diagnosis is not null and primary_diagnosis_code is not null;"
    #sql_temp = "select * from form_focus_diagnosis_followup_temp where visit_deptcode in ('22360002','B1110WM01','32360112','B1110EM01','32360112','12360002');"
    sql_temp = '''
select 
a.* 
from form_focus_diagnosis_followup_temp a
join qs_drz_patient b
on a.empi = b.empi and a.patient_no = b.patient_no
where STR_TO_DATE(a.registrationdatetime, '%Y-%m-%d')  > DATE_FORMAT(b.in_hospital_datetime, '%Y-%m-%d')
and visit_deptcode in ('22360002','B1110WM01','32360112','B1110EM01','32360112','12360002');
'''
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
    
   
# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    
    
    # 筛选科室
    visit_dept_code_list = []
    # empi\outpatient_number\ encounter_id \ primary_diagnosis_code\primary_diagnosis
    zd = ['empi', 'outpatient_number','encounter_id','primary_diagnosis_code','primary_diagnosis']
    da = da.drop_duplicates(subset=zd,keep='first')   
    da = da.reset_index(drop=True) 
    
    return da

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    df_curr = get_current_data()
    
    #找差集
    zd = ['empi', 'outpatient_number','encounter_id','primary_diagnosis_code','primary_diagnosis']
    df_temp_0 = df_temp[zd]
    df_curr_0 = df_curr[zd]
    #df_curr_0['patient_num'] = [i[9:] for i in df_curr_0['patient_num']]


    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df1 = df_temp_0.append(df_curr_0)
    df1['encounter_id'] = df1.encounter_id.astype(str) 
    df1['outpatient_number'] = df1.outpatient_number.astype(str) 

    
    df1 = df1.drop_duplicates(subset=zd,keep=False)
    df1 = df1[df1['id0']<n0]
        
    idx = df1.index.tolist()
    
    n0 = len(df_temp.columns.tolist())
    a0 = [i for i in range(n0)]
    res = df_temp.iloc[idx,a0]
    res = res.reset_index(drop=True)
        
    return res

def generate_input(data):
    '''
    生成插入数据
    param:
    data:dataframe, 经过后处理的数据

empi
patient_no
patient_name
outpatient_number
visit_date
visit_time
category_name
primary_diagnosis
primary_diagnosis_code
create_date
update_date
last_update_date
hospital_code
delete_flag
    '''
    
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
      
    for i in range(len(data)):
        
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        patient_name = data['patient_name'][i]       
        outpatient_number = data['outpatient_number'][i]
        encounter_id = data['encounter_id'][i]        
        registration_datetime  = data['registrationdatetime'][i]
        visit_datetime   = data['visitdatetime'][i]
        category_name = data['category_name'][i]
        primary_diagnosis = data['primary_diagnosis'][i]
        primary_diagnosis_code = data['primary_diagnosis_code'][i]
        hospital_code = '42502657200'
        create_date =   time_str  
        delete_flag = 0
        visit_deptname = data['visit_deptname'][i]
        visit_deptcode = data['visit_deptcode'][i]
        type_ = 0
        
        tp = ( empi,
                patient_no,
                patient_name,      
                outpatient_number,
                encounter_id ,
                registration_datetime,
                visit_datetime,
                category_name,
                primary_diagnosis,
                primary_diagnosis_code,
                hospital_code,
                create_date, 
                delete_flag,
                visit_deptname,
                visit_deptcode,
                type_)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_focus_diagnosis_followup(
                empi,
                patient_no,
                patient_name,      
                outpatient_number,
                encounter_id ,
                registration_datetime,
                visit_date,
                category_name,
                primary_diagnosis,
                primary_diagnosis_code,
                hospital_code,
                create_date, 
                delete_flag,
                visit_deptname,
                visit_deptcode,
                type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
    truncate table form_focus_diagnosis_followup_temp;
    '''
    return sql_create, sql_clear


def insert_data2mysql_15(is_clear_temp = False): 
    
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
#    a = compare_data()
    a,b = insert_data2mysql_15()