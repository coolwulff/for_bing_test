# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 11:24:52 2023

@author: LuPengFei
"""
from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def truncate_all_temp_table():
    sql_clear_all = ['truncate table qs_drz_patient_temp;'
                    ,'truncate table form_basic_info_temp;'
                    ,'truncate table form_basic_info_temp2;'
                    ,'truncate table qs_admission_history_temp;'
                    ,'truncate table form_qs_zg_temp;'
                    ,'truncate table form_diagnose_info_51_temp;'
                    ,'truncate table form_diagnose_detail_temp;'
                    ,'truncate table form_operation_info_temp;'
                    ,'truncate table form_medication_info_temp;'
                    ,'truncate table form_physical_exam_info_temp;'
                    ,'truncate table form_ris_info_temp;'
                    ,'truncate table form_lab_info_temp;'
                    ,'truncate table cdr_patient_info_temp;'
                    ,'truncate table form_focus_diagnosis_followup_temp;'
                    ,'truncate table form_medication_info_followup_temp;'
                    ,'truncate table form_lab_info_followup_temp;'
                    ,'truncate table form_ris_info_followup_temp;'
                    ,'truncate table form_complaint_inhos_temp;'
                    ,'truncate table form_complaint_outcome_temp;']
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    print("清空临时表")
    for sql in sql_clear_all:
        try:
            mysql.execute_sql(sql)
        except:
            print('临时表清空失败：' + sql)
        
    


