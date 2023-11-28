# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:01:40 2022

@author: LuPengFei
"""

import numpy as np
import pandas as pd

def generate_question_id(): 
    data = pd.read_excel('实验室检验项目名称-20220411.xlsx')
    data['检验项目代码'] = [str(i) for i in data['检验项目代码']]
    data = data[data['是否回填']==1]
    
    data2 = data[['question_id', '表单名称','检验项目代码']]
    data2 = data2.drop_duplicates()
    data2 = data2.reset_index()
    res = {}
    for i in range(len(data2)):
        if data2['检验项目代码'][i] not in res.keys():
            res[data2['检验项目代码'][i]] = data2['question_id'][i]
        else:
            #print(data2['检验项目代码'][i],data2['question_id'][i])
            pass
    
    #res["5729"] = 41
    #res["AMA-M2"] = 41
    
    return res

def generate_question_id_sf(): 
    data = pd.read_excel('实验室检验项目名称-20220411-随访.xlsx')
    data['检验项目代码'] = [str(i) for i in data['检验项目代码']]
    # 过滤不能回填项
    data2 = data[data['是否回填']==1]
    data2 = data2[data2['question_id']>0]
    data2 = data2.reset_index()
    
    data2 = data2[['question_id', '表单名称','检验项目代码']]
    data2 = data2.drop_duplicates()
    data2 = data2.reset_index()
    res = {}
    for i in range(len(data2)):
        if data2['检验项目代码'][i] not in res.keys():
            res[data2['检验项目代码'][i]] = data2['question_id'][i]
        else:
            #print(data2['检验项目代码'][i],data2['question_id'][i])
            pass
    
    #res["5729"] = 41
    #res["AMA-M2"] = 41
    
    return res
    
if __name__ == "__main__":
    a = generate_question_id_sf()