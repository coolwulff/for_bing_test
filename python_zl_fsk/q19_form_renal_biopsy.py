# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 15:09:32 2023

@author: wdky
"""

import numpy as np
import pandas as pd
import datetime
    
from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def get_temp_data():
    
    from q19_helper import data
    df_temp = data
    
    return df_temp


def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from form_renal_biopsy where hospital_code = '42502657200';"
#     sql_curr = trans_sql_add_condition(sql_curr)
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
    
   
# 数据前处理和数据生成
def preprocess(da):
    '''
    风湿科：数据前处理
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    
    
    def judge_empi(empi):
        if empi is None:
            return True
        return False
        
    da['is_del'] = [judge_empi(i) for i in da['empi']]
    da = da[da['is_del'] == False]

    
    zd = ['empi', 'patient_no','inpatient_number','ts_exam_var']
    da = da.drop_duplicates(subset=zd,keep='first')   
    da = da.reset_index(drop=True) 
    
    return da

def compare_data():
    df_temp = get_temp_data()
    df_temp = preprocess(df_temp)
    try:
        record_id = df_temp['record_id'].values[0]
    except:
        record_id = -1
    df_curr = get_current_data()
    
    #找差集
    zd = ['empi', 'patient_no','inpatient_number','ts_exam_var']
    df_temp_0 = df_temp[zd]
    df_curr_0 = df_curr[zd]
    #df_curr_0['patient_num'] = [i[9:] for i in df_curr_0['patient_num']]

    df_curr['patient_no'] = [str(int(i)) for i in df_curr['patient_no']]
    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df1 = df_temp_0.append(df_curr_0)
    df1['patient_no'] = df1.patient_no.astype(str) 
    df1['inpatient_number'] = df1.inpatient_number.astype(str) 
    df1['ts_exam_var'] = df1.ts_exam_var.astype(str) 
    
    df1 = df1.drop_duplicates(subset=zd,keep=False)
    df1 = df1[df1['id0']<n0]
        
    idx = df1.index.tolist()
    
    n0 = len(df_temp.columns.tolist())
    a0 = [i for i in range(n0)]
    res = df_temp.iloc[idx,a0]
    res = res.reset_index(drop=True)
        
    return res, record_id

def generate_input(data):
    '''
    生成插入数据
    param:
    data:dataframe, 经过后处理的数据


        empi
        ,patient_no
        ,patient_name        
        ,encounter_id
        ,inpatient_number
        ,outpatient_number
        ,ts_exam
        ,ts_exam_var
        ,p1_lcxsyblfx
        ,p2_qtlcxsyblfx
        ,p3_ai_hdxzs
        ,p4_ci_mxzs
        ,p5_mxxgnxbzd
        ,p6_mxxgnxbzdpf
        ,p7_zxlxbjrhsl
        ,p8_zxlxbjrhslpf
        ,p9_xbxhhxwxbxxyt
        ,p10_xbxhhxwxbxxytpf
        ,p11_xwsyhs
        ,p12_xwsyhspf
        ,p13_npxtmwzcj
        ,p14_npxtmwzcjpf
        ,p15_jzyxxbjr
        ,p16_jzyxxbjrpf
        ,p17_sxqyh
        ,p18_sxqyhpf
        ,p19_xwxxyt
        ,p20_xwxxytpf
        ,p21_jzxwh
        ,p22_jzxwhpf
        ,p23_sxqws
        ,p24_sxqwspf
        ,p25_myyg
        ,p26_cjwxt
        ,p27_cjwbw
        ,p28_cjwfb
        ,hospital_code
        ,create_date
        ,delete_flag
    '''
    
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
      
    for i in range(len(data)):
        
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        patient_name = data['patient_name_x'][i]        
        encounter_id = data['encounter_id'][i]
        inpatient_number = data['inpatient_number'][i]
        outpatient_number = data['outpatient_number'][i]
        ts_exam = data['ts_exam_var'][i]
        ts_exam_var = data['ts_exam_var'][i]
        p1_lcxsyblfx = data['p1_lcxsyblfx'][i]
        p2_qtlcxsyblfx = data['p2_qtlcxsyblfx'][i]
        p3_ai_hdxzs = data['p3_ai_hdxzs'][i]
        p4_ci_mxzs = data['p4_ci_mxzs'][i]
        p5_mxxgnxbzd = data['p5_mxxgnxbzd'][i]
        p6_mxxgnxbzdpf = data['p6_mxxgnxbzdpf'][i]
        p7_zxlxbjrhsl = data['p7_zxlxbjrhsl'][i]
        p8_zxlxbjrhslpf = data['p8_zxlxbjrhslpf'][i]
        p9_xbxhhxwxbxxyt = data['p9_xbxhhxwxbxxyt'][i]
        p10_xbxhhxwxbxxytpf = data['p10_xbxhhxwxbxxytpf'][i]
        p11_xwsyhs = data['p11_xwsyhs'][i]
        p12_xwsyhspf = data['p12_xwsyhspf'][i]
        p13_npxtmwzcj = data['p13_npxtmwzcj'][i]
        p14_npxtmwzcjpf = data['p14_npxtmwzcjpf'][i]
        p15_jzyxxbjr = data['p15_jzyxxbjr'][i]
        p16_jzyxxbjrpf = data['p16_jzyxxbjrpf'][i]
        p17_sxqyh = data['p17_sxqyh'][i]
        p18_sxqyhpf = data['p18_sxqyhpf'][i]
        p19_xwxxyt = data['p19_xwxxyt'][i]
        p20_xwxxytpf = data['p20_xwxxytpf'][i]
        p21_jzxwh = data['p21_jzxwh'][i]
        p22_jzxwhpf = data['p22_jzxwhpf'][i]
        p23_sxqws = data['p23_sxqws'][i]
        p24_sxqwspf = data['p24_sxqwspf'][i]
        p25_myyg = data['p25_myyg'][i]
        p26_cjwxt = data['p26_cjwxt'][i]
        p27_cjwbw = data['p27_cjwbw'][i]
        p28_cjwfb = data['p28_cjwfb'][i]
        hospital_code = '42502657200'
        create_date =   time_str  
        delete_flag = 0
        exam_find = data['exam_find'][i]
        exam_conclusion = data['exam_conclusion'][i]
        
        tp = (          empi
                        ,patient_no
                        ,patient_name        
                        ,encounter_id
                        ,inpatient_number
                        ,outpatient_number
                        ,ts_exam
                        ,ts_exam_var
                        ,p1_lcxsyblfx
                        ,p2_qtlcxsyblfx
                        ,p3_ai_hdxzs
                        ,p4_ci_mxzs
                        ,p5_mxxgnxbzd
                        ,p6_mxxgnxbzdpf
                        ,p7_zxlxbjrhsl
                        ,p8_zxlxbjrhslpf
                        ,p9_xbxhhxwxbxxyt
                        ,p10_xbxhhxwxbxxytpf
                        ,p11_xwsyhs
                        ,p12_xwsyhspf
                        ,p13_npxtmwzcj
                        ,p14_npxtmwzcjpf
                        ,p15_jzyxxbjr
                        ,p16_jzyxxbjrpf
                        ,p17_sxqyh
                        ,p18_sxqyhpf
                        ,p19_xwxxyt
                        ,p20_xwxxytpf
                        ,p21_jzxwh
                        ,p22_jzxwhpf
                        ,p23_sxqws
                        ,p24_sxqwspf
                        ,p25_myyg
                        ,p26_cjwxt
                        ,p27_cjwbw
                        ,p28_cjwfb
                        ,hospital_code
                        ,create_date
                        ,delete_flag
                        ,exam_find
                        ,exam_conclusion)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_renal_biopsy(
        empi
        ,patient_no
        ,patient_name        
        ,encounter_id
        ,inpatient_number
        ,outpatient_number
        ,ts_exam
        ,ts_exam_var
        ,p1_lcxsyblfx
        ,p2_qtlcxsyblfx
        ,p3_ai_hdxzs
        ,p4_ci_mxzs
        ,p5_mxxgnxbzd
        ,p6_mxxgnxbzdpf
        ,p7_zxlxbjrhsl
        ,p8_zxlxbjrhslpf
        ,p9_xbxhhxwxbxxyt
        ,p10_xbxhhxwxbxxytpf
        ,p11_xwsyhs
        ,p12_xwsyhspf
        ,p13_npxtmwzcj
        ,p14_npxtmwzcjpf
        ,p15_jzyxxbjr
        ,p16_jzyxxbjrpf
        ,p17_sxqyh
        ,p18_sxqyhpf
        ,p19_xwxxyt
        ,p20_xwxxytpf
        ,p21_jzxwh
        ,p22_jzxwhpf
        ,p23_sxqws
        ,p24_sxqwspf
        ,p25_myyg
        ,p26_cjwxt
        ,p27_cjwbw
        ,p28_cjwfb
        ,hospital_code
        ,create_date
        ,delete_flag
        ,exam_find
        ,exam_conclusion) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    '''
    return sql, d_insert

def generate_check_sql():
    pass

def sql_list(record_id):
    
    # 建表
    sql_create = '''
    '''
    #sql_create = sql_create.replace('\n', '')
    # 清空表
    sql_clear = '''
    '''
    
    # 更新entry_renal_biopsy
    sql_update = "update `entry_renal_biopsy` set deal_statue = 1 where record_id = "
    sql_update = sql_update + str(int(record_id)) + ';'
    
    return sql_create, sql_clear ,sql_update


def insert_data2mysql_19(is_clear_temp = False): 
    
    data,record_id = compare_data()
    sql, data_sql = generate_input(data=data)
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')

    
    sql_create, sql_clear, sql_update = sql_list(record_id)    
 
    try:
        mysql.insert_data_many(data_sql,sql)
        
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
#    a = compare_data()

    a,b = insert_data2mysql_19(is_clear_temp = False)
#    df_temp = get_temp_data()
#    df_temp = preprocess(df_temp)