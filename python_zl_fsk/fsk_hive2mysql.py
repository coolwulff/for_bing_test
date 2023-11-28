# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 16:01:28 2021

@author: LuPengFei
"""
from fsk_hive_connect import db_hive
from fsk_hive2temp import insert_data2mysql_1
#from fsk_hive_sql import sql_lis, sql_2, sql_3, sql_4, sql_5, sql_6, sql_7, sql_8, sql_9, sql_10, sql_11_1,sql_11_2, sql_11_3, sql_11_4, sql_11_5, sql_11_6, sql_11_7, sql_11_8, sql_11_9, sql_11_10, sql_11_11, sql_11_12, sql_11_13  
from fsk_hive_sql_4 import *
from a_temp_sql import *

def create_temp(sql_list=sql_lis):
    '''
    创建临时表
    '''
    db_h = db_hive()
    success = db_h.execute_sql_list(sql_list,close_conn=True)
    
    return success

def get_hive_table(sql):
    db_h = db_hive()
    success, data = db_h.execute_sql(sql,close_conn=True)
    return success, data
    

def hive2mysql(sql, sql_ins):
    
    success, data = get_hive_table(sql)
    if success:
        res = insert_data2mysql_1(sql_ins, data)
        return res
    return 0

def main():
    
    res = []
    # 患者入组
    suc_1 = create_temp(sql_list=sql_lis)
    res.append(suc_1)
    
    # 其他表
    pair = [[sql_2,sql_2_ist],
            [sql_3,sql_3_ist],
            [sql_4_2,sql_4_2_ist],
            [sql_51,sql_51_ist],
            [sql_6,sql_6_ist],
            [sql_7,sql_7_ist],
            [sql_8,sql_8_ist],
            [sql_9,sql_9_ist],
            [sql_10,sql_10_ist],
            [sql_15,sql_15_ist],
            [sql_17,sql_17_ist],
            [sql_19,sql_19_ist],
            [sql_20,sql_20_ist],
            [sql_21,sql_21_ist],
            [sql_180,sql_180_ist],
            [sql_110,sql_110_ist],
            [sql_22,sql_22_ist]]

#    pair = [#[sql_2,sql_2_ist],
#            #[sql_3,sql_3_ist],
#            #[sql_4,sql_4_ist],
#            #[sql_4_2,sql_4_2_ist],
#            [sql_51,sql_51_ist],
#            [sql_6,sql_6_ist],
#            [sql_7,sql_7_ist],
#            [sql_8,sql_8_ist],
#            [sql_9,sql_9_ist],
#            [sql_10,sql_10_ist],
#            [sql_11,sql_11_ist],
#            [sql_15,sql_15_ist],
#            [sql_17,sql_17_ist],
#            [sql_18,sql_18_ist],
#            [sql_19,sql_19_ist]]
    
    mark = 0
    for p,q in pair:
        mark = mark + 1
        print(mark)
        temp = hive2mysql(p,q)
        res.append(temp)
        print('是否执行成功',temp)
        
    if sum(res)==len(res):
        return 1
    return 0

def main_temp():
    # 临时抽取随访数据
    res = []
 
    # 其他表
#    pair = [[sql_18_1,sql_18_ist],
#            [sql_18_2,sql_18_ist],
#            [sql_18_3,sql_18_ist],
#            [sql_18_4,sql_18_ist],
#            [sql_18_5,sql_18_ist],
#            [sql_18_6,sql_18_ist],
#            [sql_18_7,sql_18_ist],
#            [sql_18_8,sql_18_ist]]

    pair = [[sql_16,sql_16_ist],
            [sql_17,sql_17_ist]]
    
    mark = 0
    for p,q in pair:
        mark = mark + 1
        print(mark)
        temp = hive2mysql(p,q)
        res.append(temp)
        print('是否执行成功',temp)
        
    if sum(res)==len(res):
        return 1
    return 0

if __name__ == '__main__':
    success, data = get_hive_table(sql_19)
    aa = insert_data2mysql_1(sql_19_ist, data)
#   a = main_temp()
#    a = main()

    

    
    