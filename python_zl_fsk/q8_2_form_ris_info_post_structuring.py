# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 19:26:52 2022

@author: LuPengFei
"""

'''
form_ris_info  超声检查后结构化

'''

import numpy as np
import pandas as pd
import datetime
import re
from bs4 import BeautifulSoup
    
from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56
from d2_fsk.dict import data_process_dict,extract_rule_1_csjc_jcsj, extract_rule_1_csjc, computer_rule_1_csjc_jcsj,computer_rule_1_csjc,extract_rule_5_csxdt,computer_rule_5_csxdt
from Struct import Struct_data

def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr ='''
select id as id_, exam_find, exam_conclusion
from form_ris_info
where question_id = 22;
'''
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr

exam_find_back_name = list(extract_rule_1_csjc_jcsj.keys())

exam_conclusion_back_name = list(extract_rule_1_csjc.keys())


def post_structure_examfind():
    '''
    对超声检查后结构化提取：检查所见
    '''
    # 检查所见
    data = get_current_data()
    
    da = []
    for i in range(len(data)):
        para = data['exam_find'][i]
        
        if para is None:
            para = '无数据'
        if para == '':
            para = '无数据'
            
        da.append(para)
        
    s = Struct_data(da, 
                  data_process_dict,
                  extract_rule_1_csjc_jcsj,
                  computer_rule_1_csjc_jcsj)
    
    s2 = s.main()    
    
    res = []
    for temp in s2:
        temp1 = []
        temp2 = temp['result']
        for temp3 in exam_find_back_name:
            try:
                temp1.append(temp2[temp3][0]['entity'])
            except:
                temp1.append(None)
        res.append(temp1)
    
    res_df = pd.DataFrame(data=np.array(res), columns = exam_find_back_name)
    res_df['id_']  = data['id_']
    
    return res_df

def post_structure_examconclusion():
    '''
    对超声检查后结构化提取：检查结论
    '''
    # 检查结论
    data = get_current_data()
    
    da = []
    for i in range(len(data)):
        para = data['exam_conclusion'][i]
        
        if para is None:
            para = '无数据'
        if para == '':
            para = '无数据'
            
        da.append(para)
        
    s = Struct_data(da, 
                  data_process_dict,
                  extract_rule_1_csjc,
                  computer_rule_1_csjc)
    
    s2 = s.main()    
    
    res = []
    for temp in s2:
        temp1 = []
        temp2 = temp['result']
        for temp3 in exam_find_back_name:
            try:
                temp1.append(temp2[temp3][0]['entity'])
            except:
                temp1.append(None)
        res.append(temp1)
    
    res_df = pd.DataFrame(data=np.array(res), columns = exam_find_back_name)
    
    # 肝脏描述
    res_df['gzms'] = None

    for i in range(len(data)):
        para = data['exam_conclusion'][i]
        
        if para is None:
            continue
        # 肝脂肪浸润
        if '肝脂肪浸润' in para:
            gzms_0 = 1
        else:
            gzms_0 = -1
        
        # 脂肪肝
        if '脂肪肝' in para:
            gzms_1 = 2
        else:
            gzms_1 = -1
            
        # 肝硬化
        if '肝硬化' in para:
            gzms_2 = 3
        else:
            gzms_2 = -1
        
        val_list = [gzms_0,gzms_1,gzms_2]
        val_list = [ str(a) for a in val_list if a > 0]
        val_str = ','.join(val_list)
        if val_str == '':
            val_str = None
        res_df['gzms'][i] = val_str
    res_df['id_'] = data['id_']
    
    return res_df

def get_binarycontent_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr ='''
select id as id_, binary_content
from form_ris_info 
where binary_content is not null and question_id = 21;
'''
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr
 
# 解析html指标
     
def get_int_value(content):
    
    b = re.findall(r'[1-9]\d*', content)
    if len(b) > 0:
        res = int(b[0])  
        return res
    return None
     
#def get_int_value(content):
#    
#    return content
    
    
def post_struct_binarycontent():
    '''
    解析binary_content
    '''
    
    df = get_binarycontent_data()
    
    df['主动脉根部内径'] = ''
    df['左房内径'] = ''
    df['室间隔厚度'] = ''
    df['左室舒张末期内径'] = ''
    df['左室收缩末期内径'] = ''
    df['左室后壁厚度'] = ''
    df['左室心内膜缩短分数'] = ''
    df['左室射血分数'] = ''
    df['右心室心底内径'] = ''
    df['右心室心腰内径'] = ''
    df['右心室纵径'] = ''
    df['右心房内径'] = ''
    df['右心房纵径'] = ''
    df['右心房面积'] = ''
    df['病变节段占左室心肌总节段的百分比'] = ''

    for j in range(len(df)):
        #print(j)
        text = df['binary_content'][j]
        text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", text)

        soup = BeautifulSoup(text, features='lxml')
        tables = soup.find('table')
        rows = tables.find_all('tr')

        result = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            # result.append([ele for ele in cols if ele])
            result.append([ele for ele in cols])

        # print(result[5])
        df.loc[j, '主动脉根部内径'] = get_int_value(result[5][1])
        df.loc[j, '左房内径'] = get_int_value(result[6][1])
        df.loc[j, '室间隔厚度'] = get_int_value(result[7][1])
        df.loc[j, '左室舒张末期内径'] = get_int_value(result[8][1])
        df.loc[j, '左室收缩末期内径'] = get_int_value(result[9][1])
        df.loc[j, '左室后壁厚度'] = get_int_value(result[10][1])
        df.loc[j, '左室心内膜缩短分数'] = get_int_value(result[11][1])
        df.loc[j, '左室射血分数'] = get_int_value(result[12][1])
        df.loc[j, '右心室心底内径'] = get_int_value(result[5][5])
        df.loc[j, '右心室心腰内径'] = get_int_value(result[6][5])
        df.loc[j, '右心室纵径'] = get_int_value(result[7][5])
        df.loc[j, '右心房内径'] = get_int_value(result[8][5])
        df.loc[j, '右心房纵径'] = get_int_value(result[9][5])
        df.loc[j, '右心房面积'] = get_int_value(result[10][5])
        df.loc[j, '病变节段占左室心肌总节段的百分比'] = get_int_value(result[11][5])
    return df


# 超声心动图后结构化
def get_csxdt_data():
    mysql = db_pymysql(host=host_56
                       , user=user_56
                       , password=password_56
                       , database=database_56
                       , charset='utf8')
    sql_curr = '''
select id as id_, exam_find, exam_conclusion
from form_ris_info 
where question_id = 21;
'''
    df_curr = mysql.get_sql2df(sql_curr)

    return df_curr


def post_struct_csxdt():
    '''
    解析超声心动图
    '''

    df = get_csxdt_data()
    df['主动脉瓣描述'] = ''
    df['二尖瓣描述'] = ''
    df['三尖瓣描述'] = ''
    df['三尖瓣跨瓣压差'] = ''
    df['估测肺动脉收缩压'] = ''
    df['是否肺动脉增宽'] = ''
    df['肺动脉瓣描述'] = ''
    df['左室舒张功能'] = ''
    df['是否心包积液'] = ''
    df['线性无回声区最大距离'] = ''

    rows = df.shape[0]
    data_col = []

    for i in range(rows):
        line_find = '' if df['exam_find'][i] is None else df['exam_find'][i]  # 检查所见
        line_conclusion = '' if df['exam_conclusion'][i] is None else df['exam_conclusion'][i]  # 检查结论
        data_col.append(line_find + line_conclusion)
    s_col = Struct_data(data_col, data_process_dict, extract_rule_5_csxdt, computer_rule_5_csxdt)
    result_col = s_col.main()
    r = 0
    for one in result_col:
        print(r)
        merges = one['result']
        if len(merges) != 0:
            if '118' not in merges and '119' in merges:
                df.loc[r, '主动脉瓣描述'] = '9'
            if '120' not in merges and '121' in merges:
                df.loc[r, '二尖瓣描述'] = '9'
            if '122' not in merges and '123' in merges:
                df.loc[r, '三尖瓣描述'] = '9'
            if '127' not in merges and '128' in merges:
                df.loc[r, '肺动脉瓣描述'] = '9'
            for key, value in merges.items():
                if '118' in key:
                    df.loc[r, '主动脉瓣描述'] += key.replace('118_主动脉瓣描述_', '') + ';'
                elif '120' in key:
                    df.loc[r, '二尖瓣描述'] += key.replace('120_二尖瓣描述_', '') + ';'
                elif '122' in key:
                    df.loc[r, '三尖瓣描述'] += key.replace('122_三尖瓣描述_', '') + ';'
                elif '124' in key:
                    df.loc[r, '三尖瓣跨瓣压差'] = value[0]['entity']
                elif '125' in key:
                    df.loc[r, '估测肺动脉收缩压'] = value[0]['entity']
                elif '126_是否肺动脉增宽_1' in key:
                    df.loc[r, '是否肺动脉增宽'] = '1'
                elif '127' in key:
                    df.loc[r, '肺动脉瓣描述'] += key.replace('127_肺动脉瓣描述_', '') + ';'
                elif '129' in key:
                    df.loc[r, '左室舒张功能'] = value[0]['entity']
                elif '130_是否心包积液_1' in key:
                    df.loc[r, '是否心包积液'] = '1'
                elif '131' in key:
                    df.loc[r, '线性无回声区最大距离'] = value[0]['entity']
            if '126_是否肺动脉增宽_0' in merges:
                df.loc[r, '是否肺动脉增宽'] = '0'
            if '130_是否心包积液_0' in merges:
                df.loc[r, '是否心包积液'] = '0'
        else:
            pass
        r += 1
    df.loc[df['主动脉瓣描述'] == '', '主动脉瓣描述'] = 'NA'
    df.loc[df['二尖瓣描述'] == '', '二尖瓣描述'] = 'NA'
    df.loc[df['三尖瓣描述'] == '', '三尖瓣描述'] = 'NA'
    df.loc[df['肺动脉瓣描述'] == '', '肺动脉瓣描述'] = 'NA'
    df.loc[df['是否肺动脉增宽'] == '', '是否肺动脉增宽'] = 'NA'
    df.loc[df['是否心包积液'] == '', '是否心包积液'] = 'NA'
    df['主动脉瓣描述'] = df['主动脉瓣描述'].str.strip(';')
    df['二尖瓣描述'] = df['二尖瓣描述'].str.strip(';')
    df['三尖瓣描述'] = df['三尖瓣描述'].str.strip(';')
    df['肺动脉瓣描述'] = df['肺动脉瓣描述'].str.strip(';')
    return df


def post_structure():
    '''
    表18 辅助检查-超声检查——7月22日之前（优先级高）
    回填的数据根据检查所见和检查结论内容，需要结构化填入选项中。
    重点结构化填入选项：1.5肝脏描述、1.9脾脏长径 、1.10脾脏厚径 

    表21 辅助检查-超声心动图——7月22日之前（优先级高）
    回填的数据根据检查所见和检查结论内容，需要结构化填入选项中。

    '''
    df_exam_find = post_structure_examfind()
    df_exam_conclusion = post_structure_examconclusion()    
    df_exam_csxdt = post_struct_binarycontent()
    df_exam_csxdt_1 = post_struct_csxdt()

    #df = pd.concat([df_exam_find,df_exam_conclusion],axis = 1)
    
    # 超声检查
    zd_use0 = ['id_'        
              ,'gzms'
              ,'109_脾脏长径'
              ,'110_脾脏厚径']  
    
    #df = df.replace({np.nan: None})    
    
    
    replace_list_0 = []
    for i in range(len(df_exam_conclusion)):
        id_ = df_exam_conclusion['id_'][i]
        a= df_exam_conclusion['gzms'][i]
        b = df_exam_find['109_脾脏长径'][i]
        c = df_exam_find['110_脾脏厚径'][i]

        if a is None and b is None and c is None:
            continue

        tp = (a,b,c,id_)
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        replace_list_0.append(tp)
        
    sql_0 = '''
    update form_ris_info set gzms = (%s), gzcj = (%s), gzhj = (%s) where id = (%s);
    '''

    # 超声心动图
    zd_use0 = ['id_'        
              ,'主动脉根部内径'
              ,'左房内径'
              ,'室间隔厚度'
              ,'左室舒张末期内径'
              ,'左室收缩末期内径'
              '左室后壁厚度', 
              '左室心内膜缩短分数', 
              '左室射血分数', 
              '右心室心底内径', 
              '右心室心腰内径',
              '右心室纵径', 
              '右心房内径', 
              '右心房纵径', 
              '右心房面积', 
              '病变节段占左室心肌总节段的百分比']

    df_exam_csxdt = df_exam_csxdt.replace({np.nan: None})    
    
    replace_list_1 = []
    for ii in range(len(df_exam_csxdt)):
        id_ = df_exam_csxdt['id_'][ii]
        a = df_exam_csxdt['主动脉根部内径'][ii]
        b = df_exam_csxdt['左房内径'][ii]
        c = df_exam_csxdt['室间隔厚度'][ii]
        d = df_exam_csxdt['左室舒张末期内径'][ii]
        e = df_exam_csxdt['左室收缩末期内径'][ii]
        f = df_exam_csxdt['左室后壁厚度'][ii]
        g = df_exam_csxdt['左室心内膜缩短分数'][ii]
        h = df_exam_csxdt['左室射血分数'][ii]
        i = df_exam_csxdt['右心室心底内径'][ii]
        j = df_exam_csxdt['右心室心腰内径'][ii]
        k = df_exam_csxdt['右心室纵径'][ii]
        l = df_exam_csxdt['右心房内径'][ii]
        m = df_exam_csxdt['右心房纵径'][ii]
        n = df_exam_csxdt['右心房面积'][ii]
        o = df_exam_csxdt['病变节段占左室心肌总节段的百分比'][ii]        
        tp = (a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,id_)
        tp = (str(i) if i is not None else i for i in tp)
        tp = (None if i == 'nan' else i for i in tp)
        tp = tuple(list(tp))
        replace_list_1.append(tp)
        
    sql_1 = '''
update form_ris_info 
set aortic_root = (%s), 
left_atrial = (%s), 
ivs = (%s),
lvedd = (%s), 
lvesd = (%s),
lvpwt = (%s), 
lvesf = (%s),
lvef = (%s), 
idrv = (%s),
idrvc = (%s), 
larv = (%s),
idra = (%s), 
ldra = (%s),
raa = (%s), 
percentage = (%s)
where id = (%s);
    '''

    df_exam_csxdt_1 = df_exam_csxdt_1.replace({np.nan: None})

    replace_list_2 = []
    for ii in range(len(df_exam_csxdt_1)):
        id_ = df_exam_csxdt_1['id_'][ii]
        a = df_exam_csxdt_1['主动脉瓣描述'][ii]
        b = df_exam_csxdt_1['二尖瓣描述'][ii]
        c = df_exam_csxdt_1['三尖瓣描述'][ii]
        d = df_exam_csxdt_1['三尖瓣跨瓣压差'][ii]
        e = df_exam_csxdt_1['估测肺动脉收缩压'][ii]
        f = df_exam_csxdt_1['是否肺动脉增宽'][ii]
        g = df_exam_csxdt_1['肺动脉瓣描述'][ii]
        h = df_exam_csxdt_1['左室舒张功能'][ii]
        i = df_exam_csxdt_1['是否心包积液'][ii]
        j = df_exam_csxdt_1['线性无回声区最大距离'][ii]
        tp = (a, b, c, d, e, f, g, h, i, j, id_)
        tp = (str(i) if i is not None else i for i in tp)
        tp = (None if i in ('nan', '') else i for i in tp)
        tp = tuple(list(tp))
        replace_list_2.append(tp)

    sql_2 = '''
    update form_ris_info 
    set aortic_valve_desc = (%s), 
    mitral_valve_desc = (%s), 
    tricus_valve_desc = (%s),
    press_diff = (%s), 
    systo_pul = (%s),
    pul_artery_wide = (%s), 
    pul_artery_desc = (%s),
    diasto_left_ventri = (%s), 
    pericar_effusion = (%s),
    zone_distance = (%s)
    where id = (%s);
        '''

    return sql_0, replace_list_0, sql_1, replace_list_1, sql_2, replace_list_2
    
def update_data():
    '''
    根据id更新数据:
    
    '''
    sql0,data_sql0,sql1,data_sql1,sql2,data_sql2 = post_structure()
    
    # 更新超声检查
    mysql = db_pymysql(host=host_56
                 ,user=user_56
                 ,password=password_56
                 ,database=database_56
                 ,charset='utf8')
    mysql.insert_data_many(data_sql0,sql0)  
    
    # 更新超声心动图
    mysql = db_pymysql(host=host_56
                 ,user=user_56
                 ,password=password_56
                 ,database=database_56
                 ,charset='utf8')
    mysql.insert_data_many(data_sql1,sql1)  
    
    # 更新超声心动图
    mysql = db_pymysql(host=host_56
                 ,user=user_56
                 ,password=password_56
                 ,database=database_56
                 ,charset='utf8')
    mysql.insert_data_many(data_sql2,sql2)

    return sql0,data_sql0,sql1,data_sql1,sql2,data_sql2
    
 
if __name__ == '__main__':
    
#    a = post_structure_examconclusion()
#    df_exam_csxdt = post_struct_binarycontent()
#    b = post_struct_binarycontent()
#    a,aa,aaa,aaaa = post_structure()
    a,b,c,d,e,f = update_data()
#    a = get_current_data()
    
#    sql0,data_sql0,sql1,data_sql1  = post_structure()
#    df_exam_find = post_structure_examfind()

