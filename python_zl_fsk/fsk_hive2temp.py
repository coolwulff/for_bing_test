# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 16:43:42 2021

@author: LuPengFei
"""

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56
from log import generate_log

def insert_data2mysql_1(sql, data_sql):

    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    success = 0
    try:
        mysql.insert_data_many(data_sql,sql)
        success = 1
        print('插入临时表成功')
    except Exception as e:
        logger = generate_log()
        logger.error('%s', e)
        print('插入临时表失败')
    return success