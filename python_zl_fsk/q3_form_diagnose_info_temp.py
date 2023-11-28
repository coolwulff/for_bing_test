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
    

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def get_temp_data():
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    #sql_temp = "select * from form_diagnose_info_51_temp where diagnose_type = 4;"
    sql_temp_old = '''
select 
a.*
from form_diagnose_info_51_temp a
join qs_drz_patient b
on a.empi = b.empi and a.patient_no = b.patient_no
where STR_TO_DATE(a.in_hospital_time, '%Y-%m-%d')  >= DATE_FORMAT(b.in_hospital_datetime, '%Y-%m-%d') and diagnose_type = 4
'''

    sql_temp = '''
select 
a.*
from form_diagnose_info_51_temp a
join qs_drz_patient b
on a.empi = b.empi and a.patient_no = b.patient_no
where STR_TO_DATE(a.in_hospital_time, '%Y-%m-%d')  >= DATE_FORMAT(b.in_hospital_datetime, '%Y-%m-%d') and (diagnosetypename = '出院诊断')    
'''
    #sql_temp = "select * from form_diagnose_info;"
    df_temp = mysql.get_sql2df(sql_temp)
    
    return df_temp


def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from form_diagnose_info where hospital_code = '42502657200';"
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
    
#def process_admission_history(da):
#    # da:hive原始数据
#     mysql = db_pymysql(host=host_56
#                         ,user=user_56
#                         ,password=password_56
#                         ,database=database_56
#                         ,charset='utf8')
#     sql_admission = "select * from qs_admission_history;"
#     df_admission = mysql.get_sql2df(sql_admission) 
#     df_admission = df_admission[['empi','inpatient_number','admission_num']]
#
#     res = pd.merge(left=da, right=df_admission, how='left', left_on=['empi','inpatient_number'], right_on=['empi','inpatient_number'])
#     del res['inpatient_times']
#     res['inpatient_times'] = res['admission_num']
#     res = res[np.isnan(res['inpatient_times']) == False]
#     res = res.reset_index(drop=True)    
#     
#     return res


def process_first_inpatient(da):
    # da:hive原始数据
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_admission = "select * from qs_drz_patient;"
     df_admission = mysql.get_sql2df(sql_admission) 
     df_admission = df_admission[['empi','inpatient_number']]

     res = pd.merge(left=da, right=df_admission, how='inner', left_on=['empi','inpatient_number'], right_on=['empi','inpatient_number'])
     res = res.reset_index(drop=True)    
     
     return res
     
     
   
# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    
    
    # 筛选第一次住院
    da = process_first_inpatient(da)

    zd = ['empi', 'patient_no','inpatient_number','encounter_id','isprimary','diagnose_code']
    da = da.drop_duplicates(subset=zd,keep='first')  
    da = da.reset_index(drop=True) 
    
    return da

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    df_curr = get_current_data()
    
    #找差集
    zd = ['empi', 'patient_no','inpatient_number','encounter_id','isprimary','diagnose_code']
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
    df1['isprimary'] = df1.isprimary.astype(str)    
    
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
    patient_name,
    age,
    inpatient_number,
    outpatient_number,
    in_hospital_time,
    out_hospital_time, 
    outhospital_dept_name,    
    pay_way,
    die_time,
    is_die,
    inhospital_dept_name,
    inhospital_way,
zgqk,
    inhospital_total_cost,
    inpatient_times,
    isprimary,
    diagnose_code,
    diagnose_name,
    hospital_code,
    create_date
    delete_flag
    
    '''
    
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
      
    for i in range(len(data)):
        
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        encounter_id = data['encounter_id'][i]
        patient_name = data['patient_name'][i]
        age = data['age'][i]
        inpatient_number = data['inpatient_number'][i]
        outpatient_number = data['outpatient_number'][i]
        in_hospital_time = data['in_hospital_time'][i]
        out_hospital_time = data['out_hospital_time'][i]
        outhospital_dept_name = data['outhospital_dept_name'][i]   
        pay_way = data['pay_way'][i]
        die_time = data['die_time'][i]
        is_die = int(float(data['is_die'][i]))
        inhospital_dept_name = data['inhospital_dept_name'][i]
        inhospital_way = data['inhospital_way'][i]
        inhospital_total_cost = data['inhospital_total_cost'][i]
        #inpatient_times = data['inpatient_times'][i]
        inpatient_times = 1
        isprimary = data['isprimary'][i]
        diagnose_code = data['diagnose_code'][i]
        diagnose_name = data['diagnose_name'][i]
        hospital_code = data['hospital_code'][i]
        create_date = time_str
        delete_flag = int(float(data['delete_flag'][i]))
    
        tp = (      empi, 
                    patient_no,
                    encounter_id,
                    patient_name,
                    age,
                    inpatient_number,
                    outpatient_number,
                    in_hospital_time,
                    out_hospital_time, 
                    outhospital_dept_name,    
                    pay_way,
                    die_time,
                    is_die,
                    inhospital_dept_name,
                    inhospital_way,
                    inhospital_total_cost,
                    inpatient_times,
                    isprimary,
                    diagnose_code,
                    diagnose_name,
                    hospital_code,
                    create_date,
                    delete_flag)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_diagnose_info(
                    empi, 
                    patient_no,
                    encounter_id,
                    patient_name,
                    age,
                    inpatient_number,
                    outpatient_number,
                    in_hospital_time,
                    out_hospital_time, 
                    outhospital_dept_name,    
                    pay_way,
                    die_time,
                    is_die,
                    inhospital_dept_name,
                    inhospital_way,
                    inhospital_total_cost,
                    inpatient_times,
                    isprimary,
                    diagnose_code,
                    diagnose_name,
                    hospital_code,
                    create_date,
                    delete_flag) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def insert_data2mysql_3(is_clear_temp = False): 
    
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
#    df_temp = get_temp_data()
#    a = process_first_inpatient(df_temp)
#    df_temp = preprocess(df_temp) 
    a,c = insert_data2mysql_3()
#    a = get_current_data()
#    c = compare_data()