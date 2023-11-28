# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 11:13:57 2022

@author: LuPengFei
"""
import numpy as np
import pandas as pd
import datetime

from mysql_connect import db_pymysql,host_56,user_56,password_56,database_56

def get_temp_data():
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    sql_temp = "select * from form_basic_info_temp;"
    df_temp = mysql.get_sql2df(sql_temp)
    
    return df_temp

def get_temp_data2():
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    sql_temp = "select * from form_basic_info_temp2;"
    df_temp = mysql.get_sql2df(sql_temp)
    
    return df_temp

def get_current_data():
    
     mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
     sql_curr = "select * from form_basic_info where hospital_code = '42502657200';"
     df_curr = mysql.get_sql2df(sql_curr)
    
     return df_curr

def preprocess(da):
    '''
    '''
    da = da.replace({'(null)': None})
    da = da.replace({np.nan: None})    

    return da

def compare_data():
    df_temp = get_temp_data2()
    df_curr = get_current_data()
    
#    df_curr = df_curr[0:200]
    
    #找差集
    zd = ['empi', 'patient_no','encounter_id']
#    df_curr['patient_no'] = df_curr.patient_no.astype(str) 
#    df_curr['inpatient_number'] = df_curr.inpatient_number.astype(str) 
    
    df_temp_0 = df_temp[zd]
    n0 = len(df_temp_0)
    df_temp_0['id0'] = [i for i in range(n0)]
    
    df_curr_0 = df_curr[zd]

    n1 = len(df_curr_0)
    df_curr_0['id0'] = [i+n0 for i in range(n1)]
    
    df1 = df_temp_0.append(df_curr_0)
    df1['patient_no'] = df1.patient_no.astype(str)     
    df1['encounter_id'] = df1.encounter_id.astype(str)      
    
    df1 = df1.drop_duplicates(subset=zd,keep=False)
    df1 = df1[df1['id0']<n0]

    idx = df1.index.tolist()
    
    n0 = len(df_temp.columns.tolist())
    a0 = [i for i in range(n0)]
    res = df_temp.iloc[idx,a0]
    res = res.reset_index(drop=True)
    return res 

def generate_input(data):
    '''
    生成插入数据
    param:
    data:dataframe, 经过后处理的数据

    patient_no,
    EMPI, 
    encounter_id, 
    patient_name, 
    sex, 
    countryname,
    nationname, 
    birth, 
    in_hospital_time, 
    out_hospital_time, 
    id_number,
    marriage,
    jobname,
    birth_sheng,
    birth_sheng_code,
    birth_shi,
    birth_shi_code,
    birth_qu,
    birth_qu_code,
    native_sheng,
    native_sheng_code, 
    native_shi,
    native_shi_code,
    current_province_code,
    current_province_name,
    current_city_code, 
    current_city_name,
    current_county_code,
    current_county_name,
    current_addr,
    contact_tel,
    by_tel,
    blood_abo,
    blood_rh,
    payway,
    hospital_code,
    inpatient_number,
    outpatient_number,
    contactphone,
    delete_flag,
    create_date,
    num

    '''
    
    def trans_nation_name(nationname):
        # 民族转换
        if nationname == '汉族':
            return 1
        else:
            return 9
    
    def trans_marriage_code(marriage):
        try:
            if str(int(marriage)) == '1':
                return 10
            elif str(int(marriage)) == '2':
                return 20    
            elif str(int(marriage)) == '3':
                return 30 
            elif str(int(marriage)) == '4':
                return 40 
            elif str(int(marriage)) == '9':
                return 90
            else:
                return marriage
        except:
            return None

    def trans_job_code(job_name):
        # 通过jobname得到工作编码
        if job_name == '国家公务员':
            return 11
        elif job_name == '专业技术人员' or job_name == '农业技术' or job_name == '工程技术':
            return 12   
        elif job_name == '职员' or job_name == '教学人员' or job_name == '行政办公':
            return 13
        elif job_name == '企业管理人员':
            return 14
        elif job_name == '工人':
            return 15
        elif job_name == '农民':
            return 16  
        elif job_name == '学生':
            return 17
        elif job_name == '现役军人':
            return 18
        elif job_name == '自由职业者':
            return 19 
        elif job_name == '个体经营者':
            return 20
        elif job_name == '无业人员' or job_name == '退（离）休人员' or job_name == '无业人员退（离）休人员':
            return 21 
        elif job_name == None:
            return None
        else:
            return 99

    def trans_job_code2(job_code):
        # 通过jobcode得到工作编码
        if job_code == '11':
            return 11
        elif job_code == '13' or job_code == '13':
            return 12   
        elif job_code == '21':
            return 14
        elif job_code == '37':
            return 18
        elif job_code == '51':
            return 19 
        elif job_code == '54':
            return 20
        elif job_code == '70':
            return 21 
        elif job_code == None:
            return None
        else:
            return 99
        
    def trans_blood_abo(blood_abo):
        # abo血型转换
        blood_abo_str = str(blood_abo)
        try:
            if str(int(blood_abo_str)) == '6':
                return '9'
            else:
                return blood_abo
        except:
            return None

        
    # 时间戳
    time = datetime.datetime.now()
    time_str = datetime.datetime.strftime(time,'%Y-%m-%d %H:%M:%S')
    d_insert = []
      
    for i in range(len(data)):
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        encounter_id = data['encounter_id'][i]
        patient_name = data['patient_name'][i]
        sex = data['sex'][i]
        countryname = data['countryname'][i]
        nationname = data['nationname'][i]
        birth = data['birth'][i]      
        in_hospital_time = data['in_hospital_time'][i] 
        out_hospital_time = data['out_hospital_time'][i] 
        id_number = data['id_number'][i]
        marriage = trans_marriage_code(data['marriage'][i])
        jobname = trans_job_code(data['jobname'][i])
        if jobname is None:
            jobcode = data['jobcode'][i]
            jobname = trans_job_code2(jobcode)
        birth_sheng = data['birth_sheng'][i]
        birth_sheng_code = data['birth_sheng_code'][i]
        birth_shi = data['birth_shi'][i]
        birth_shi_code = data['birth_shi_code'][i]
        birth_qu = data['birth_qu'][i]
        birth_qu_code = data['birth_qu_code'][i]
        native_sheng = data['native_sheng'][i]
        native_sheng_code = data['native_sheng_code'][i] 
        native_shi = data['native_shi'][i]
        native_shi_code = data['native_shi_code'][i]
        current_province_code = data['current_province_code'][i]
        current_province_name = data['current_province_name'][i]
        current_city_code = data['current_city_code'][i] 
        current_city_name = data['current_city_name'][i]
        current_county_code = data['current_county_code'][i]
        current_county_name = data['current_county_name'][i]
        current_addr = data['current_addr'][i]
        contact_tel = data['contact_tel'][i]
        by_tel = data['by_tel'][i]
        blood_abo = trans_blood_abo(data['blood_abo'][i])
        blood_rh = data['blood_rh'][i]   
        payway = data['payway'][i]
        hospital_code = data['hospital_code'][i]
        inpatient_number = data['inpatient_number'][i]
        outpatient_number = data['outpatient_number'][i]
        delete_flag = data['delete_flag'][i]
        create_date = time_str

    
        tp = (empi,
            patient_no,
            encounter_id,
            patient_name,
            sex,
            countryname,
            nationname,
            birth,     
            in_hospital_time,
            out_hospital_time,
            id_number,
            marriage,
            jobname,
            birth_sheng,
            birth_sheng_code,
            birth_shi,
            birth_shi_code,
            birth_qu,
            birth_qu_code,
            native_sheng,
            native_sheng_code,
            native_shi,
            native_shi_code,
            current_province_code,
            current_province_name,
            current_city_code,
            current_city_name,
            current_county_code,
            current_county_name,
            current_addr,
            contact_tel,
            by_tel,
            blood_abo,
            blood_rh,
            payway,
            hospital_code,
            inpatient_number,
            outpatient_number,
            delete_flag,
            create_date)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_basic_info_temp2(
            empi,
            patient_no,
            encounter_id,
            patient_name,
            sex,
            countryname,
            nationname,
            birth,     
            in_hospital_time,
            out_hospital_time,
            id_number,
            marriage,
            jobname,
            birth_sheng,
            birth_sheng_code,
            birth_shi,
            birth_shi_code,
            birth_qu,
            birth_qu_code,
            native_sheng,
            native_sheng_code,
            native_shi,
            native_shi_code,
            current_province_code,
            current_province_name,
            current_city_code,
            current_city_name,
            current_county_code,
            current_county_name,
            current_addr,
            contact_tel,
            by_tel,
            blood_abo,
            blood_rh,
            payway,
            hospital_code,
            inpatientnumber,
            outpatientnumber,
            delete_flag,
            create_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    '''
    return sql, d_insert

def generate_input2():
    '''
    待修改
    
    临时表插入到对应的表
    param:
    data:dataframe, 经过后处理的数据

    empi,
    empi_old,
    patient_no,
    encounter_id,
    patient_name,
    id_number,
    nation_code,
    nation_name,
    job_code,
    job_name,
    marriage_id,
    marriage_name,
    marriage,
    hospital_name,
    hospital_code,
    inpatient_number,
    outpatient_number,
    hukou_province_code,
    hukou_province_name,
    hukou_city_code,
    hukou_city_name ,
    hukou_county_code,
    hukou_county_name ,
    hukou_addr,
    native_province_code,
    native_province_name,
    native_city_code ,
    native_city_name ,
    native_county_code ,
    native_county_name ,
    current_province_code ,
    current_province_name ,
    current_city_code ,
    current_city_name ,
    current_county_code ,
    current_county_name ,
    current_addr ,
    current_tel ,
    contact_tel,
    contact_name ,
    contactrelation_name ,
    contactrelation_code,
    create_date
    '''
    
    def trans_nation_name(nationname):
        # 民族转换
        if nationname == '汉族':
            return 1
        else:
            return 9    
    # 时间戳
    data = compare_data()
    
    d_insert = []
    for i in range(len(data)):
        empi = data['empi'][i]
        patient_no = data['patient_no'][i]
        encounter_id = data['encounter_id'][i]
        patient_name = data['patient_name'][i]
        sex = data['sex'][i]
        countryname = data['countryname'][i]
        nation_detail = data['nationname'][i]
        nationname = trans_nation_name(data['nationname'][i])
        birth = data['birth'][i]      
        in_hospital_time = data['in_hospital_time'][i] 
        out_hospital_time = data['out_hospital_time'][i] 
        id_number = data['id_number'][i]
        marriage = data['marriage'][i]
        jobname = data['jobname'][i]
        birth_sheng = data['birth_sheng'][i]
        birth_sheng_code = data['birth_sheng_code'][i]
        birth_shi = data['birth_shi'][i]
        birth_shi_code = data['birth_shi_code'][i]
        birth_qu = data['birth_qu'][i]
        birth_qu_code = data['birth_qu_code'][i]
        native_sheng = data['native_sheng'][i]
        native_sheng_code = data['native_sheng_code'][i] 
        native_shi = data['native_shi'][i]
        native_shi_code = data['native_shi_code'][i]
        current_province_code = data['current_province_code'][i]
        current_province_name = data['current_province_name'][i]
        current_city_code = data['current_city_code'][i] 
        current_city_name = data['current_city_name'][i]
        current_county_code = data['current_county_code'][i]
        current_county_name = data['current_county_name'][i]
        current_addr = data['current_addr'][i]
        contact_tel = data['contact_tel'][i]
        by_tel = data['by_tel'][i]
        
        #update form_basic_info a set a.blood_rh = left(a.blood_rh, 1)  where length(a.blood_rh)>0;
        #update form_basic_info a set a.blood_abo = left(a.blood_abo, 1)  where length(a.blood_abo)>0;
        
        blood_abo = data['blood_abo'][i]
        blood_rh = data['blood_rh'][i] 
        
        # 去blood_abo和blood_rh空格
        if blood_abo is not None:
            blood_abo = blood_abo.strip()

        if blood_rh is not None:
            blood_rh = blood_rh.strip()
            
        payway = data['payway'][i]
        hospital_code = data['hospital_code'][i]
        inpatient_number = data['inpatientnumber'][i]
        outpatient_number = data['outpatientnumber'][i]
        delete_flag = data['delete_flag'][i]
        create_date = data['create_date'][i]

    
        tp = (empi,
            patient_no,
            encounter_id,
            patient_name,
            sex,
            countryname,
            nationname,
            birth,     
            in_hospital_time,
            out_hospital_time,
            id_number,
            marriage,
            jobname,
            birth_sheng,
            birth_sheng_code,
            birth_shi,
            birth_shi_code,
            birth_qu,
            birth_qu_code,
            native_sheng,
            native_sheng_code,
            native_shi,
            native_shi_code,
            current_province_code,
            current_province_name,
            current_city_code,
            current_city_name,
            current_county_code,
            current_county_name,
            current_addr,
            contact_tel,
            by_tel,
            blood_abo,
            blood_rh,
            payway,
            hospital_code,
            inpatient_number,
            outpatient_number,
            delete_flag,
            create_date,
            nation_detail)
        
        tp = (str(i) if i is not None else i for i in tp)
        tp = tuple(list(tp))
        d_insert.append(tp)
        
    sql = '''
    insert into form_basic_info(
            empi,
            patient_no,
            encounter_id,
            patient_name,
            sex,
            countryname,
            nationname,
            birth,     
            in_hospital_time,
            out_hospital_time,
            id_number,
            marriage,
            jobname,
            birth_sheng,
            birth_sheng_code,
            birth_shi,
            birth_shi_code,
            birth_qu,
            birth_qu_code,
            native_sheng,
            native_sheng_code,
            native_shi,
            native_shi_code,
            current_province_code,
            current_province_name,
            current_city_code,
            current_city_name,
            current_county_code,
            current_county_name,
            current_addr,
            contact_tel,
            by_tel,
            blood_abo,
            blood_rh,
            payway,
            hospital_code,
            inpatientnumber,
            outpatientnumber,
            delete_flag,
            create_date,
            nation_detail) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
    '''
    return sql, d_insert

def sql_list_1():
    sql_clear = '''
    truncate table form_basic_info_temp;
    '''
    
    return sql_clear

def sql_list_2():
    # 待修改
    
    # 建表
    sql_create = '''DROP TABLE if exists form_basic_info_temp2;
CREATE TABLE IF NOT EXISTS form_basic_info_temp2(
`id` int(8) NOT NULL AUTO_INCREMENT COMMENT '病案首页ID',
`empi` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'EMPI',
`patient_no` int(20) NOT NULL COMMENT '患者ID',
`encounter_id` int(20) NOT NULL COMMENT '住院就诊ID',
`patient_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '姓名',
`sex` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '性别',
`countryname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '国籍名称',
`nationname` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '民族',
`birth` date NULL DEFAULT NULL COMMENT '出生日期',
`in_hospital_time` date NULL DEFAULT NULL COMMENT '入院时间',
`out_hospital_time` date NULL DEFAULT NULL COMMENT '出院时间',
`id_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '身份证号',
`marriage` char(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '婚姻',
`whcd` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文化程度',
`jobname` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '职业',
`birth_sheng` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地省份',
`birth_sheng_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地省份编码',
`birth_shi` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地市',
`birth_shi_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地市编码',
`birth_qu` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地区县',
`birth_qu_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地区县编码',
`birth_xz` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地乡镇街道',
`birth_xz_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地乡镇街道编码',
`birth_cun` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地村居委会',
`birth_cun_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '出生地村居委会编码',
`native_sheng` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯省份',
`native_sheng_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯省份编码',
`native_shi` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯市',
`native_shi_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯市编码',
`native_qu` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯区县',
`native_qu_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯区县编码',
`native_xz` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯乡镇街道',
`native_xz_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯乡镇街道编码',
`native_cun` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯村居委会',
`native_cun_code` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '籍贯村居委会编码',
`current_province_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '（家庭）\r\n现住址省代码\r\n',
`current_province_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '（家庭）\r\n现住址省名称\r\n',
`current_city_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '（家庭）\r\n现住址市代码\r\n',
`current_city_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '（家庭）\r\n现住址市名称\r\n',
`current_county_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '（家庭）\r\n现住址县代码\r\n',
`current_county_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '（家庭）\r\n现住址县名称\r\n',
`current_addr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '（家庭）\r\n现住址详细地址\r\n',
`contact_tel` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '联系电话',
`by_tel` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备用电话',
`blood_abo` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'abo血型',
`blood_rh` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'rh血型',
`inpatientnumber` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '住院号',
`payway` char(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '医疗付费方式',
`outpatientnumber` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '门诊号',
`is_dead` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '是否死亡',
`hospital_code` varchar(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '组织机构代码',
`create_date` datetime(6) NULL DEFAULT NULL COMMENT '创建日期',
`update_date` datetime(6) NULL DEFAULT NULL COMMENT '更新日期',
`last_update_date` datetime(6) NULL DEFAULT NULL COMMENT '上次更新日期',
`delete_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志',
PRIMARY KEY (`id`) USING BTREE,
INDEX `id_index`(`empi`) USING BTREE
);
    '''
    #sql_create = sql_create.replace('\n', '')
    # 清空表
    sql_clear = '''
    truncate table form_basic_info_temp2;
    '''
#    sql_update = '''
#update form_basic_info_temp2 a set a.birth_qu_code = a.birth_shi_code, a.birth_qu = (select name from dic_district b where b.code = a.birth_shi_code) WHERE a.birth_qu_code is NULL and a.birth_qu is NULL;
#update form_basic_info_temp2 a set a.birth_qu = (select name from dic_district b where b.code = a.birth_qu_code) WHERE a.birth_qu_code is not NULL and a.birth_qu is NULL;
#update form_basic_info_temp2 a set a.birth_shi = (select name from dic_city b where b.code = left(a.birth_shi_code, 4)), a.birth_shi_code = left(a.birth_shi_code, 4) WHERE a.birth_shi is NULL;
#update form_basic_info_temp2 a set a.birth_shi = (select name from dic_city b where b.code = left(a.birth_shi_code, 4)), a.birth_shi_code = left(a.birth_shi_code, 4);
#update form_basic_info_temp2 a set a.birth_sheng_code = left(a.birth_sheng_code, 2);
#update form_basic_info_temp2 a set a.current_county_code = a.current_city_code, a.current_county_name = (select name from dic_district b where b.code = a.current_city_code) WHERE a.current_county_code is NULL and a.current_county_name is NULL;
#update form_basic_info_temp2 a set a.current_county_name = (select name from dic_district b where b.code = a.current_county_code) WHERE a.current_county_code is not NULL and a.current_county_name is NULL;
#update form_basic_info_temp2 a set a.current_city_name = (select name from dic_city b where b.code = left(a.current_city_code, 4)), a.current_city_code = left(a.current_city_code, 4) WHERE a.current_city_name is NULL;
#update form_basic_info_temp2 a set a.current_city_name = (select name from dic_city b where b.code = left(a.current_city_code, 4)), a.current_city_code = left(a.current_city_code, 4);
#update form_basic_info_temp2 a set a.current_province_code = left(a.current_province_code, 2);
#UPDATE form_basic_info_temp2 set birth_qu_code = NULL WHERE birth_qu_code is not NULL and birth_qu is NULL;
#UPDATE form_basic_info_temp2 set current_county_code = NULL WHERE current_county_code is not NULL and current_county_name is NULL;
#update form_basic_info_temp2 a set a.native_sheng_code = left(a.native_sheng_code, 2);
#update form_basic_info_temp2 a set a.native_qu_code = a.native_shi_code, a.native_qu = (select name from dic_district b where b.code = a.native_shi_code);
#UPDATE form_basic_info_temp2 set native_qu_code = NULL WHERE native_qu is NULL;
#update form_basic_info_temp2 a set a.native_shi = (select name from dic_city b where b.code = left(a.native_shi_code, 4)), a.native_shi_code = left(a.native_shi_code, 4) WHERE a.native_shi is NULL;
#update form_basic_info_temp2 a set a.native_shi = (select name from dic_city b where b.code = left(a.native_shi_code, 4)), a.native_shi_code = left(a.native_shi_code, 4);  
#update form_basic_info_temp2 a, dic_province b set a.birth_sheng_code = b.code where a.birth_sheng = b.name and a.birth_sheng_code is null;
#update form_basic_info_temp2 a, dic_province b set a.native_sheng_code = b.code where a.native_sheng = b.name and a.native_sheng_code is null;
#update form_basic_info_temp2 a, dic_province b set a.current_province_code = b.code where a.current_province_name = b.name and a.current_province_code is null;
#update form_basic_info a, dic_province b set a.birth_sheng_code = b.code where a.birth_sheng = b.name and a.birth_sheng_code is null;
#update form_basic_info a, dic_province b set a.native_sheng_code = b.code where a.native_sheng = b.name and a.native_sheng_code is null;
#update form_basic_info a, dic_province b set a.current_province_code = b.code where a.current_province_name = b.name and a.current_province_code is null;
#    '''
    

    sql_update = [
            "update form_basic_info_temp2 a set a.birth_qu_code = a.birth_shi_code, a.birth_qu = (select name from dic_district b where b.code = a.birth_shi_code) WHERE a.birth_qu_code is NULL and a.birth_qu is NULL;"
            ,"update form_basic_info_temp2 a set a.birth_qu = (select name from dic_district b where b.code = a.birth_qu_code) WHERE a.birth_qu_code is not NULL and a.birth_qu is NULL;"
            ,"update form_basic_info_temp2 a set a.birth_shi = (select name from dic_city b where b.code = left(a.birth_shi_code, 4)), a.birth_shi_code = left(a.birth_shi_code, 4) WHERE a.birth_shi is NULL;"
            ,"update form_basic_info_temp2 a set a.birth_shi = (select name from dic_city b where b.code = left(a.birth_shi_code, 4)), a.birth_shi_code = left(a.birth_shi_code, 4);"
            ,"update form_basic_info_temp2 a set a.birth_sheng_code = left(a.birth_sheng_code, 2);"
            ,"update form_basic_info_temp2 a set a.current_county_code = a.current_city_code, a.current_county_name = (select name from dic_district b where b.code = a.current_city_code) WHERE a.current_county_code is NULL and a.current_county_name is NULL;"
            ,"update form_basic_info_temp2 a set a.current_county_name = (select name from dic_district b where b.code = a.current_county_code) WHERE a.current_county_code is not NULL and a.current_county_name is NULL;"
            ,"update form_basic_info_temp2 a set a.current_city_name = (select name from dic_city b where b.code = left(a.current_city_code, 4)), a.current_city_code = left(a.current_city_code, 4) WHERE a.current_city_name is NULL;"
            ,"update form_basic_info_temp2 a set a.current_city_name = (select name from dic_city b where b.code = left(a.current_city_code, 4)), a.current_city_code = left(a.current_city_code, 4);"
            ,"update form_basic_info_temp2 a set a.current_province_code = left(a.current_province_code, 2);"
            ,"UPDATE form_basic_info_temp2 set birth_qu_code = NULL WHERE birth_qu_code is not NULL and birth_qu is NULL;"
            ,"UPDATE form_basic_info_temp2 set current_county_code = NULL WHERE current_county_code is not NULL and current_county_name is NULL;"
            ,"update form_basic_info_temp2 a set a.native_sheng_code = left(a.native_sheng_code, 2);"
            ,"update form_basic_info_temp2 a set a.native_qu_code = a.native_shi_code, a.native_qu = (select name from dic_district b where b.code = a.native_shi_code);"
            ,"UPDATE form_basic_info_temp2 set native_qu_code = NULL WHERE native_qu is NULL;"
            ,"update form_basic_info_temp2 a set a.native_shi = (select name from dic_city b where b.code = left(a.native_shi_code, 4)), a.native_shi_code = left(a.native_shi_code, 4) WHERE a.native_shi is NULL;"
            ,"update form_basic_info_temp2 a set a.native_shi = (select name from dic_city b where b.code = left(a.native_shi_code, 4)), a.native_shi_code = left(a.native_shi_code, 4);"
            ,"update form_basic_info_temp2 a, dic_province b set a.birth_sheng_code = b.code where a.birth_sheng = b.name and a.birth_sheng_code is null;"
            ,"update form_basic_info_temp2 a, dic_province b set a.native_sheng_code = b.code where a.native_sheng = b.name and a.native_sheng_code is null;"
            ,"update form_basic_info_temp2 a, dic_province b set a.current_province_code = b.code where a.current_province_name = b.name and a.current_province_code is null;"
            ,"update form_basic_info a, dic_province b set a.birth_sheng_code = b.code where a.birth_sheng = b.name and a.birth_sheng_code is null;"
            ,"update form_basic_info a, dic_province b set a.native_sheng_code = b.code where a.native_sheng = b.name and a.native_sheng_code is null;"
            ,"update form_basic_info a, dic_province b set a.current_province_code = b.code where a.current_province_name = b.name and a.current_province_code is null;"
    ]
    
    return sql_create, sql_clear, sql_update

from log import generate_log
def insert_data2mysql_1(is_clear_1 = False,
                        is_create_2 = False,
                        is_clear_2 = False):
    da = get_temp_data()
    data = preprocess(da)
    sql, data_sql = generate_input(data=data)
    
    mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
    
    sql_clear_1 = sql_list_1()
    
    sql_create_2, sql_clear_2, sql_update = sql_list_2()    
    # 建表
    if is_create_2:
        mysql.execute_sql(sql_create_2)
    
    # 清空表temp2
    if is_clear_2:
        mysql.execute_sql(sql_clear_2)
 
    try:
        mysql.insert_data_many(data_sql,sql)
        
        # 更新数据，插入到temp2
        for s in sql_update:
            mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
            mysql.update_sql(s)
        
        # 插入增量数据到form_basic_info
        mysql = db_pymysql(host=host_56
                     ,user=user_56
                     ,password=password_56
                     ,database=database_56
                     ,charset='utf8')
        sql, data_sql = generate_input2()
        mysql.insert_data_many(data_sql,sql)

        # 清空临时表1
        if is_clear_1:
            mysql = db_pymysql(host=host_56
                         ,user=user_56
                         ,password=password_56
                         ,database=database_56
                         ,charset='utf8')
            mysql.execute_sql(sql_clear_1)
        
        return sql, data_sql
    except Exception as e:
        logger = generate_log()
        logger.error('%s', e)
        
        return sql, data_sql

if __name__ == '__main__':
#    a = compare_data()
    
    a,b = insert_data2mysql_1(is_clear_1 = False,
                        is_create_2 = True,
                        is_clear_2 = True)


