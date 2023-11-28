# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 15:37:35 2021

@author: LuPengFei
"""
from pyhive import hive
from log import generate_log
import pandas as pd


class db_hive:
    
    host_h = '172.28.18.124'
    port_h = 10000
    auth_h = "CUSTOM"
    db_h = 'default'
    user_h = 'hive'
    psw_h ='123456'
    
    def __init__(self
                 ,host=host_h
                 ,port=port_h
                 ,auth=auth_h
                 ,database=db_h
                 ,user=user_h
                 ,password=psw_h):
        
        self.host = host
        self.port = port
        self.auth = auth
        self.user = user       
        self.password = password       
        self.database = database

        self.conn = self.connect_db()
    
    def connect_db(self):
        # 连接数据库
        try:
            conn = hive.Connection(host=self.host,
                                   port=self.port,
                                   auth=self.auth,
                                   database=self.database,
                                   username=self.user,
                                   password=self.password)
            return conn
        except Exception as e:
            logger = generate_log()
            logger.error('%s', e)
            return None        

    
    def execute_sql(self,sql,
                    close_conn=False):
        
        cursor = self.conn.cursor()
        
        res = []        
        try:
            cursor.execute('set hive.execution.engine=spark')
            cursor.execute(sql)
            print('执行成功')
            success = 1
            
            # 返回值
            for d0 in cursor.fetchall():
                #d0 = (str(i) if i != '(null)' else None for i in d0)
                d1 = [str(i) if i != '(null)' else None for i in d0]
                d1 = [i if i!='None' else None for i in d1]
                d1 = tuple(d1)
                res.append(d1)
            
        except Exception as e:
            logger = generate_log()
            logger.error('%s', e)
            print('执行失败')
            success = 0
        finally:
            if close_conn:
                self.conn.close() 
        
        return success,res

    def execute_sql_list(self,sql_list,
                    close_conn=False):
        
        cursor = self.conn.cursor()
        try:
            cursor.execute('set hive.execution.engine=spark')
            for sql in sql_list: 
                cursor.execute(sql)
            print('执行成功')
            success = 1
        except Exception as e:
            logger = generate_log()
            logger.error('%s', e)
            print('执行失败')
            success = 0
        finally:
            if close_conn:
                self.conn.close() 
                
        return success
    
    def excute_sql2df(self,sql,
                    close_conn=False):

        cursor = self.conn.cursor()
        
        res = []        
        try:
            cursor.execute('set hive.execution.engine=spark')
            cursor.execute(sql)
            print('执行成功')
            success = 1
            
            # 返回值
            # 读取字段列名
            index = cursor.description
            row = list()
            for i in range(len(index)):
            	row.append(index[i][0])
              #获取返回信息
            data = cursor.fetchall()
            res = pd.DataFrame(list(data), columns = row)

            
        except Exception as e:
            logger = generate_log()
            logger.error('%s', e)
            print('执行失败')
            success = 0
        finally:
            if close_conn:
                self.conn.close() 
        
        return success,res
    
if __name__ == '__main__':
    a = db_hive()