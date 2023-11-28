# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 13:11:28 2022

@author: LuPengFei
"""

'''
form_outcome

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
    sql_temp = "select * from form_qs_zg_temp;"
    df_temp = mysql.get_sql2df(sql_temp)
    
    return df_temp

from helper import trans_sql_add_condition
def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from form_outcome where hospital_code = '42502657200';"
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
    
   
# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    

    zd = ['empi', 'patient_no','inpatient_number']
    da = da.drop_duplicates(subset=zd,keep='first')   
    da = da.reset_index(drop=True) 
    
    return da

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    df_curr = get_current_data()
    
    #找差集
    zd = ['patient_no','inpatient_number']
    df_temp_0 = df_temp[zd]
    df_curr_0 = df_curr[zd]


    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df1 = df_temp_0.append(df_curr_0)
    df1['patient_no'] = df1.patient_no.astype(str) 
    df1['inpatient_number'] = df1.inpatient_number.astype(str) 
    
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

    empi, 
    patient_no,
    encounter_id, 
    inpatient_number,
    in_hospital_datetime,
    out_hospital_datetime,
    operate_name,
    operate_code,
    operation_dept_name,
    operate_doctor_name,
    operate_date,
    anesthesia_way_name,
    anesthesia_doctor_name,
    preoperation_diagnose_name,    
    preoperation_diagnose_code,
    hospital_code,
    create_date,     
    delete_flag
    '''
    def process_outhospital_result(val):
        
        return int(val)
        
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
      
    for i in range(len(data)):
        
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        inpatient_number = data['inpatient_number'][i]
        outpatient_number = data['outpatient_number'][i]
        inhospital_time = data['inhospital_time'][i]
        outhospital_time = data['outhospital_time'][i]        
        outhospital_result = data['outhospital_result'][i]
        outhospital_result = process_outhospital_result(outhospital_result)
        hospital_code = data['hospital_code'][i]
        create_date =   time_str  
        delete_flag = data['delete_flag'][i]
        
        tp = (  empi, 
                patient_no,
                inpatient_number,
                outpatient_number,
                inhospital_time,
                outhospital_time,
                outhospital_result,
                hospital_code,
                create_date,     
                delete_flag)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_outcome(
                empi, 
                patient_no,
                inpatient_number,
                outpatient_number,
                inhospital_time,
                outhospital_time,
                outhospital_result,
                hospital_code,
                create_date,     
                delete_flag) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
    truncate table form_qs_zg_temp;
    '''
    return sql_create, sql_clear

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def insert_data2mysql_4_2(is_clear_temp = False): 
    
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
    a,b = insert_data2mysql_4_2()