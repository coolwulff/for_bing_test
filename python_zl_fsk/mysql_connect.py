# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 09:58:01 2021

@author: LuPengFei
"""

import pymysql
import pandas as pd
from pymysql.constants import CLIENT

# 113服务器：'10.1.192.113'  'root' '123456' 'rheumatism_questionnaire'

#
#host_56 = '10.1.192.113'
#user_56 = 'root'
#password_56 = '123456'
#database_56 = 'rheumatism_questionnaire'


host_56 = '172.28.17.238'
user_56 = 'sjkdatazh'
password_56 = '5dg=ycnngMVh'
database_56 = 'rheumatism_questionnaire'

class db_pymysql:

    
    def __init__(self
                 ,host=host_56
                 ,user=user_56
                 ,password=password_56
                 ,database=database_56
                 ,charset='utf8'):
        
        self.host = host
        self.user = user       
        self.password = password       
        self.database = database
        self.charset = charset

        self.conn = self.connect_db()
    
    def __latin_gbk(self, x):
        try:
            return x.encode('latin-1').decode('gbk')
        except:
            return x
        
    def __trans_latin(self, df):
        trans = lambda x: self.__latin_gbk(x)
        return df.applymap(trans)
    
    def sql2dataframe(self, sql, conn):
        return self.__trans_latin(pd.read_sql(sql, con=conn))
    
    def connect_db(self):
        # 连接数据库
        try:
            conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    charset=self.charset,
                    database=self.database,
                    client_flag=CLIENT.MULTI_STATEMENTS)     #库名
            return conn
        except pymysql.Error as e:
            print (e)
            return None        
        
    def get_sql2df(self, sql):
        # 执行sql查询，返回dataframe数据
        df = self.sql2dataframe(sql,
                                self.conn)
        
        return df
    
    def check_db_exists(self, sql):
        # 检查数据库中是否存在数据
        df = len(self.get_sql2df(sql))
        
        if len(df) == 0:
            return 0,df
        else:
            return 1, df
    
    def insert_data_many(self, data, ins_sql):
        # 一次向数据库中插入多条数据
        cursor = self.conn.cursor()
        
        try:
            cursor.executemany(ins_sql,data)
            self.conn.commit()
            print('插入成功')
        except Exception as e:
            print(e)
            self.conn.rollback()
            print('插入失败')
        finally:
            self.conn.close() 
    
    def execute_sql(self,sql,
                    close_conn=False):
        
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            print('执行成功')
        except Exception as e:
            print(e)
            print('执行失败')
        finally:
            if close_conn:
                self.conn.close() 
    
    def update_sql(self,sql):
        cursor = self.conn.cursor()
        
        try:
            cursor.execute(sql)
            self.conn.commit()
            print('更新成功')
        except Exception as e:
            print(e)
            self.conn.rollback()
            print('更新失败')
        finally:
            self.conn.close()
            
    def execute_sql_with_return(self,sql,
                    close_conn=False):
        
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            print('执行成功')
            return 1
        except Exception as e:
            print(e)
            print('执行失败')
            return 0
        finally:
            if close_conn:
                self.conn.close()             