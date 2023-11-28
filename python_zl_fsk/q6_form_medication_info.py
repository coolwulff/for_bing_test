# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 15:59:09 2022

@author: LuPengFei
"""

'''
form_medication_info_temp
区分第一次住院和其他住院
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
    #sql_temp = "select * from form_medication_info_temp;"
    sql_temp = '''
select 
a.*
from form_medication_info_temp a
join qs_drz_patient b
on a.empi = b.empi and a.patient_no = b.patient_no
where STR_TO_DATE(a.write_recipe_time, '%Y-%m-%d')  >= DATE_FORMAT(b.in_hospital_datetime, '%Y-%m-%d')
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
     sql_curr = "select * from form_medication_info where hospital_code = '42502657200';"
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
     da['type'] = ['1' if a in inp_list else '0' for a in da['inpatient_number']]
     da = da.reset_index(drop=True) 
     
     return da
    
   
# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    
    da = da.replace({'NaT': None})

    a = da.copy()
    a['write_recipe_time_ymd'] = [str(i)[0:10] for i in a['write_recipe_time']]
    zd = ['empi','patient_no','encounter_id','inpatient_number','in_hospital_time',\
          'orders_code','orders_name','write_recipe_time_ymd','frequency']
    df1 = a.sort_values(by=zd)
    df1 = df1.reset_index(drop=True)
    
    zd_2 = ['empi','patient_no','encounter_id','inpatient_number','in_hospital_time',\
          'orders_code','orders_name','write_recipe_time_ymd']

    df1 = df1.drop_duplicates(subset=zd_2,keep='first')
    
    # 删除 pc为立即，stop_time为null
    #df1 = df1[(df1.pc != 'ST') & (df1.stop_time != None)]
    
    # 区分 type
    df1 = delete_first_inpatientnumber(df1)
    
    df1 = df1.reset_index(drop=True)
    
    return df1

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    df_curr = get_current_data()
    
    #找差集
    zd = ['empi', 'patient_no','inpatient_number','encounter_id','master_orders_id','orders_name']
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
    df1['encounter_id'] = df1.encounter_id.astype(str) 
    df1['master_orders_id'] = df1.master_orders_id.astype(str) 
    
    df1 = df1.drop_duplicates(subset=zd,keep=False)
    df1 = df1[df1['id0']<n0]
        
    idx = df1.index.tolist()
    
    n0 = len(df_temp.columns.tolist())
    a0 = [i for i in range(n0)]
    res = df_temp.iloc[idx,a0]
    res = res.reset_index(drop=True)
        
    return res

def process_1():
    '''
    处理药品重复（立即和每天一次）的情况
    '''
    a = get_current_data()
    a['write_recipe_time_ymd'] = [str(i)[0:10] for i in a['write_recipe_time']]
    zd = ['empi','patient_no','encounter_id','inpatient_number','in_hospital_time',\
          'orders_code','orders_name','write_recipe_time_ymd','frequency']
    df1 = a.sort_values(by=zd)
    df1 = df1.reset_index(drop=True)
    
    zd_2 = ['empi','patient_no','encounter_id','inpatient_number','in_hospital_time',\
          'orders_code','orders_name','write_recipe_time_ymd']

    df1 = df1.drop_duplicates(subset=zd_2,keep='first')
    
    del_id = set(a['id'].values.tolist()) - set(df1['id'].values.tolist())
    del_id = list(del_id)
    del_id.sort()
    
    # 数据库操作 - 根据id删除重复数据
    sql_del = "DELETE FROM form_medication_info WHERE id = %s;"
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    mysql.insert_data_many(del_id,sql_del)
    return del_id

def generate_input(data):
    '''
    生成插入数据
    param:
    data:dataframe, 经过后处理的数据

    empi, 
    patient_no,
    encounter_id,
    inpatient_number,
    outpatient_number,
    type1,
    in_hospital_time,
    out_hospital_time,
    master_orders_id,
    orders_code,
    orders_name,
    specifications,
    dosage,
    dosage_unit,
    pathway,
    tj,
    frequency,
    pc,
    project_type_code,
    project_type_name,    
    write_recipe_time,
    orders_start_time,
    stop_time,
    remark,
    hospital_code,
    delete_flag,
    create_date
    '''
    
#    def get_tj(pathway):
#        if pathway=='口服':
#            return 1
#        else:
#            return None
    
    def get_pc(freqency):
        
        if freqency is None:
            return None, None
        
#        dic_pc = {'QD':'每天一次'
#                    ,'BID':'每天二次'
#                    ,'TID':'每天三次'
#                    ,'QID':'每天四次'
#                    ,'Q30D':'每30天一次'
#                    ,'QW':'一周一次'
#                    ,'Q2W':'二周一次'
#                    ,'BIW':'一周二次'
#                    ,'TIW':'每周三次(W1/W3/W5)'
#                    ,'Q30M':'每三十分钟一次'
#                    ,'Q1H':'一小时一次'
#                    ,'Q2H':'二小时一次'
#                    ,'Q3H':'三小时一次'
#                    ,'Q4H':'四小时一次'
#                    ,'Q5H':'五小时一次'
#                    ,'Q6H':'六小时一次'
#                    ,'Q8H':'八小时一次'
#                    ,'Q12H':'12小时一次'
#                    ,'Q72H':'72小时一次'
#                    ,'QM':'每天中午一次'
#                    ,'QN':'每晚一次'
#                    ,'QON':'每2晚一次'
#                    ,'ST':'立即'
#                    ,'QOD':'隔天一次'
#                    ,'Q5D':'五天一次'
#                    ,'Q10D':'十天一次'
#                    ,'C12H':'12小时维持'
#                    ,'C24H':'24小时维持'
#                    ,'PRN':'必要时使用'
#                    ,'AC':'明晨急化验'
#                    ,'AM':'明晨化验'}

        dic_pc = {'QD':'每天一次'
                    ,'BID':'每天二次'
                    ,'TID':'每天三次'
                    ,'QID':'每天四次'
                    ,'Q30D':'每30天一次'
                    ,'QW':'一周一次'
                    ,'Q2W':'二周一次'
                    ,'BIW':'一周二次'
                    ,'TIW':'每周三次(W1/W3/W5)'
                    ,'Q30M':'每三十分钟一次'
                    ,'Q1H':'一小时一次'
                    ,'Q2H':'二小时一次'
                    ,'Q3H':'三小时一次'
                    ,'Q4H':'四小时一次'
                    ,'Q5H':'五小时一次'
                    ,'Q6H':'六小时一次'
                    ,'Q8H':'八小时一次'
                    ,'Q12H':'12小时一次'
                    ,'Q72H':'72小时一次'
                    ,'QM':'每天中午一次'
                    ,'QN':'每晚一次'
                    ,'QON':'每2晚一次'
                    ,'ST':'立即'
                    ,'QOD':'隔天一次'
                    ,'Q5D':'五天一次'
                    ,'Q10D':'十天一次'
                    ,'C12H':'12小时维持'
                    ,'C24H':'24小时维持'
                    ,'PRN':'必要时使用'
                    ,'AC':'明晨急化验'
                    ,'AM':'明晨化验'}
            
        try:
            return freqency, dic_pc[freqency]
        except:
            return '9', '其他给药频次'

    def get_tj(pathway):
        
        if pathway is None:
            return None
        # 参考excel
        dic_tj = {'口服':	1
                    ,'餐中口服':	1
                    ,'餐前口服':	1
                    ,'餐后口服':	1
                    ,'直肠给药':	2
                    ,'舌下给药':	3
                    ,'注射给药':	4
                    ,'皮下':	401
                    ,'皮内':	402
                    ,'肌注':	403
                    ,'静滴':	404
                    ,'营养静滴':	404
                    ,'静脉注射':	405
                    ,'静注':	405
                    ,'吸入':	5
                    ,'雾化吸入':	5
                    ,'局部用药':	6
                    ,'椎管内给药':	601
                    ,'关节腔内给药':	602
                    ,'胸膜腔给药	':603
                    ,'腹腔给药':	604
                    ,'阴道用药':	605
                    ,'滴眼':	606
                    ,'滴左眼	':606
                    ,'滴右眼':	606
                    ,'滴鼻':	607
                    ,'喷喉':	608
                    ,'含化':	609
                    ,'湿敷':	610
                    ,'皮肤外用':	611
                    ,'外用':	611
                    ,'局部用药扩充内容':	'6XX'
                    ,'其他局部给药途径':	699
                    ,'其他':	9
                    ,'膀胱冲洗':	9
                    ,'含漱':	9
                    ,'静推':	15
                    ,'动脉注射':	9
                    ,'气道湿化':	9
                    ,'鼻饲':	10
                    ,'纳阴':	9
                    ,'静脉微泵':	7
                    ,'眼部外用':	9
                    ,'口腔外用':	9
                    ,'喷鼻':	9
                    ,'纳肛':	9
                    ,'灌肠':	16
                    ,'空肠造瘘管注入':9
                    ,'口腔喷雾':	9
                    ,'清洗':	9
                    ,'管饲':	11
                    ,'鼻腔填塞':	9
                    ,'静泵':	8
                    ,'涂眼':	9
                    ,'煎服':	14
                    ,'胃管内注药':	9
                    ,'喷洒':	9
                    ,'嚼服':	9
                    ,'冲服':	9
                    ,'睡前涂眼':	9
                    ,'喷雾':	9
                    ,'造影':13
                    ,'舌下含服':	12
                    ,'坐浴':	9
                    ,'吞服':	9
                    }
        
        try:
            res = dic_tj[pathway]
        except:
            res = 9
        return res


        
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
      
    for i in range(len(data)):
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        encounter_id = data['encounter_id'][i]
        inpatient_number = data['inpatient_number'][i]
        outpatient_number = data['outpatient_number'][i]
        type1 = data['type'][i]
        in_hospital_time = data['in_hospital_time'][i]
        out_hospital_time = data['out_hospital_time'][i]
        master_orders_id = data['master_orders_id'][i]
        orders_code = data['orders_code'][i]
        orders_name = data['orders_name'][i]
        specifications = data['specifications'][i]
        dosage = data['dosage'][i]
        dosage_unit = data['dosage_unit'][i]
        pathway = data['pathway'][i]
        tj = get_tj(pathway)
        frequency = data['frequency'][i]
        #pc = data['pc'][i]
        frequency, pc = get_pc(frequency)
        project_type_code = data['project_type_code'][i]
        project_type_name = data['project_type_name'][i]    
        write_recipe_time = data['write_recipe_time'][i]
        orders_start_time = data['orders_start_time'][i]
        stop_time = data['stop_time'][i]
        remark = data['remark'][i]
        hospital_code = data['hospital_code'][i]
        delete_flag = data['delete_flag'][i]
        create_date = time_str
        
        tp = (      empi, 
                    patient_no,
                    encounter_id,
                    inpatient_number,
                    outpatient_number,
                    type1,
                    in_hospital_time,
                    out_hospital_time,
                    master_orders_id,
                    orders_code,
                    orders_name,
                    specifications,
                    dosage,
                    dosage_unit,
                    pathway,
                    tj,
                    frequency,
                    pc,
                    project_type_code,
                    project_type_name,    
                    write_recipe_time,
                    orders_start_time,
                    stop_time,
                    remark,
                    hospital_code,
                    delete_flag,
                    create_date)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_medication_info(
                empi, 
                patient_no,
                encounter_id,
                inpatient_number,
                outpatient_number,
                type,
                in_hospital_time,
                out_hospital_time,
                master_orders_id,
                orders_code,
                orders_name,
                specifications,
                dosage,
                dosage_unit,
                pathway,
                tj,
                frequency,
                pc,
                project_type_code,
                project_type_name,    
                write_recipe_time,
                orders_start_time,
                stop_time,
                remark,
                hospital_code,
                delete_flag,
                create_date ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
    truncate table form_medication_info_temp;
    '''
    
    sql_update = '''
    update form_medication_info s, dic_medication_orders m set s.orders_type = m.code where s.orders_code = m.orders_code;
    '''
    return sql_create, sql_clear,sql_update

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def insert_data2mysql_6(is_clear_temp = False): 
    
    data = compare_data()
    sql, data_sql = generate_input(data=data)
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    
    sql_create, sql_clear, sql_update = sql_list()    
 
    try:
        mysql.insert_data_many(data_sql,sql)

        #更新表
        mysql = db_pymysql(host=host_56
                             ,user=user_56
                             ,password=password_56
                             ,database=database_56
                             ,charset='utf8')
        mysql.update_sql(sql_update)
        
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
    a,b = insert_data2mysql_6()

    