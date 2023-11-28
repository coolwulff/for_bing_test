# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 11:03:24 2022

@author: LuPengFei
"""

'''
form_ris_info_followup_temp  检查
随访规则：
不做任何处理，直接展示
保留：超声心动图和骨密度

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
#    sql_temp = "select * from form_ris_info_followup_temp where question_id = 21;"
    sql_temp = '''
select 
a.*
from form_ris_info_followup_temp a
join qs_drz_patient b
on a.empi = b.empi and a.patient_no = b.patient_no
where STR_TO_DATE(a.ts_exam, '%Y-%m-%d')  > DATE_FORMAT(b.in_hospital_datetime, '%Y-%m-%d') and a.question_id = 21    
'''
    df_temp = mysql.get_sql2df(sql_temp)
    
    return df_temp

from helper import trans_sql_add_condition
def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from form_ris_info where type = 0 and hospital_code = '42502657200';"
     #sql_curr = trans_sql_add_condition(sql_curr)
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
    
def tras_question_id(question_id):
    
    ques_dict = {'20':66,
                 '21':67,
                 '22':67,
                 '23':68,
                 '24':69}
    return ques_dict[question_id]

# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    
    da = da.replace({'NaT': None})
    
    # 对question_id进行转换
    #转换规则：20 - 66; 21 - 67; 22 - 67; 23、 肺部 - 68；24 + 腹部 - 69
    da['question_id'] = [tras_question_id(a) for a in da['question_id']]
    
    # 过滤  超声检查部位：肝脏、胆囊、胰腺、脾脏、肾脏、甲状腺。 sql代码已经过滤
    zd = ['empi', 'patient_no','encounter_id','report_id']
    da = da.drop_duplicates(subset=zd,keep='first')  
    da = da.reset_index(drop=True) 
    
    return da

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    df_curr = get_current_data()
    
    #找差集
    #zd = ['empi', 'patient_no','inpatient_number','encounter_id','ts_exam_var','exam_name','exam_find']
    zd = ['empi', 'patient_no','encounter_id','report_id']
    df_temp_0 = df_temp[zd]
    df_curr_0 = df_curr[zd]
    #df_curr_0['patient_num'] = [i[9:] for i in df_curr_0['patient_num']]


    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df1 = df_temp_0.append(df_curr_0)
    df1['patient_no'] = df1.patient_no.astype(str) 
    df1['encounter_id'] = df1.encounter_id.astype(str) 
    df1['report_id'] = df1.report_id.astype(str) 
    
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
    id_number, 
    encounter_id,
    inpatient_number,
    outpatient_number,
type
    question_id,
    report_id,
    report_name,
    exam_name,    
    ts_exam,
    ts_exam_var, 
    body_site,
    exam_find,
    exam_conclusion,
    summary_note,
    
    hospital_code,
    delete_flag,
    create_date

    '''
    
        
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
      
    for i in range(len(data)):
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        #id_number = data['id_number'][i] 
        encounter_id = data['encounter_id'][i]
        #inpatient_number = data['inpatient_number'][i]
        #outpatient_number = data['outpatient_number'][i]
        type1 = 0
        question_id = data['question_id'][i]
        report_id = data['report_id'][i]
        report_name = data['report_name'][i]
        exam_name = data['exam_name'][i]   
        ts_exam = data['ts_exam'][i]
        ts_exam_var = data['ts_exam_var'][i] 
        body_site = data['body_site'][i]
        exam_find = data['exam_find'][i]
        exam_conclusion = data['exam_conclusion'][i]
        summary_note = data['summary_note'][i]
        hospital_code = '42502657200'
        delete_flag = '0'
        create_date = time_str
        
        tp = (empi,
                patient_no,
                encounter_id,
                type1,
                question_id,
                report_id,
                report_name,
                exam_name, 
                ts_exam,
                ts_exam_var,
                body_site,
                exam_find,
                exam_conclusion,
                summary_note,
                hospital_code,
                delete_flag,
                create_date)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_ris_info(
                empi,
                patient_no,
                encounter_id,
                type,
                question_id,
                report_id,
                report_name,
                exam_name, 
                ts_exam,
                ts_exam_var,
                body_site,
                exam_find,
                exam_conclusion,
                summary_note,
                hospital_code,
                delete_flag,
                create_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
    truncate table form_ris_info_followup_temp;
    '''
    return sql_create, sql_clear

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def insert_data2mysql_11(is_clear_temp = False): 
    
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
    #a = compare_data()
    a,b = insert_data2mysql_11()