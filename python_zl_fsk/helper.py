# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 17:54:49 2022

@author: LuPengFei
"""

import numpy as np
import pandas as pd
import datetime
    

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def get_grouped_data():
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    sql_temp = "select * from qs_drz_patient where is_grouped = 1 and hospital_code = '42502657200';"
    df_temp = mysql.get_sql2df(sql_temp)
    
    return df_temp

def get_empi_condition():
    
    a = get_grouped_data()   
    empi_all = "("
    
    for i in range(len(a)):
        empi_all = empi_all + "'"+ a["empi"][i] + "'"+ ","
    empi_all = empi_all[:-1] + ')'
    
    condition_str = "empi in " + empi_all + ";"
    
    return condition_str

def trans_sql_add_condition(sql):
    
    if "where" in sql:
        return sql[:-1] + " and " + get_empi_condition()
    else:
        return sql[:-1] + " where " + get_empi_condition()

if __name__ == '__main__':
    sql = "select a from b where;"
    a = trans_sql_add_condition(sql)
    
    