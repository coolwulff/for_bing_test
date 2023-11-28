# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 09:43:44 2022

@author: LuPengFei
"""

'''
form_medication_info_followup
修改：增加encounter_id
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
    #sql_temp = "select * from form_medication_info_followup_temp where projecttypecode = 1;"
    sql_temp = '''
select 
a.*
from form_medication_info_followup_temp a
join qs_drz_patient b
on a.empi = b.empi and a.patient_no = b.patient_no
where STR_TO_DATE(a.writerecipedatetime_date, '%Y-%m-%d')  > DATE_FORMAT(b.in_hospital_datetime, '%Y-%m-%d') and projecttypecode = 1
'''
    df_temp = mysql.get_sql2df(sql_temp)
    
    return df_temp

def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from form_medication_info where type = 0;"
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
    
def get_dic_medication_orders():
    
    

    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    sql = "select orders_code,code from dic_medication_orders;"
    df = mysql.get_sql2df(sql)
    
    dic_medication = {}
    for i in range(len(df)):
        dic_medication[df['orders_code'][i]] = df['code'][i]
        
    return dic_medication
    
def trans_orders_type(dic_medication,
                      projectcode):
    #print(projectcode)
    try:
        return dic_medication[projectcode]
    except:
        return 'None'
    
 
def get_ordersname2orderscode_dict():
    # 药品名称 映射 药品code
    #df = pd.read_excel('./狼疮患者西药医嘱去重_加code_过滤关键词.xlsx')
    df = pd.read_excel('./狼疮患者西药医嘱去重2022.3.3_加code_过滤关键词.xlsx')
    dic_medication = {}
    for i in range(len(df)):
        a = df['医嘱名称'][i]
        dic_medication[a] = df['code'][i]
        a = a.replace("（", "(")
        a = a.replace("）", ")")        
        dic_medication[a] = df['code'][i]
        
    return dic_medication        

    

# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    
    da = da.replace({'NaT': None})

    a = da.copy()

    zd = ['empi','patient_no','outpatient_number','encounter_id','writerecipedatetime_date','projectcode','projectname']
    df1 = a.sort_values(by=zd)
    df1 = df1.reset_index(drop=True)
    
    zd_2 = ['empi','patient_no','outpatient_number','encounter_id','writerecipedatetime_date','projectcode','projectname']

    df1 = df1.drop_duplicates(subset=zd_2,keep='first')
    
    # 删除 pc为立即，stop_time为null
    #df1 = df1[(df1.pc != 'ST') & (df1.stop_time != None)]
    
    df1['write_recipe_time'] = df1['writerecipedatetime_date']
    df1['orders_name'] = df1['projectname']    
    df1['orders_code'] = df1['projectid']    
    df1['write_recipe_time_var'] = df1['writerecipedatetime_date']    
    # projectid 映射 orders_code
#    dic_medication = get_dic_medication_orders()
#    df1['orders_type'] = [trans_orders_type(dic_medication,a) for a in df1['projectid']]
#    df1 = df1.reset_index(drop=True)
    
    # orders_name 映射 orders_code
    dic_medication = get_ordersname2orderscode_dict()
    df1['orders_type'] = [trans_orders_type(dic_medication,a) for a in df1['projectname']]
    df1 = df1[df1['orders_type'] != 'None']
    df1 = df1.reset_index(drop=True)
      
    
    
    return df1

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    df_curr = get_current_data()
    
    #找差集
    zd = ['empi', 'patient_no','outpatient_number','encounter_id','write_recipe_time_var','orders_name','orders_code']
    df_temp_0 = df_temp[zd]
    df_curr_0 = df_curr[zd]
    #df_curr_0['patient_num'] = [i[9:] for i in df_curr_0['patient_num']]


    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df1 = df_temp_0.append(df_curr_0)
    df1['patient_no'] = df1.patient_no.astype(str) 
    df1['outpatient_number'] = df1.outpatient_number.astype(str) 
    df1['write_recipe_time_var'] = df1.write_recipe_time_var.astype(str) 
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
        outpatient_number = data['outpatient_number'][i]
        type1 = 0
        orders_code = data['orders_code'][i]
        orders_name = data['orders_name'][i]
        specifications = data['specifications'][i]
        dosage = data['dosage'][i]
        dosage_unit = data['dosageunit'][i]
        pathway = data['pathway'][i]
        tj = get_tj(pathway)
        frequency = data['frequency'][i]
        #pc = data['pc'][i]
        frequency, pc = get_pc(frequency)
        project_type_code = data['projecttypecode'][i]
        project_type_name = data['projecttypename'][i]    
        write_recipe_time = data['write_recipe_time'][i]
        hospital_code = data['hospital_code'][i]
        delete_flag = 0
        create_date = time_str
        encounter_id = 0
        orders_type = data['orders_type'][i]
        encounter_id = data['encounter_id'][i]
        
        tp = (      empi, 
                    patient_no,
                    outpatient_number,
                    type1,
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
                    hospital_code,
                    delete_flag,
                    create_date,
                    encounter_id,
                    write_recipe_time,
                    orders_type)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_medication_info(
                    empi, 
                    patient_no,
                    outpatient_number,
                    type,
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
                    hospital_code,
                    delete_flag,
                    create_date,
                    encounter_id,
                    write_recipe_time_var,
                    orders_type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
    truncate table form_medication_info_followup_temp;
    '''
    
    sql_update = '''
    update form_medication_info s, dic_medication_orders m set s.orders_type = m.code where s.type = 0 and s.orders_code = m.orders_code;
    '''
    
    sql_update_2 = '''
    ALTER table form_medication_info add column write_recipe_time_var VARCHAR(20) COMMENT "下嘱(开方)日期" after write_recipe_time;
    '''
    
    return sql_create, sql_clear,sql_update,sql_update_2

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def insert_data2mysql_14(is_clear_temp = False): 
    
    data = compare_data()
    sql, data_sql = generate_input(data=data)
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    
    sql_create, sql_clear, sql_update,sql_update_2 = sql_list()    

    # 更新字段
    try:
        #更新表
        mysql = db_pymysql(host=host_56
                             ,user=user_56
                             ,password=password_56
                             ,database=database_56
                             ,charset='utf8')
        mysql.update_sql(sql_update_2)
    except Exception as e:
        print(e)
 
    try:
        mysql = db_pymysql(host=host_56
                             ,user=user_56
                             ,password=password_56
                             ,database=database_56
                             ,charset='utf8')
        mysql.insert_data_many(data_sql,sql)

#        #更新表,更新速度太慢，在preprocess中转换
#        mysql = db_pymysql(host=host_56
#                             ,user=user_56
#                             ,password=password_56
#                             ,database=database_56
#                             ,charset='utf8')
#        mysql.update_sql(sql_update)
        
        # 清空表
        if is_clear_temp:
            mysql = db_pymysql(host=host_56
                                 ,user=user_56
                                 ,password=password_56
                                 ,database=database_56
                                 ,charset='utf8')
            mysql.execute_sql(sql_clear)
        
        return sql, data_sql
    except Exception as e:
        print(e)
        return sql, data_sql

if __name__ == '__main__':
    #a = get_temp_data()
    #b = preprocess(a)
    #a = compare_data()
    a,b = insert_data2mysql_14()
    
    #a = get_temp_data()
    #c = get_dic_medication_orders()