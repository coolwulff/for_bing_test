
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 17:14:35 2022

@author: LuPengFei
"""

'''
form_lab_info_followup:
回填规则：
正常回填，不加任何规则

'''

import numpy as np
import pandas as pd
import datetime
    

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

#def get_temp_data_old():
#    
#    mysql = db_pymysql(host=host_56
#                         ,user=user_56
#                         ,password=password_56
#                         ,database=database_56
#                         ,charset='utf8')
#    sql_temp = "select * from form_lab_info_followup_temp;"
#    df_temp = mysql.get_sql2df(sql_temp)
#    
#    return df_temp


def generate_lab_temp_all_sql():
    
    da = pd.read_excel('./实验室检验项目名称-20220805-随访.xlsx')
    da = da[da["question_id"]>0]
    #sql = "select * from form_lab_info_temp_all where encounter_type = 0 and Replace1"
    sql = '''
select 
a.*
from form_lab_info_temp_all a
join qs_drz_patient b
on a.empi = b.empi and a.patient_no = b.patient_no
where STR_TO_DATE(a.ts_test_var, '%Y-%m-%d')  > DATE_FORMAT(b.in_hospital_datetime, '%Y-%m-%d') and encounter_type = 0 and Replace1
'''
    code_list = da['检验项目代码'].values.tolist()
    code_list = list(set(code_list))
    
    temp = '('
    for c in code_list:
        temp2 = "(a.test_item_code = " + "\"" + str(c) + "\"" + ") or "
        temp = temp + temp2
    
    temp = temp[:-4]
    temp = temp + ')'
    
    sql = sql.replace('Replace1', temp)
    
    return sql
    
def get_temp_data():
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    sql_temp = generate_lab_temp_all_sql()
    df_temp = mysql.get_sql2df(sql_temp)
    #df_temp = df_temp[df_temp.ts_test_var > '2020-11-30']
    df_temp["reportname"] = df_temp["table_item_name"]
    df_temp["test_item_code"] = [a.upper() for a in df_temp["test_item_code"]]
    
    return df_temp

def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from form_lab_info where type = 0 and hospital_code = '42502657200';"
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
    

def get_labcode2tablename():
    # 检验表单名称 打标签
    da = pd.read_excel('./实验室检验项目名称-20220805-随访.xlsx')
    da = da[da["question_id"]>0]
    da = da.reset_index(drop=True)
    res = {}
    for i in range(len(da)):
        a = da['检验项目代码'][i]
        a = str(a).upper()
        b = da['表单名称'][i]
        res[a] = b
    res['5650'] = "抗Sm"    
    return res

def process_labcode_5650(test_item_name,
                         test_item_code,
                         table_name_dict):
    
    if test_item_name == "抗nRNP/Sm":
        return "抗nRNP/Sm"
    return table_name_dict[test_item_code]
 
from generate_lab_question_id import generate_question_id_sf

dict_question_id = generate_question_id_sf()

def process_question_id(test_item_code):
    #生成question_id
    
    try:
        return str(dict_question_id[test_item_code])
    except:
        return str(-1)    

def process_question_id_40or41(da):
    
    da_temp = da[da["table_item_name"]=="抗F肌动蛋白（F-Actin）抗体"]
    lab_generic_list = da_temp["lab_generic_id"].values.tolist()
    
    def judge_40or41(a,b,c):
        
        if a == "抗线粒体-M2型抗体" or a == "抗Ro52抗体":
            if b in lab_generic_list:
                return "-1"
            else:
                return "51"
        else:
            return c
        
    
    da['question_id'] = [judge_40or41(a,b,c) for a,b,c in zip(da["table_item_name"], da["lab_generic_id"],da['question_id'])]
    
    return da

# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    


    # test_item_name - > table_item_name 字典映射，解决5650对应两个检查名称的bug
    table_name_dict = get_labcode2tablename()
    da['table_item_name'] = [process_labcode_5650(a,b,table_name_dict) for a,b in zip(da['test_item_name'],da['test_item_code'])]
 
    # 重新生成question_id,并过滤无关项
    da['question_id'] = [process_question_id(a) for a in da['test_item_code']]
    da = da[da['question_id'] != "-1"]
    da = da.reset_index(drop=True)
    
    # 处理抗Ro52抗体、抗线粒体-M2型抗体
    #规则：如果同lab_generic_id(同份报告)的 table_item_name 存在 抗F肌动蛋白（F-Actin）抗体 ,则同份报告的另外两个指标（若存在） question_id 为-1，否则为51。
    da = process_question_id_40or41(da)  
    da = da[da['question_id'] != "-1"]
    da = da.reset_index(drop=True)    


    
    # 不去重，如实展示
#    # 按照empi,patid,encounter_id, question_id,table_item_name 排序和去重？
#    da = da.sort_values(by=['empi','patid','encounter_id',"question_id",'table_item_name','ts_test_var'],ascending=[True,True,True,True,True,True])
#    da = da.reset_index(drop=True)
#    
#    da.drop_duplicates(subset=['empi','patid','encounter_id',"question_id",'table_item_name'],keep='first',inplace=True)     
#    da = da.reset_index(drop=True)    
    
#    da["outpatient_number"] = da["patid"]
    
    return da

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    df_curr = get_current_data()
    
    #找差集
    zd = ['empi', 'outpatient_number','encounter_id','question_id','table_item_name','ts_test_var','test_item_name','print_value']
    df_temp_0 = df_temp[zd]
    df_curr_0 = df_curr[zd]
    #df_curr_0['patient_num'] = [i[9:] for i in df_curr_0['patient_num']]


    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df1 = df_temp_0.append(df_curr_0)
    df1['outpatient_number'] = df1.outpatient_number.astype(str) 
    df1['encounter_id'] = df1.encounter_id.astype(str) 
    df1['question_id'] = df1.question_id.astype(str) 
    df1['print_value'] = df1.print_value.astype(str) 

    
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
    encounter_type,
    inpatient_number,
    outpatient_number,
    question_id,
    lab_generic_id,
type,
    ts_test,
    ts_test_var,
    table_item_name,
    test_item_code,
    test_item_name,
    print_value,
    result_value,
    result_unit,
    reference_text,
    abnormal_flag,
    abnormal_flag_name,
    hospital_code,
    create_date,
    ts_draw,
    ts_draw_var
    '''
    def trans_table_item_name(table_item_name):
        return table_item_name
        
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
    table_name_dict = get_labcode2tablename()
      
    for i in range(len(data)):
        
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        #id_number = data['id_number'][i]
        encounter_id = data['encounter_id'][i]

        #inpatient_number = data['inpatient_number'][i]
        outpatient_number = data['outpatient_number'][i]
        question_id = data['question_id'][i]
        lab_generic_id = data['lab_generic_id'][i]
        type1 = 0
        ts_test = data['ts_test'][i]
        ts_test_var = data['ts_test_var'][i]

        table_item_name = data['table_item_name'][i]
        test_item_code = data['test_item_code'][i]
        test_item_name = data['test_item_name'][i]
        print_value = data['print_value'][i]
        result_value = data['result_value'][i]
        result_unit = data['result_unit'][i]
        reference_text = data['reference_text'][i]
        abnormal_flag = data['abnormal_flag'][i]
        abnormal_flag_name = data['abnormal_flag_name'][i]
        ts_draw = data['ts_draw'][i]
        ts_draw_var = data['ts_draw_var'][i]
        hospital_code = data['hospital_code'][i]
        create_date =   time_str  
        delete_flag = 0
        report_name = data['reportname'][i]
        
        tp = (      empi,
                    patient_no,
                    encounter_id,
                    outpatient_number,
                    question_id,
                    lab_generic_id,
                    type1,
                    ts_test,
                    ts_test_var,
                    table_item_name,
                    test_item_code,
                    test_item_name,
                    print_value,
                    result_value,
                    result_unit,
                    reference_text,
                    abnormal_flag,
                    abnormal_flag_name,
                    ts_draw,
                    ts_draw_var,
                    hospital_code,
                    create_date, 
                    delete_flag,
                    report_name)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_lab_info(
                    empi,
                    patient_no,
                    encounter_id,
                    outpatient_number,
                    question_id,
                    lab_generic_id,
                    type,
                    ts_test,
                    ts_test_var,
                    table_item_name,
                    test_item_code,
                    test_item_name,
                    print_value,
                    result_value,
                    result_unit,
                    reference_text,
                    abnormal_flag,
                    abnormal_flag_name,
                    ts_draw,
                    ts_draw_var,
                    hospital_code,
                    create_date, 
                    delete_flag,
                    report_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
    truncate table form_lab_info_temp_all;
    '''
    return sql_create, sql_clear

def insert_data2mysql_12(is_clear_temp = False): 
    
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
#    b = preprocess(a)
#    a = compare_data()
#    b,c = generate_input(a)
    a,b = insert_data2mysql_12()