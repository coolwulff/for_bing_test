# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 17:57:46 2022

@author: wdky
"""

'''
建表：
DROP TABLE if exists form_bone_density;
CREATE TABLE IF NOT EXISTS form_bone_density(
empi VARCHAR(36) COMMENT 'EMPI',
patient_no INT(20) COMMENT '患者ID',
patient_name VARCHAR(36) COMMENT '姓名', 
in_hospital_datetime VARCHAR(36) COMMENT '入院日期',
spine_scan_date VARCHAR(36) COMMENT '脊柱扫描日期',
spine_tscore VARCHAR(36) COMMENT '腰椎整体',
hip_tscore VARCHAR(36) COMMENT '左髋整体',
hipneck_tscore VARCHAR(36) COMMENT '左髋颈部 ',
create_date datetime(0) COMMENT '创建时间',
update_date datetime(0) COMMENT '更新时间',
last_update_date datetime(0) COMMENT '最后一次回填时间',
hospital_code VARCHAR(36) COMMENT '医疗机构代码',
delete_flag INT(20) COMMENT '删除标识'
);
'''



import numpy as np
import pandas as pd
import datetime
    

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def get_temp_data():
    from q18_gmd import data2    
    zd_use = ['empi', 'patient_no','PATIENT_NAME', 'ryrq','SPINE_SCANDATE', 'SPINE_TSCORE', 'HIP_TSCORE', 'HIPNECK_TSCORE','inpatient_number','type']
    data2 = data2[zd_use]
    data2.rename(columns={'empi':'empi'
                          ,'patient_no':'patient_no'
                          ,'PATIENT_NAME':'patient_name'
                          ,'ryrq':'in_hospital_datetime'
                          ,'SPINE_SCANDATE':'spine_scan_date'
                          ,'SPINE_TSCORE':'spine_tscore'
                          ,'HIP_TSCORE':'hip_tscore'
                          ,'HIPNECK_TSCORE':'hipneck_tscore'}
                          ,inplace=True)

    return data2

def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from form_bone_density;"
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
    
   
# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    

    zd = ['empi', 'patient_no','spine_scan_date','spine_tscore','hip_tscore','hipneck_tscore']
    da = da.drop_duplicates(subset=zd,keep='first')   
    da = da.reset_index(drop=True) 
    
    return da

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    df_curr = get_current_data()
    
    #找差集
    zd = ['empi', 'patient_no','spine_scan_date','spine_tscore','hip_tscore','hipneck_tscore']
    df_temp_0 = df_temp[zd]
    df_curr_0 = df_curr[zd]
    #df_curr_0['patient_num'] = [i[9:] for i in df_curr_0['patient_num']]


    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df1 = df_temp_0.append(df_curr_0)
    df1['patient_no'] = df1.patient_no.astype(str) 
    df1['spine_scan_date'] = df1.spine_scan_date.astype(str) 
    df1['spine_tscore'] = df1.spine_tscore.astype(str) 
    df1['hip_tscore'] = df1.hip_tscore.astype(str) 
    df1['hipneck_tscore'] = df1.hipneck_tscore.astype(str) 
    
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
    patient_name 
    in_hospital_datetime 
    spine_scan_date
    spine_tscore 
    hip_tscore
    hipneck_tscore
    hospital_code,
    create_date,     
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
        in_hospital_datetime = data['in_hospital_datetime'][i]
        spine_scan_date = data['spine_scan_date'][i]
        spine_tscore = data['spine_tscore'][i]
        hip_tscore = data['hip_tscore'][i]
        hipneck_tscore = data['hipneck_tscore'][i]
        hospital_code = "42502657200"
        create_date =   time_str  
        delete_flag = "0"
        inpatient_number = data['inpatient_number'][i]
        type_ = data['type'][i]
        
        tp = (  empi, 
                patient_no,
                patient_name, 
                in_hospital_datetime,
                spine_scan_date,
                spine_tscore,
                hip_tscore,
                hipneck_tscore,
                hospital_code,
                create_date,     
                delete_flag,
                inpatient_number,
                type_)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_bone_density(
                empi, 
                patient_no,
                patient_name, 
                in_hospital_datetime,
                spine_scan_date,
                spine_tscore,
                hip_tscore,
                hipneck_tscore,
                hospital_code,
                create_date,     
                delete_flag,
                inpatient_number,
                type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
    '''
    return sql_create, sql_clear

def insert_data2mysql_18(is_clear_temp = False): 
    
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
    a,b = insert_data2mysql_18()