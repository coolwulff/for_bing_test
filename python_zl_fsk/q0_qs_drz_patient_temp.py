# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 13:40:59 2021

@author: LuPengFei
"""

'''
风湿科：qs_drz_patient_temp

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
    sql_temp = "select * from qs_drz_patient_temp;"
    df_temp = mysql.get_sql2df(sql_temp)
    
    return df_temp

def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from qs_drz_patient where hospital_code = '42502657200';"
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
    
def filter_by_idcard(da):
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select distinct id_card from qs_drz_patient where hospital_code = '42502657200' and is_grouped=1;"
     df_curr = mysql.get_sql2df(sql_curr) 

     id_card_list = df_curr.id_card.values.tolist()
     
     da["is_del"] = da['id_card'].isin(id_card_list)
     da = da[da["is_del"]==False]
     return da
     
    
# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    
    
    # 过滤重复患者
    da = da[da["empi"] != '29ce8f56c1cea8a3109e6e74bb32f0f1']
    da = filter_by_idcard(da)    
    
    zd = ['empi']
    #zd = ['empi','inpatient_number']
    da = da.drop_duplicates(subset=zd,keep='first')    
    da = da.reset_index(drop=True) 
    
    return da

def get_max_patient_num():
    # 获取生产库中每年最大的patient_num序号
    mysql = db_pymysql(host=host_56
                 ,user=user_56
                 ,password=password_56
                 ,database=database_56
                 ,charset='utf8')
    
    # 添加 42502657200
    sql_curr = '''
SELECT
	patient_num,
	left( patient_num, 4 ) AS patient_num_year 
FROM
	qs_drz_patient 
WHERE
	length( patient_num ) = 9 and hospital_code = "42502657200"
ORDER BY
	patient_num;    
'''
    df = mysql.get_sql2df(sql_curr)
    year_range = list(range(1980,3990))
    res = {}
    
    for i in year_range:
        df_i = df[df['patient_num_year'].str.contains(str(i))]
        res[i] = 0
        if len(df_i) > 0:
            df_i = df_i[['patient_num']]
            res[i] = int(df_i.patient_num.values[-1][6:])

    return res

def fix_increase_patient_num(df_increase,
                             max_patient_num_dict):
    # 修正增量数据的patient_num。
    # 规则：对新增数据，以当年最大的patient_num向后排序
    
    for i in range(len(df_increase)):
        temp0 = df_increase.patient_num[i]
        year_ = int(temp0[0:4])
        current_num = max_patient_num_dict[year_] + 1
        max_patient_num_dict[year_] = current_num
        
        new_num = str(int(current_num))
        new_num = new_num.rjust(4,'0')
        
        new_patient_num = str(year_) + '-' + new_num
        df_increase.patient_num[i] = new_patient_num
    
    return df_increase


def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    
#    df_temp = df_temp[df_temp['operate_date']>'2017-01-01']
#    df_temp = df_temp.reset_index(drop=True)
    
    df_curr = get_current_data()
    
    #找差集
    zd = ['empi']
    #zd = ['empi','inpatient_number']
    df_temp_0 = df_temp[zd]
    df_curr_0 = df_curr[zd]
    #df_curr_0['patient_num'] = [i[9:] for i in df_curr_0['patient_num']]


    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df1 = df_temp_0.append(df_curr_0)
#    df1['inpatient_number'] = df1.inpatient_number.astype(str) 
#    df1['patient_no'] = df1.patient_no.astype(str) 
    
    df1 = df1.drop_duplicates(subset=zd,keep=False)
    df1 = df1[df1['id0']<n0]
        
    idx = df1.index.tolist()
    
    n0 = len(df_temp.columns.tolist())
    a0 = [i for i in range(n0)]
    res = df_temp.iloc[idx,a0]
    
    res = res.reset_index(drop=True)
    
    # 对patient_num重新编号
    max_patient_num_dict = get_max_patient_num()
    res2 = fix_increase_patient_num(res,
                                    max_patient_num_dict)
    
    
        
    return res2

def generate_input(data):
    '''
    生成插入数据
    param:
    data:dataframe, 经过后处理的数据

    patient_num,
    empi, 
    inpatient_number, 
    patient_no, 
    name, 
    id_card, 
    sex, 
    age,
    hospital_id,
    hospital_code,
    ward,        
    group_id, 

    in_hospital_datetime, 
    out_hospital_datetime, 
    in_hospital_dept_code, 
    in_hospital_dept_name, 

    primary_diagnosis_code, 
    primary_diagnosis, 
 
    delete_flag,
    source_flag, 
    create_date

    '''
    
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
      
    for i in range(len(data)):
        #patient_num = 'LiT-RenJ-' + str(data['patient_num'][i])
        patient_num = data['patient_num'][i]
        empi = data['empi'][i]
        inpatient_number = data['inpatient_number'][i]
        patient_no = data['patient_no'][i]
        name = data['name'][i]
        id_card = data['id_card'][i]
        sex = data['sex'][i]        
        age = data['age'][i]
        hospital_id = data['hospital_id'][i]
        hospital_code =  data['hospital_code'][i]
        ward =  data['ward'][i]
        group_id = data['group_id'][i]
        in_hospital_datetime = data['in_hospital_datetime'][i]
        out_hospital_datetime = data['out_hospital_datetime'][i]
        in_hospital_dept_code = data['in_hospital_dept_code'][i]
        in_hospital_dept_name = data['in_hospital_dept_name'][i]  
        primary_diagnosis_code = data['primary_diagnosis_code'][i]  
        primary_diagnosis = data['primary_diagnosis'][i]                 
        delete_flag = data['delete_flag'][i]
        source_flag = data['source_flag'][i]
        create_date = time_str
        is_grouped = str(1)


    
        tp = (patient_num,
            empi,
            inpatient_number,
            patient_no,
            name,
            id_card,
            sex,    
            age,
            hospital_id,
            hospital_code,
            ward,
            group_id,
            in_hospital_datetime,
            out_hospital_datetime,
            in_hospital_dept_code,
            in_hospital_dept_name,
            primary_diagnosis_code,
            primary_diagnosis,
            delete_flag,
            source_flag,
            create_date,
            is_grouped)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into qs_drz_patient(
            patient_num,
            empi,
            inpatient_number,
            patient_no,
            name,
            id_card,
            sex,    
            age,
            hospital_id,
            hospital_code,
            ward,
            group_id,
            in_hospital_datetime,
            out_hospital_datetime,
            in_hospital_dept_code,
            in_hospital_dept_name,
            primary_diagnosis_code,
            primary_diagnosis,
            delete_flag,
            source_flag,
            create_date,
            is_grouped) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
    truncate table qs_drz_patient_temp;
    '''
    return sql_create, sql_clear

def insert_data2mysql_0(is_clear_temp = False): 
    
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

    a,b = insert_data2mysql_0(False)
#    a = compare_data()
#    df_curr = get_current_data()
#    a = get_max_patient_num()

    