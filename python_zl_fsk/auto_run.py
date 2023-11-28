 # -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 17:40:12 2021

@author: LuPengFei
"""

import numpy as np
import pandas as pd
import datetime
import time as t

from q0_qs_drz_patient_temp import insert_data2mysql_0
from q1_form_basic_info import insert_data2mysql_1
from q3_form_diagnose_info_temp import insert_data2mysql_3
from q3_2_form_diagnose_info_followup import insert_data2mysql_3_2
from q4_form_diagnose_detail import insert_data2mysql_4
from q4_2_form_outcome import insert_data2mysql_4_2
from q5_form_operation_info import insert_data2mysql_5
from q6_form_medication_info import insert_data2mysql_6
from q7_form_physical_exam_info import insert_data2mysql_7
from q8_form_ris_info import insert_data2mysql_8
from q9_form_lab_info import insert_data2mysql_9
from q11_form_ris_info_followup import insert_data2mysql_11
from q12_form_lab_info_followup import insert_data2mysql_12
from q14_form_medication_info_followup_new import insert_data2mysql_14
from q15_form_focus_diagnosis_followup import insert_data2mysql_15
from q16_complaint_inhos import insert_data2mysql_16
from q17_complaint_outcome import insert_data2mysql_17
from q18_form_bonedensity import insert_data2mysql_18
from q19_form_renal_biopsy import insert_data2mysql_19
from q20_form_operate_treatement import insert_data2mysql_20

from log import generate_log
def compute_1():
    
    # 模型计算模块
    try:
#        b = 1/0
        insert_data2mysql_0(is_clear_temp = True)
        insert_data2mysql_1(is_clear_1 = True,
                            is_create_2 = False,
                            is_clear_2 = True)
        insert_data2mysql_3(is_clear_temp = False)
        insert_data2mysql_3_2(is_clear_temp = True)
        insert_data2mysql_4(is_clear_temp = True)
        insert_data2mysql_4_2(is_clear_temp = True)
        insert_data2mysql_5(is_clear_temp = True)
        insert_data2mysql_6(is_clear_temp = True)
        insert_data2mysql_7(is_clear_temp = True)
        insert_data2mysql_8(is_clear_temp = True)
        insert_data2mysql_9(is_clear_temp = False)       
        insert_data2mysql_11(is_clear_temp = True) 
        insert_data2mysql_12(is_clear_temp = True) 
        insert_data2mysql_14(is_clear_temp = True) 
        insert_data2mysql_15(is_clear_temp = True) 
        insert_data2mysql_16(is_clear_temp = True) 
        insert_data2mysql_17(is_clear_temp = True) 
        
        try:
            insert_data2mysql_18(is_clear_temp = False)
            print('已处理：18')
        except:
            pass
        
        try:
            insert_data2mysql_19(is_clear_temp = False)
            print('已处理：19')
        except:
            pass
        
        insert_data2mysql_20(is_clear_temp = True)
        
        return 1
    
    except Exception as e:
        logger = generate_log()
        logger.error('%s', e)
        return 0


    
from fsk_hive2mysql import main
from clear_all_temp import truncate_all_temp_table

def auto_run(t_start=1,
             t_end=24):
    
    # 凌晨*点-*点清洗数据数据
    mark = 1
    while 1:      
        time = datetime.datetime.now()
        hour = time.hour
        success = 0
        # 23点执行
        if hour ==15:
            truncate_all_temp_table()
            success = main()
            print('数据是否成功：', success)
            
        #success = 1 #运行时删掉    
        
        #print(is_in,is_out)
        #is_in,is_out = 0,0
        if hour >= t_start and hour < t_end and success:
            print('开始导入数据')
            mark = compute_1()
            print('导入数据成功')
            
        t.sleep(3600)
            
if __name__ == '__main__':
    #num = CheckInDB('data_out')
    auto_run() 