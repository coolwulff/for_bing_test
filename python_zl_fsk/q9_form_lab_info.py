# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 14:17:33 2022

@author: LuPengFei
"""

'''
form_lab_info
修改：
第一次住院为 住院
后面的都为随访
不加规则展示

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
#    #sql_temp = "select * from form_lab_info_temp where test_item_name like '%尿蛋白' limit 100;"
#    sql_temp = "select * from form_lab_info_temp;"
#    df_temp = mysql.get_sql2df(sql_temp)
#    df_temp = df_temp[df_temp.ts_test_var > '2020-11-30']
#    
#    return df_temp


def generate_lab_temp_all_sql():
    
    da = pd.read_excel('./实验室检验项目名称-20220805.xlsx')
    #sql = "select * from form_lab_info_temp_all where encounter_type = 1 and Replace1"
    sql = '''
select 
a.*
from form_lab_info_temp_all a
join qs_drz_patient b
on a.empi = b.empi and a.patient_no = b.patient_no
where STR_TO_DATE(a.ts_test_var, '%Y-%m-%d')  >= DATE_FORMAT(b.in_hospital_datetime, '%Y-%m-%d') and encounter_type = 1 and Replace1
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
    del df_temp["table_item_name"]
    df_temp["test_item_code"] = [a.upper() for a in df_temp["test_item_code"]]
    
    return df_temp

#from helper import trans_sql_add_condition
def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from form_lab_info where hospital_code = '42502657200';"
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
    

def get_labcode2tablename():
    # 检验表单名称 打标签
    da = pd.read_excel('./实验室检验项目名称-20220805.xlsx')
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
 
from generate_lab_question_id import generate_question_id

dict_question_id = generate_question_id()

#def process_labcode_6699(question_id,
#                         test_item_code):
#    
#    if test_item_code == '6699' or test_item_code == "5729" or test_item_code == "AMA-M2":
#        return '41'
#    else:
#        try:
#            return str(dict_question_id[test_item_code])
#        except:
#            return str(-1)

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
                return "40"
            else:
                return "41"
        else:
            return c
        
    
    da['question_id'] = [judge_40or41(a,b,c) for a,b,c in zip(da["table_item_name"], da["lab_generic_id"],da['question_id'])]
    
    return da

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
     da['type1'] = ['1' if a in inp_list else '0' for a in da['inpatient_number']]
     da = da.reset_index(drop=True) 
     
     return da
     
# 数据前处理和数据生成
# 抗核糖核蛋白抗体:https://xueshu.baidu.com/usercenter/paper/show?paperid=83c134c3a31ca80ce08ad2d24bd1f11a&site=xueshu_se
# 抗nRNP抗体,又称为抗U1RNP抗体,全称抗u1-SnRNP抗体(抗U1小核核糖核蛋白抗体),也可以简称为抗RNP抗体   
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    
    
    # 每人每次住院保留一次
    da = da.sort_values(by=['empi','patient_no','inpatient_number','ts_test'],ascending=[True,True,True,True])
    da = da.reset_index()
    
#    # test_item_name - > table_item_name 字典映射
#    # 旧版，无法解决5650对应两个检查名称的bug
#    table_name_dict = get_labcode2tablename()
#    da['table_item_name'] = [table_name_dict[a] for a in da['test_item_code']]
    
    # test_item_name - > table_item_name 字典映射，解决5650对应两个检查名称的bug
    table_name_dict = get_labcode2tablename()
    da['table_item_name'] = [process_labcode_5650(a,b,table_name_dict) for a,b in zip(da['test_item_name'],da['test_item_code'])]
    
    # test_item_code 为 6699时， question_id改为41
    #da['question_id'] = [process_labcode_6699(a,b) for a,b in zip(da['question_id'],da['test_item_code'])]
     
    # 重新生成question_id,并过滤无关项
    da['question_id'] = [process_question_id(a) for a in da['test_item_code']]
    
    # 处理抗Ro52抗体、抗线粒体-M2型抗体
    #规则：如果同lab_generic_id(同份报告)的 table_item_name 存在 抗F肌动蛋白（F-Actin）抗体 ,则同份报告的另外两个指标（若存在） question_id 为40，否则为41。
    da = process_question_id_40or41(da)
    
    # 区分随访和非随访
    da = delete_first_inpatientnumber(da)


    
    return da

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    df_curr = get_current_data()
    
    #找差集
    zd = ['empi', 'patient_no','inpatient_number','question_id','lab_generic_id','table_item_name','test_item_name','ts_test_var', 'print_value']
    df_temp_0 = df_temp[zd]
    df_curr_0 = df_curr[zd]
    #df_curr_0['patient_num'] = [i[9:] for i in df_curr_0['patient_num']]


    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df1 = df_temp_0.append(df_curr_0)
    df1['patient_no'] = df1.patient_no.astype(str) 
    df1['inpatient_number'] = df1.inpatient_number.astype(str) 
    df1['question_id'] = df1.question_id.astype(str) 
    df1['lab_generic_id'] = df1.lab_generic_id.astype(str) 
    df1['ts_test_var'] = df1.ts_test_var.astype(str) 
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
#        if table_item_name == '尿沉渣白细胞':
#            return '尿沉渣白细胞计数'
#        elif table_item_name == '尿沉渣红细胞':
#            return '尿沉渣红细胞计数'
#        else:
#            return table_item_name
        
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
      
    for i in range(len(data)):
        
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        id_number = data['id_number'][i]
        encounter_id = data['encounter_id'][i]
        #encounter_type = data['encounter_type'][i]
        inpatient_number = data['inpatient_number'][i]
        outpatient_number = data['outpatient_number'][i]
        question_id = data['question_id'][i]
        lab_generic_id = data['lab_generic_id'][i]
        type1 =  data['type1'][i]
        ts_test = data['ts_test'][i]
        ts_test_var = data['ts_test_var'][i]
        #table_item_name = table_name_dict[data['test_item_code'][i]]
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
                    id_number,
                    encounter_id,
                    inpatient_number,
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
                    id_number,
                    encounter_id,
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
                    ts_draw,
                    ts_draw_var,
                    hospital_code,
                    create_date, 
                    delete_flag,
                    report_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
    truncate table form_lab_info_temp;
    '''
    return sql_create, sql_clear

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def insert_data2mysql_9(is_clear_temp = False): 
    
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