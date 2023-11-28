# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 16:27:17 2021

@author: LuPengFei
"""

# 2020-11-30
#in_hospitaldate_first = '2018-12-31'
in_hospitaldate_first = '2020-11-30'
## 1- 患者入组

# 筛选风湿入组患者
sql_1_00 = 'DROP TABLE IF EXISTS skzbk.fs_medicalrecordmain_ls_temp'


# 加时间约束,科室条件是这几个：免疫学专业、日间病房(南)、风湿科(南)、其他业务科室、风湿科（A类）(南)、A类11F病房
#还要再加个条件：住院记录中存在过住院时间大于1天的
 # 加时间约束,修改为病案首页诊断，去除妊娠期诊断编码，加科室约束
sql_1_01 = '''
CREATE TABLE skzbk.fs_medicalrecordmain_ls_temp AS 
select m.empi, c.MedicalRecordID, a.inhospitaldeptcode, a.InHospitalDeptName, a.OutHospitalDeptName, a.inhospitalwardname, a.EncounterID, a.patientno, a.patientname, a.inpatientnumber, to_date(a.inhospitaltime) AS inhospitaltime, to_date(a.OutHospitalTime) AS OutHospitalTime, to_date(c.OperateDate) as OperateDate, c.OperateCODE, c.OperateName, c.operateidx, c.operatedoctorname, c.operatefirstname, concat_ws(';', collect_set(replace(b.diagnosecode,'，','，'))) as diagnosecode, concat_ws(';', collect_set(replace(b.diagnosename,'，','，'))) as diagnosename 
from cdr_v_MedicalRecordMain a 
join 
(SELECT * FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) b 
on a.id = b.MedicalRecordID
left join 
(select MedicalRecordID, OperateDate, OperateCODE, OperateName, operateidx, operatedoctorname,operatefirstname FROM cdr_v_MedicalRecordOperate) c 
on a.id = c.MedicalRecordID 
join (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) m 
on a.patientno = m.patientno 
group by m.empi, c.MedicalRecordID, a.inhospitaldeptcode, a.InHospitalDeptName, a.OutHospitalDeptName, a.inhospitalwardname, a.EncounterID, a.patientno, a.patientname, a.inpatientnumber, to_date(a.inhospitaltime), to_date(a.outhospitaltime), to_date(c.OperateDate), c.OperateCODE, c.OperateName, c.operateidx, c.operatedoctorname, c.operatefirstname
having to_date(a.inhospitaltime) > to_date('%s') and datediff(to_date(a.outhospitaltime), to_date(a.inhospitaltime)) > 1 and TRIM(a.InHospitalDeptName) in ('免疫学专业','日间病房(南)','风湿科(南)','其他业务科室','风湿科（A类）(南)','A类11F病房')
''' % in_hospitaldate_first
# and a.InHospitalDeptName in ('免疫学专业','日间病房(南)','风湿科(南)','其他业务科室','风湿科（A类）(南)','A类11F病房')


sql_1_02 = 'DROP TABLE IF EXISTS skzbk.fs_medicalrecordmain_ls_temp2'
sql_1_03 = '''
CREATE TABLE skzbk.fs_medicalrecordmain_ls_temp2 AS 
select a.id, m.empi,a.inhospitaldeptcode, a.InHospitalDeptName, a.OutHospitalDeptName, a.inhospitalwardname, a.EncounterID, a.patientno, a.patientname, a.inpatientnumber, to_date(a.inhospitaltime) AS inhospitaltime, to_date(a.OutHospitalTime) AS OutHospitalTime,concat_ws(';', collect_set(replace(b.diagnosecode,'，','，'))) as diagnosecode, concat_ws(';', collect_set(replace(b.diagnosename,'，','，'))) as diagnosename 
from cdr_v_MedicalRecordMain a 
join 
(SELECT * FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) b 
on a.id = b.MedicalRecordID 
join (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) m 
on a.patientno = m.patientno 
group by a.id, m.empi, a.inhospitaldeptcode, a.InHospitalDeptName, a.OutHospitalDeptName, a.inhospitalwardname, a.EncounterID, a.patientno, a.patientname, a.inpatientnumber, to_date(a.inhospitaltime), to_date(a.outhospitaltime)
'''

# 关联患者信息
sql_1_10 = '''
DROP TABLE IF EXISTS skzbk.fs_INPATIENTNUMBER_LS_TEMP0
'''

sql_1_11 = '''
CREATE TABLE skzbk.fs_INPATIENTNUMBER_LS_TEMP0 AS 
SELECT NVL(B.EMPI, A.patientno) AS EMPI, B.EMPI AS EMPI_OLD, A.medicalrecordid, A.inhospitaldeptcode, A.inhospitaldeptname, A.outhospitaldeptname, A.inhospitalwardname, A.encounterid, A.patientno, A.patientname, A.inpatientnumber, A.inhospitaltime, A.outhospitaltime, A.operatedate, A.operatecode, A.operatename, A.operateidx, A.operatedoctorname, A.operatefirstname, A.diagnosecode, A.diagnosename FROM skzbk.fs_medicalrecordmain_ls_temp A 
LEFT JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) B 
ON A.patientno=B.patientno
'''

# 加工唯一键，并对同一人手术按手术时间排序
sql_1_20 = '''
DROP TABLE IF EXISTS skzbk.fs_INPATIENTNUMBER_LS_TEMP
'''

sql_1_21 = '''
CREATE TABLE skzbk.fs_INPATIENTNUMBER_LS_TEMP AS
SELECT B.*, CONCAT(B.MedicalRecordID, '#', B.operateidx) AS KEY_ID, CONCAT(YEAR(B.operatedate), '-', Lpad(B.YEAR_RN, 4, '0')) AS operationnum FROM 
(select a.*, row_number() over(partition by a.empi order by a.inhospitaltime, a.operatedate, a.operateidx) as rn, row_number() over(partition by year(a.inhospitaltime) order by a.inhospitaltime ) as year_rn FROM skzbk.fs_INPATIENTNUMBER_LS_TEMP0 a) B
'''

# 病案首页数据处理
sql_1_30 = '''
DROP TABLE IF EXISTS skzbk.fs_MEDICALRECORDMAIN_TEMP
'''

sql_1_31 = '''
CREATE TABLE skzbk.fs_MEDICALRECORDMAIN_TEMP AS
SELECT A.ID, A.PatientNo, A.RecordNumber, A.EncounterID, A.InpatientNumber, A.PatientName AS XM, A.AGE AS NL, A.ShowAge, CASE WHEN TRIM(A.SEX) IN ('1','2') THEN TRIM(A.SEX) WHEN A.IDNumber rlike '(^[1-9]\\d{5}(18|19|([23]\\d))\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$)|(^[1-9]\\d{5}\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}$)' THEN CASE WHEN PMOD(SUBSTR(A.IDNumber, 15, 3), 2) = 1 THEN '1' WHEN PMOD(SUBSTR(A.IDNumber, 15, 3), 2) = 0 THEN '2' ELSE '0' END ELSE '0' END AS XB, TO_DATE(A.Birth) AS Birth, A.NationName, nvl(B.CODE, '99') as mz, CASE WHEN TRIM(A.Marriage) IN ('1', '2', '3', '4') THEN TRIM(A.Marriage) ELSE '9' END AS HYZK, A.IDNumber AS sfzhm, NVL(A.JobName, '') AS zy, C.wj_jobcode, A.ContactName AS LXRXM, A.ContactRelationName AS LXRGX, A.ContactTel AS LXRDH, A.ABO, CASE WHEN TRIM(A.ABO) IN ('1', '2') THEN TRIM(A.ABO) WHEN TRIM(A.ABO) = '3' THEN '4' WHEN TRIM(A.ABO) = '4' THEN '3' ELSE '5' END AS XX, A.Rh AS OLD_RH, CASE WHEN TRIM(A.Rh) = '1' THEN '2' WHEN TRIM(A.Rh) = '2' THEN '1' ELSE '3' END AS RH 
FROM cdr_V_MedicalRecordMain A 
LEFT JOIN (SELECT CODE, NAME FROM qs_wexzl_all_dic WHERE dic_type='民族字典表') B 
ON A.NationNAME = B.NAME 
LEFT JOIN WEXZL_JOB_MAPPING_DIC C 
ON TRIM(A.JobCODE)=C.cdr_jobcode
'''
# 行政区域
sql_1_40 = '''
drop table skzbk.fs_REGIONAL_LS_temp
'''

sql_1_41 = '''
create table skzbk.fs_REGIONAL_LS_temp as 
select A.ID, A.PatientNo, A.RecordNumber, A.InpatientNumber, HukouProvinceCode, HukouProvinceName, HukouCityCode, HukouCityName, HukouCountyCode, HukouCountyName, HukouAddr, i.level_one_code AS level_one_code_HK, i.level_one_name AS level_one_name_HK, case when h.level_one_code = i.level_one_code then h.level_two_code end as level_two_code_HK, case when h.level_one_code = i.level_one_code then h.level_two_name end as level_two_name_HK, case when g.level_two_code = h.level_two_code and h.level_one_code = i.level_one_code then g.level_three_code when f.level_two_code = h.level_two_code and h.level_one_code = i.level_one_code then f.level_three_code end as level_three_code_HK, case when g.level_two_code = h.level_two_code and h.level_one_code = i.level_one_code then g.level_three_name when f.level_two_code = h.level_two_code and h.level_one_code = i.level_one_code then f.level_three_name end as level_three_name_HK, CurrentProvinceCode, CurrentProvinceName, CurrentCityCode, CurrentCityName, CurrentCountyCode, CurrentCountyName, e.level_one_code, e.level_one_name, case when d.level_one_code = e.level_one_code then d.level_two_code end as level_two_code, case when d.level_one_code = e.level_one_code then d.level_two_name end as level_two_name, case when c.level_two_code = d.level_two_code and d.level_one_code = e.level_one_code then c.level_three_code when b.level_two_code = d.level_two_code and d.level_one_code = e.level_one_code then b.level_three_code end as level_three_code, case when c.level_two_code = d.level_two_code and d.level_one_code = e.level_one_code then c.level_three_name when b.level_two_code = d.level_two_code and d.level_one_code = e.level_one_code then b.level_three_name end as level_three_name, CurrentAddr 
from cdr_V_MedicalRecordMain a 
left join syz_regional_dic_TEMP b 
on a.CurrentCountyCode = b.rgn_code 
and a.CurrentCountyCode is not null 
left join syz_regional_dic_TEMP c 
on a.CurrentCityCode = c.rgn_code 
and a.CurrentCityCode is not null 
left join syz_regional_dic_TEMP d 
on substr(a.CurrentCityCode, 1, 4) = d.rgn_code 
and a.CurrentCityCode is not null 
left join syz_regional_dic_TEMP e 
on substr(CurrentProvinceCode, 1, 2) = e.rgn_code 
left join syz_regional_dic_TEMP f 
on a.HukouCountyCode = f.rgn_code 
and a.HukouCountyCode is not null 
left join syz_regional_dic_TEMP g 
on a.HukouCityCode = g.rgn_code 
and a.HukouCityCode is not null 
left join syz_regional_dic_TEMP h 
on substr(a.HukouCityCode, 1, 4) = h.rgn_code 
and a.HukouCityCode is not null 
left join syz_regional_dic_TEMP i 
on substr(HukouProvinceCode, 1, 2) = i.rgn_code
'''

# 关联病案首页
sql_1_50 = '''
DROP TABLE IF EXISTS skzbk.fs_INPATIENTNUMBER_FIRST
'''

sql_1_51 = '''
CREATE TABLE skzbk.fs_INPATIENTNUMBER_FIRST AS 
SELECT DISTINCT A.EMPI, A.patientno, A.inpatientnumber, A.InHospitalTime, A.OutHospitalTime, A.InHospitalDeptCode, A.InHospitalDeptname, A.OutHospitalDeptName, A.inhospitalwardname, A.diagnosecode, A.diagnosename, A.OperateDate, A.RN AS OperateIdx, A.OperateCode, A.OperateName, C.XM AS NAME, replace(C.NL,'岁','') AS AGE,  C.XB AS SEX, C.Birth AS BIRTHDAY, NVL(NVL(C.SFZHM,B.IDNo),'') AS IDCARD, NVL(C.LXRXM,'') AS CONTACTNAME, NVL(C.LXRGX,'') AS CONTACTRELATION, NVL(C.LXRDH,'') AS CONTACTTEL, C.MZ AS NATION, C.wj_jobcode AS JOB, C.HYZK AS MARRIAGE, C.XX, C.RH, NVL(D.HukouAddr,'') AS hJzzxxdz, NVL(D.level_one_code_hk,'') AS hJzzsdm, NVL(D.level_one_name_hk,'') AS hJzzs, NVL(D.level_two_code_hk,'') AS hJzzshidm, NVL(D.level_two_name_hk,'') AS hJzzshi, NVL(D.level_three_code_hk,'') AS hJzzxdm, NVL(D.level_three_name_hk,'') AS hJzzx, NVL(D.CurrentAddr,'') AS jtzzxxdz, NVL(D.level_one_code,'') AS jtzzsdm, NVL(D.level_one_name,'') AS jtzzs, NVL(D.level_two_code,'') AS jtzzshidm, NVL(D.level_two_name,'') AS jtzzshi, NVL(D.level_three_code,'') AS jtzzxdm, NVL(D.level_three_name,'') AS jtzzx 
FROM (SELECT * FROM skzbk.fs_INPATIENTNUMBER_LS_TEMP WHERE RN=1) A 
LEFT JOIN cdr_v_PatientBasicInformation B 
ON A.EMPI=B.EMPI 
left JOIN skzbk.fs_MEDICALRECORDMAIN_TEMP C 
ON A.encounterid=C.encounterid 
left JOIN skzbk.fs_REGIONAL_LS_temp D 
ON C.ID=D.ID
'''
# 关联病案首页
sql_1_60 = '''
DROP TABLE IF EXISTS skzbk.fs_INPATIENTNUMBER_LS
'''


# 添加入组时间和病区约束
sql_1_61 = '''
CREATE TABLE skzbk.fs_INPATIENTNUMBER_LS AS 
SELECT CONCAT(YEAR(B.inhospitaltime),'-',Lpad(B.YEAR_RN,4,'0')) AS patient_num, B.* 
FROM (SELECT A.*, ROW_NUMBER() OVER(PARTITION BY YEAR(A.inhospitaltime) ORDER BY A.InHospitalTime, A.inpatientnumber) AS YEAR_RN FROM skzbk.fs_INPATIENTNUMBER_FIRST A) B
where to_date(B.inhospitaltime) > to_date('%s')
'''% in_hospitaldate_first

sql_lis = [sql_1_00,
           sql_1_01,
           sql_1_02,
           sql_1_03,
           sql_1_10,
           sql_1_11,
           sql_1_20,
           sql_1_21,
           sql_1_30,
           sql_1_31,
           sql_1_40,
           sql_1_41,
           sql_1_50,
           sql_1_51,
           sql_1_60,
           sql_1_61]


## 2 - 患者入组；qs_drz_patient不脱敏
# 不变

sql_2= '''
SELECT A.patient_num as patient_num, A.EMPI as empi, A.inpatientnumber as inpatient_number, A.patientno as patient_no, A.name as name, A.idcard as id_card, CASE WHEN A.SEX='1' THEN '男' WHEN A.SEX='2' THEN '女' ELSE '未知' END as sex, A.age as age, 1 as hospital_id, '42502657200' as hospital_code, 1 as group_id, A.inhospitaltime as in_hospital_datetime, A.outhospitaltime as out_hospital_datetime, A.InHospitalDeptCode as in_hospital_dept_code, A.InHospitalDeptName as in_hospital_dept_name, A.OutHospitalDeptName as out_hospital_dept_name, A.inhospitalwardname as ward, A.diagnosecode as primary_diagnosis_code, A.diagnosename as primary_diagnosis, A.OperateDate as operate_date, A.OperateCode as operate_code, A.OperateName as operate_name, '0' AS delete_flag, '0' AS source_flag, A.operateidx as operate_idx, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd') AS create_date 
FROM skzbk.fs_INPATIENTNUMBER_LS A
'''

sql_2_ist = '''
insert into qs_drz_patient_temp(
patient_num,
empi, 
inpatient_number, 
patient_no, 
name, 
id_card, 
sex, 
age,
hospital_id,
hospital_code,
group_id, 
in_hospital_datetime, 
out_hospital_datetime, 
in_hospital_dept_code, 
in_hospital_dept_name, 
out_hospital_dept_name, 
ward, 
primary_diagnosis_code, 
primary_diagnosis, 
operate_date, 
operate_code, 
operate_name, 
delete_flag,
source_flag, 
operate_idx, 
create_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 3 - 基本信息；form_basic_info不脱敏

# 增加inpatient_number约束,限定和入组住院号一致
sql_3 = '''
SELECT * FROM 
(SELECT g.*, row_number() over (partition by g.empi order by g.in_hospital_time desc) num FROM
(select distinct a.PatientNo as patient_no, NVL(i.EMPI, i.patientno) AS EMPI, a.EncounterID as encounter_id, a.PatientName as patient_name, a.Sex as sex, a.countryname as countryname, a.nationname as nationname, a.birth as birth, a.InHospitalTime as in_hospital_time, a.OutHospitalTime as out_hospital_time, a.IDNumber as id_number, a.marriage as marriage, a.jobname as jobname, a.jobcode as jobcode, a.birthprovincename as birth_sheng, a.birthprovincecode as birth_sheng_code, a.birthcityname as birth_shi, a.birthcitycode as birth_shi_code, a.birthcountyname as birth_qu, a.birthcountycode as birth_qu_code, a.NativeProvinceName as native_sheng, a.NativeProvinceCode as native_sheng_code, a.NativeCityName as native_shi, a.NativeCityCode as native_shi_code, a.CurrentProvinceCode as current_province_code, a.CurrentProvinceName as current_province_name, a.CurrentCityCode as current_city_code, a.CurrentCityName as current_city_name, a.CurrentCountyCode as current_county_code, a.CurrentCountyName as current_county_name, a.CurrentAddr as current_addr, a.contacttel as contact_tel, a.CurrentTel as by_tel, a.abo as blood_abo, a.rh as blood_rh, a.payway as payway, '42502657200' as hospital_code, a.InpatientNumber as inpatient_number, a.OutpatientNumber as outpatient_number, b.contactphone as contactphone, 0 as delete_flag, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
from (SELECT * FROM cdr_v_MedicalRecordMain where id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))) a 
left join cdr_V_PatientBasicInformation b
on a.PatientNo=b.PatientNo 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) i 
ON a.PatientNo=i.PatientNo 
join skzbk.fs_INPATIENTNUMBER_LS d
on a.inpatientnumber = d.inpatientnumber
where a.PatientNo in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)) g) h 
WHERE h.num = 1
'''


sql_3_ist = '''
insert into form_basic_info_temp(
patient_no,
empi, 
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
jobcode,
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
num) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''


# 4_2 - 住院转归情况
# 增加住院号与第一住院一致约束
sql_4_2 = '''
select 
distinct 
NVL(c.EMPI, c.patientno) AS EMPI, 
a.PatientNo as patient_no, 
a.encounterid as encounter_id, 
a.PatientName as patient_name, 
a.inhospitaltime as inhospital_time, 
a.outhospitaltime as outhospital_time, 
a.inpatientnumber as inpatient_number, 
a.outpatientnumber as outpatient_number, 
null as inhospital_condition, 
b.outhospitalresult as outhospital_result, 
'42502657200' as hospital_code, 
0 as delete_flag, 
FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
from cdr_v_MedicalRecordMain a 
JOIN (SELECT * FROM cdr_v_MEDICALRECORDDIAGNOSE where isprimary = 1 and diagnosetype = 2) b ON a.id = b.medicalrecordid
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) c 
ON a.PatientNo = c.PatientNo 
join skzbk.fs_INPATIENTNUMBER_LS d
on a.inpatientnumber = d.inpatientnumber
WHERE a.PatientNo in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)
'''

sql_4_2_ist = '''
insert into form_qs_zg_temp(
empi, 
patient_no,
encounter_id,
patient_name,
inhospital_time,
outhospital_time,
inpatient_number, 
outpatient_number,
inhospital_condition, 
outhospital_result,
hospital_code,
delete_flag,
create_date ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 5 - form_diagnose_info

sql_51 = '''
SELECT
	f.*,
   CASE WHEN f.die_time IS NOT NULL THEN 1 ELSE 0 END AS is_die,
	dense_rank ( ) OVER ( PARTITION BY f.empi ORDER BY f.in_hospital_time ) AS inpatient_times 
FROM
	(
SELECT
	NVL ( c.EMPI, a.patientno ) AS empi,
	a.PatientNo AS patient_no,
	a.encounterid AS encounter_id,
	a.PatientName AS patient_name,
	REPLACE ( a.age, '岁', '' ) AS age,
	a.inpatientnumber AS inpatient_number,
	a.outpatientnumber AS outpatient_number,
	SUBSTR( a.inhospitaltime, 0, 10 ) AS in_hospital_time,
	SUBSTR( a.outhospitaltime, 0, 10 ) AS out_hospital_time,
	a.payway AS pay_way,
	a.dietime AS die_time,
	a.inhospitalwardcode AS inhospital_ward_code,
	a.inhospitalwardname AS inhospital_ward_name,
	a.inhospitalbedcode AS inhospital_bed_code,
	a.inhospitaldeptcode AS inhospital_dept_code,
	a.inhospitaldeptname AS inhospital_dept_name,
	a.inhospitalway AS inhospital_way,
	a.outhospitaldeptcode AS outhospital_dept_code,
	a.outhospitaldeptname AS outhospital_dept_name,
	a.inhospitaltotalcost AS inhospital_total_cost,
	b.isprimary AS isprimary,
	b.diagnosecode AS diagnose_code,
	b.diagnosename AS diagnose_name,
	b.diagnosetype as diagnose_type,
	b.diagnosetypename as diagnosetypename,
	b.sourceid as sourceid,
	b.sourceapp as sourceapp,
	'42502657200' AS hospital_code,
	0 AS delete_flag,
	FROM_UNIXTIME( UNIX_TIMESTAMP( ), 'yyyy-MM-dd HH:mm:ss' ) AS create_date
FROM
	( SELECT * FROM cdr_v_MedicalRecordMain WHERE id IN ( SELECT DISTINCT id FROM skzbk.fs_medicalrecordmain_ls_temp2 ) ) a
	left JOIN ( SELECT * FROM cdr_v_PATIENTDIAGNOSIS) b ON a.patientno = b.patientno and a.encounterid = b.encounterid 
	JOIN ( SELECT DISTINCT empi, patientno FROM dw.empi_cdw WHERE effect_flag = 1 ) c ON a.PatientNo = c.PatientNo
GROUP BY
	c.EMPI,
	a.patientno,
	a.encounterid,
	a.PatientName,
	a.age,
	a.inpatientnumber,
	a.outpatientnumber,
	a.inhospitaltime,
	a.outhospitaltime,
	a.payway,
	a.dietime,
	a.inhospitalwardcode,
	a.inhospitalwardname,
	a.inhospitalbedcode,
	a.inhospitaldeptcode,
	a.inhospitaldeptname,
	a.inhospitalway,
	a.outhospitaldeptcode,
	a.outhospitaldeptname,
	a.inhospitaltotalcost,
	b.isprimary,
	b.diagnosecode,
	b.diagnosename,
	b.diagnosetype,
	b.diagnosetypename,
	b.sourceid,
	b.sourceapp
	) f
'''

sql_51_ist = '''
insert into form_diagnose_info_51_temp(
empi, 
patient_no,
encounter_id,
patient_name,
age,
inpatient_number,
outpatient_number,
in_hospital_time,
out_hospital_time, 
pay_way,
die_time,
inhospital_ward_code, 
inhospital_ward_name, 
inhospital_bed_code, 
inhospital_dept_code,
inhospital_dept_name,
inhospital_way,
outhospital_dept_code,
outhospital_dept_name,
inhospital_total_cost,
isprimary,
diagnose_code,
diagnose_name,
diagnose_type,
diagnosetypename,
sourceid,
sourceapp,
hospital_code,
delete_flag,
create_date,
is_die,
inpatient_times) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 6 - form_diagnose_detail: 查sle确诊时间
sql_6 = '''
select distinct NVL(c.EMPI, c.patientno) AS EMPI, a.PatientNo as patient_no, a.encounterid as encounter_id, a.PatientName as patient_name, a.inhospitaltime as inhospital_time, a.outhospitaltime as outhospital_time, a.inpatientnumber as inpatient_number, a.outpatientnumber as outpatient_number, b.diagnosetime as diagnose_time, substr(b.diagnosetime, 0, 10) as diagnose_time_var, b.isprimary as isprimary, b.diagnosecode as diagnose_code, b.diagnosename as diagnose_name, '42502657200' as hospital_code, 0 as delete_flag, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
from cdr_v_MedicalRecordMain a 
JOIN (SELECT * FROM cdr_v_PATIENTDIAGNOSIS WHERE diagnosetype = 2) b
ON a.patientno = b.patientno and a.encounterid = b.encounterid 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) c 
ON a.PatientNo = c.PatientNo 
WHERE a.PatientNo in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS) AND (TRIM(b.DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) AND b.diagnosetype = 2
'''

sql_6_ist = '''
insert into form_diagnose_detail_temp(
empi, 
patient_no,
encounter_id,
patient_name,
inhospital_time,
outhospital_time,
inpatient_number, 
outpatient_number,
diagnose_time, 
diagnose_time_var,
isprimary,
diagnose_code,
diagnose_name,
hospital_code,
delete_flag,
create_date ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 7 - form_operation_info
sql_7 = '''
SELECT distinct NVL(d.EMPI, d.PatientNo) AS EMPI, a.PatientNo as patient_no, a.encounterid as encounter_id, a.inpatientnumber as inpatient_number, a.inhospitaltime as in_hospital_datetime, a.outhospitaltime as out_hospital_datetime, b.operatedate as operate_date, b.operatecode as operate_code, b.operatename as operate_name, c.operationdeptnname as operation_dept_name, b.operatedoctorname as operate_doctor_name, b.anesthesiawaycode as anesthesia_way_code, b.anesthesiawayname as anesthesia_way_name, b.anesthesiadoctorname as anesthesia_doctor_name, c.preoperationdiagnosecode as preoperation_diagnose_code, c.preoperationdiagnosename as preoperation_diagnose_name, '42502657200' as hospital_code, 0 as delete_flag, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
FROM cdr_V_MedicalRecordMain a 
JOIN cdr_V_MEDICALRECORDOPERATE b 
ON a.id = b.medicalrecordid 
LEFT JOIN (SELECT * FROM cdr_V_OPERATIONRECORD WHERE bigdata_data_tag = 1) c 
ON a.patientno = c.patientno AND a.encounterid = c.Inpatientvisitid AND b.operatedate = c.operationtime 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)) d 
ON a.PatientNo = d.PatientNo 
WHERE a.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))
'''



sql_7_ist = '''
insert into form_operation_info_temp(
empi, 
patient_no,
encounter_id, 
inpatient_number,
in_hospital_datetime,
out_hospital_datetime,
operate_date,
operate_code,
operate_name,
operation_dept_name,
operate_doctor_name,
anesthesia_way_code,
anesthesia_way_name,
anesthesia_doctor_name,
preoperation_diagnose_code,
preoperation_diagnose_name,
hospital_code,
delete_flag,
create_date ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''
# to_date(a.inhospitaltime) > to_date('2020-11-30')

# 8 - form_medication_info
sql_8 = '''
SELECT NVL(d.EMPI, d.patientno) AS EMPI, c.PatientNo as patient_no, c.EncounterID as encounter_id, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, c.InHospitalTime as in_hospital_time, c.OutHospitalTime as out_hospital_time, a.MasterOrdersID as master_orders_id, a.OrdersCode as orders_code, case when a.OrdersName = '(甲)重组人胰岛素注射液(优泌林R)笔芯' then '(甲)重组人胰岛素注射液(优泌林R笔芯)' when a.OrdersName = '(乙10%)重组牛碱性成纤维细胞生长因子外用溶液(贝复济' then '(乙10%)重组牛碱性成纤维细胞生长因子外用溶液(贝复济)' when a.OrdersName LIKE '%（%' then replace(a.OrdersName, '（', '(') when a.OrdersName LIKE '%）%' then replace(a.OrdersName, '）', ')') else a.OrdersName end as orders_name, a.Specifications as specifications, a.Dosage as dosage, a.DosageUnit as dosage_unit, a.Pathway as pathway, a.Frequency as frequency, a.frequency as pc, a.WriteRecipeTime as write_recipe_time, a.ProjectTypeCode as project_type_code, a.ProjectTypeName as project_type_name, a.ordersstarttime as orders_start_time, a.stoptime as stop_time, a.solventflag as solventflag, a.remark as remark, '42502657200' as hospital_code, 0 as delete_flag, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
FROM cdr_V_MedicationOrders a -- 住院用药医嘱（MedicationOrders）
JOIN cdr_V_MedicalRecordMain c -- 病案首页（MedicalRecordMain）
ON a.inpatientvisitid = c.encounterid 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)) d
ON a.PatientNo = d.PatientNo 
LEFT JOIN skzbk.dict_frequency e 
ON a.Frequency=e.code 
WHERE c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and a.OrdersCode in ('100438','100439','100440','100441','100443','100444','100546','121153','124600','100070','121390','100598','100854','100855','100856','100857','100858','100865','100871','100875','100877','100878','112192','121229','121298','122968','122973','122998','124685','100548','100549','100550','100551','100552','100599','100601','100646','100867','100873','100874','101163','101310','102947','112249','121403','122991','124612','100001','100006','100007','100008','100009','100014','100016','100017','100030','100038','100039','100050','100051','100055','100056','100059','100063','100066','100073','100079','100086','100115','100116','100119','100122','100124','100301','100370','100885','100886','100887','112212','112258','121122','121130','121135','121246','121273','121305','121348','121365','121446','121450','121452','121454','121456','121457','121462','121466','122993','122994','123884','124624','124687','124692','124697','124802','124804','100520','100521','100515','100518','100638','100650','100677','102938','121242','124767','121468','122992','100203','100214','100218','121397','100171','100176','100177','100198','100200','100233','100242','100246','100247','100248','100249','100250','100252','100259','100264','100265','100267','100268','100270','102939','112245','121099','121119','121141','121156','121300','121301','121307','121309','121367','121453','121465','122995','123864','124691','124693','124701','124707','100567','100570','100572','100576','100950','100956','100957','102943','121187','121210','121213','121399','121451','121455','122979','122997','124698','124703','124706','100222','100225','100229','121255','121299','121352','121444','121469','122974','124801','100144','100157','100158','100159','100160','100161','100163','100206','100207','100883','100884','112272','121149','121150','121236','121294','121319','121320','121346','122976','100962','100964','100966','100978','121270','100308','100310','100311','100313','100315','100317','100318','100340','100342','112233','121176','121232','121252','121381','121458','122988','124681','124688','100635','100106','100133','100137','100143','100148','100153','100169','100191','100192','100201','100205','100208','100266','100271','100283','100285','100289','100291','100293','100294','100295','100302','100327','100334','100337','100346','100353','100359','100367','100368','100375','100376','100401','100402','100429','100456','100464','100467','100473','100488','100490','100497','100506','100525','100529','100534','100580','100583','100585','100587','100597','100684','100716','100723','100732','100733','100745','100747','100749','100750','100752','100761','100764','100766','100767','100768','100769','100770','100772','100774','100827','100828','100842','100851','100889','100890','100892','100899','100904','100924','100926','100933','100938','100953','100969','100970','100981','100985','100986','100987','100994','100997','101000','101007','101014','101027','101028','101057','101076','101089','101090','101091','101093','101102','101103','101104','101106','101162','101164','101166','101168','101170','101323','101328','102946','112143','112215','112216','112274','112281','112282','121091','121114','121124','121136','121157','121159','121166','121202','121207','121221','121230','121233','121245','121260','121264','121272','121303','121304','121312','121327','121353','121354','121377','121378','121388','121389','121394','121412','121421','121445','121459','121460','121470','122316','122317','122944','122966','122969','122972','122975','122977','122978','122980','122982','122983','122985','122987','124602','124643','124645','124657','124671','124680','124684','124686','124695','124702','124749','124759','124761','124787','100882','121158','100738','100739','100810','100815','121310','100658','101033','101036','112236','121133','121383','122344','100180','100182','100186','100074','100075','100078','100091','100093','100381','100382','100394','100398','100400','100403','100404','100409','100411','100412','100421','100422','100424','100426','100428','100430','100431','100433','100434','100537','100864','101260','101277','101329','102934','102940','121103','121173','121361','121375','122984','123855','123888','124705','124724','100071','100164','100173','100185','100876','100975','101173','101176','101181','101186','101187','101190','101209','101210','101214','101227','101231','101244','101247','101279','101295','101296','101302','101317','101320','121123','121431','121432','121474','122943','122952')
'''


sql_8_ist = '''
insert into form_medication_info_temp(
empi, 
patient_no,
encounter_id,
inpatient_number,
outpatient_number,
in_hospital_time,
out_hospital_time,
master_orders_id,
orders_code,
orders_name,
specifications,
dosage,
dosage_unit,
pathway,
frequency,
pc,
write_recipe_time,
project_type_code,
project_type_name,
orders_start_time,
stop_time,
solventflag,
remark,
hospital_code,
delete_flag,
create_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 9 - form_physical_exam_info
sql_9 = '''
SELECT NVL(r.EMPI, r.PatientNo) AS EMPI, a.PatientNo as patient_no, CONCAT('***', SUBSTRING(a.IDNumber, 4, length(a.IDNumber)-7), '0000') as id_number, a.EncounterID as encounter_id, a.InpatientNumber as inpatient_number, a.OutpatientNumber as outpatient_number, c.operatedate as operate_date, substr(c.operatedate, 0, 10) as operate_date_var, c.Value as height, e.Value as weight, g.Value as temperature, CASE WHEN i.Value IS NOT NULL THEN split(i.Value, '/')[0] ELSE NULL END as systolic, CASE WHEN i.Value IS NOT NULL THEN split(i.Value, '/')[1] ELSE NULL END as diastolic, m.Value as respiratory_rate, o.Value as heart_rate, q.Value as oxygen_saturation, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
FROM cdr_V_MedicalRecordMain a 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate asc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='3024') b WHERE b.rank = 1) c -- 身高
ON a.PatientNo = c.PatientNo and a.encounterid = c.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate asc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='1014') d WHERE d.rank = 1) e -- 体重 
ON a.PatientNo = e.PatientNo and a.encounterid = e.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate asc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='1001') f WHERE f.rank = 1) g -- 体温 
ON a.PatientNo = g.PatientNo and a.encounterid = g.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate asc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='128') h WHERE h.rank = 1) i -- 收缩压 
ON a.PatientNo = i.PatientNo and a.encounterid = i.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate asc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='1004') l WHERE l.rank = 1) m -- 呼吸频率 
ON a.PatientNo = m.PatientNo and a.encounterid = m.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate asc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='1002') n WHERE n.rank = 1) o -- 心率 
ON a.PatientNo = o.PatientNo and a.encounterid = o.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate asc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='129') p WHERE p.rank = 1) q -- 氧饱和度 
ON a.PatientNo = q.PatientNo and a.encounterid = q.encounterid 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)) r 
ON a.PatientNo = r.PatientNo 
where a.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))
'''

sql_9_ist = '''
insert into form_physical_exam_info_temp(
empi,
patient_no,
id_number,
encounter_id,
inpatient_number,
outpatient_number,
operate_date,
operate_date_var,
height,
weight,
temperature,
systolic,
diastolic,
respiratory_rate,
heart_rate,
oxygen_saturation,
hospital_code,
create_date) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''


sql_10 = '''
SELECT 
distinct NVL(d.EMPI, d.PatientNo) AS EMPI, 
a.PatientNo as patient_no,
CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, 
a.EncounterID as encounter_id, 
c.InpatientNumber as inpatient_number, 
c.OutpatientNumber as outpatient_number, 
a.EncounterType as encounter_type, 
CASE WHEN a.reportclasscode='Electrocardio' and a.reportname like '%心电图%' THEN 20 WHEN a.reportname = '彩超检查报告' THEN 21 WHEN a.reportname like '%心脏%彩超%' THEN 21 WHEN a.reportclasscode in ('Ultrasound', 'US') THEN 22 WHEN reportname='CT报告' and bodysite='胸部' THEN 23 WHEN reportname='CT报告' and bodysite like '%腹部%' THEN 24 ELSE NULL END as question_id, 
b.ReportID as report_id, 
a.TSExam as ts_exam, 
substr(a.TSExam, 0, 10) as ts_exam_var, 
b.examName as exam_name,
a.ReportName as report_name, 
b.ExamFind as exam_find, 
b.ExamConclusion as exam_conclusion, 
b.BodySite as body_site, 
FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date, 
a.reportclasscode as report_class_code, 
a.reportclassname as report_class_name,
b.summarynote as summary_note,
a.binarycontent as binary_content 
FROM cdr_V_OTHERREPORT a -- B超报告（UltrasoundReport）
JOIN cdr_V_OTHERRESULT b -- B超报告项目结果（UltrasoundResult）
ON a.id = b.ReportID 
JOIN cdr_V_MedicalRecordMain c -- 病案首页（MedicalRecordMain）
ON a.PatientNo = c.PatientNo and a.encounterid = c.encounterid 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)) d 
ON a.PatientNo = d.PatientNo 
join (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) h
on c.id = h.medicalrecordid
where (a.reportclasscode='Electrocardio' and a.reportname like '%心电图%') or (a.reportname = '彩超检查报告' and a.reportclasscode='XC') or a.reportname like '%心脏%彩超%' or  (a.reportclasscode in ('Ultrasound', 'US') and (b.ExamFind like '%肝%' or b.ExamFind like '%胆%' or b.ExamFind like '%胰%' or b.ExamFind like '%脾%' or b.ExamFind like '%肾%' or b.ExamFind like '%甲状腺%')) or (a.reportname='CT报告' and (b.bodysite='胸部' or b.bodysite like '%腹部%'))
'''

sql_10_ist = '''
insert into form_ris_info_temp(
empi, 
patient_no,
id_number, 
encounter_id,
inpatient_number,
outpatient_number,
encounter_type,
question_id,
report_id,
ts_exam,
ts_exam_var, 
exam_name,
report_name,
exam_find,
exam_conclusion,
body_site,
create_date,
report_class_code,
report_class_name,
summary_note,
binary_content) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 11 - form_lab_info

# 抽取所有检查，进行分析
sql_110 = '''
SELECT a.test_order as Examclasscode, a.test_order_name as Examclassname, c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 27 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, a.Reportname as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))
and to_date(c.inhospitaltime) > to_date('%s')
'''% in_hospitaldate_first
#and to_date(c.inhospitaltime) < to_date('2020-05-03') and to_date(c.inhospitaltime) > to_date('2018-05-02')

sql_110_ist = '''
insert into form_lab_info_temp_all(
Examclasscode,
Examclassname,
in_hospital_date,
empi,
patient_no,
id_number,
encounter_id,
encounter_type,
inpatient_number,
outpatient_number,
question_id,
lab_generic_id,
ts_test,
ts_test_var,
SpecimenClassName,
table_item_name,
test_item_code,
test_item_name,
print_value,
result_value,
result_unit,
reference_text,
abnormal_flag,
abnormal_flag_name,
hospital_code,
create_date,
ts_draw,
ts_draw_var) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''


# 15 - 门诊诊断 form_focus_diagnosis_followup

sql_15 = '''
select 
distinct
b.empi as empi,
b.PatientNo as patient_no,
a.id as encounter_id,
a.patientname as patient_name,
a.patid as outpatient_number,
a.registrationdatetime as registrationdatetime,
a.visitdatetime as visitdatetime,
c.encountertype as category_name,
c.diagnosename as primary_diagnosis,
c.diagnosecode as primary_diagnosis_code,
a.visitdeptcode as visit_deptcode,
a.visitdeptname as visit_deptname
FROM cdr_v_OUTPATIENTVISITRECORD a 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) b 
ON a.PatientNo=b.PatientNo
JOIN (select * from cdr_v_PATIENTDIAGNOSIS where  diagnosetype = 0 and isprimary = 1) c
ON a.PatientNo=c.PatientNo and a.id = c.encounterid
WHERE a.PatientNo 
in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)
'''


sql_15_ist = '''
insert into form_focus_diagnosis_followup_temp(
empi,
patient_no, 
encounter_id,
patient_name,
outpatient_number,
registrationdatetime,
visitdatetime,
category_name, 
primary_diagnosis, 
primary_diagnosis_code,
visit_deptcode,
visit_deptname
) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''


# 17 - form_medication_info_followup
sql_17 = '''
SELECT distinct NVL(d.EMPI, a.PatientNo) AS EMPI, 
a.PatientNo as patient_no, 
a.patid as outpatient_number, 
a.id as encounter_id,
to_date(b.writerecipetime) AS writerecipetime_date, 
to_date(b.writerecipedatetime) AS writerecipedatetime_date, 
a.primarydiagnosis as primary_diagnosis,
a.primarydiagnosiscode as primary_diagnosis_code,
c.outpatientrecipeid as outpatientrecipeid,
c.projecttypename as projecttypename,
c.projecttypecode as projecttypecode,
c.projectid as projectid,
c.projectcode as projectcode,
c.projectname as projectname,
c.specifications as specifications,
c.projectnumber as projectnumber,
c.dosage as dosage,
c.dosageunit as dosageunit,
c.frequency as frequency,
c.pathway as pathway,
c.days as days,
c.orders as orders,
c.recipeno as recipeno,
'42502657200' as hospital_code, 
FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
FROM cdr_v_OUTPATIENTVISITRECORD a 
JOIN cdr_V_OUTPATIENTRECIPE b ON a.id = b.outpatientvisitid and a.PatientNo = b.PatientNo
JOIN cdr_V_OUTPATIENTRECIPEDETAIL c ON b.id = c.outpatientrecipeid
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) d 
ON a.PatientNo=d.PatientNo 
WHERE a.PatientNo 
in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)
'''

sql_17_ist = '''
insert into form_medication_info_followup_temp(
empi, 
patient_no,
outpatient_number,
encounter_id,
writerecipetime_date, 
writerecipedatetime_date, 
primary_diagnosis,
primary_diagnosis_code,
outpatientrecipeid,
projecttypename,
projecttypecode,
projectid,
projectcode,
projectname,
specifications,
projectnumber,
dosage,
dosageunit,
frequency,
pathway,
days,
orders,
recipeno,
hospital_code, 
create_date ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 18 随访实验室检验

# 抽取所有检查，进行分析
sql_180 = '''
SELECT 
a.test_order as Examclasscode, 
a.test_order_name as Examclassname, 
c.registrationdatetime as visittime, 
NVL(d.EMPI, d.PatientNo) AS EMPI, 
c.PatientNo as patient_no, 
null as id_number, 
c.ID as encounter_id, 
a.EncounterType as encounter_type, 
c.patid as patid, 
null as inpatient_number, 
43 as question_id, 
b.LabGenericID as lab_generic_id, 
a.TSTest as ts_test, 
substr(a.TSTest, 0, 10) as ts_test_var, 
a.SpecimenClassName, 
a.Reportname,
b.TestItemCode as test_item_code, 
b.TestItemName as test_item_name, 
b.PrintValue as print_value,
 b.ResultValue as result_value, 
 b.ResultUnit as result_unit, 
 b.ReferenceText as reference_text, 
 b.AbnormalFlag as abnormal_flag, 
 b.AbnormalFlagName as abnormal_flag_name, 
 '42502657200' as hospital_code, 
 FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date ,
 a.tsdraw as ts_draw, 
 substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_OUTPATIENTVISITRECORD c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT encounterid FROM cdr_v_PATIENTDIAGNOSIS WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))
and to_date(c.registrationdatetime) > to_date('%s')
'''% in_hospitaldate_first


sql_180_ist = '''
insert into form_lab_info_temp_all(
Examclasscode,
Examclassname,
in_hospital_date,
empi,
patient_no,
id_number,
encounter_id,
encounter_type,
outpatient_number,
inpatient_number,
question_id,
lab_generic_id,
ts_test,
ts_test_var,
SpecimenClassName,
table_item_name,
test_item_code,
test_item_name,
print_value,
result_value,
result_unit,
reference_text,
abnormal_flag,
abnormal_flag_name,
hospital_code,
create_date,
ts_draw,
ts_draw_var) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# -- # 19 随访检查

#拓展超声心动图
sql_19 = '''
SELECT 
distinct NVL(d.EMPI, d.PatientNo) AS EMPI, 
a.PatientNo as patient_no,
null as id_number, 
a.EncounterID as encounter_id, 
c.patid as patid, 
c.visitdate as visitdate, 
a.EncounterType as encounter_type, 
CASE WHEN a.reportclasscode='Electrocardio' and a.reportname like '%心电图%' THEN 20 WHEN a.reportname = '彩超检查报告' THEN 21 WHEN a.reportname like '%心脏%彩超%' THEN 21 WHEN a.reportclasscode in ('Ultrasound', 'US') THEN 22 WHEN reportname='CT报告' and bodysite='胸部' THEN 23 WHEN reportname='CT报告' and bodysite like '%腹部%' THEN 24 ELSE NULL END as question_id, 
b.ReportID as report_id, 
a.TSExam as ts_exam, 
substr(a.TSExam, 0, 10) as ts_exam_var, 
b.examName as exam_name,
a.ReportName as report_name, 
b.ExamFind as exam_find, 
b.ExamConclusion as exam_conclusion, 
b.BodySite as body_site, 
FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date, 
a.reportclasscode as report_class_code, 
a.reportclassname as report_class_name,
b.summarynote as summary_note 
FROM cdr_V_OTHERREPORT a -- B超报告（UltrasoundReport）
JOIN cdr_V_OTHERRESULT b -- B超报告项目结果（UltrasoundResult）
ON a.id = b.ReportID 
JOIN cdr_V_OUTPATIENTVISITRECORD c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_INPATIENTNUMBER_LS)) d 
ON a.PatientNo = d.PatientNo 
-- where (a.reportname = '彩超检查报告' and a.reportclasscode='XC') or a.reportname like '%心脏%彩超%' or (a.reportclasscode='Electrocardio' and a.reportname like '%心电图%') or (a.reportname = '彩超检查报告' and a.reportclasscode='XC') or a.reportname like '%心脏%彩超%' or  (a.reportclasscode in ('Ultrasound', 'US') and (b.ExamFind like '%肝%' or b.ExamFind like '%胆%' or b.ExamFind like '%胰%' or b.ExamFind like '%脾%' or b.ExamFind like '%肾%' or b.ExamFind like '%甲状腺%')) or (a.reportname='CT报告' and (b.bodysite='胸部' or b.bodysite like '%腹部%'))
'''


sql_19_ist = '''
insert into form_ris_info_followup_temp(
empi,
patient_no,
id_number, 
encounter_id,
patid,
visitdate,
encounter_type,
question_id,
report_id,
ts_exam,
ts_exam_var, 
exam_name,
report_name,
exam_find,
exam_conclusion,
body_site,
create_date,
report_class_code,
report_class_name,
summary_note) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''


# -- # 20 表4 主诉及现病史 form_complaint_inhos

sql_20 = '''
select 
distinct
c.empi as empi
,c.patientno as patient_no
,a.BRXM as patient_name
,a.HDSD0002025 as id_number
,a.HDSD0013116 as inpatient_number
,a.HDSD0013003 as ward
,a.HDSD0013045 as dept_name
,a.HDSD0013057 as inhospital_time
,a.HDSD0013114 as complaint
,a.HDSD0013095 as present_ill_history
from cdr_tb_ryjl a
join cdr_V_INPATIENTVISITRECORD b
on a.HDSD0013116 = b.admissionnumber
join skzbk.fs_INPATIENTNUMBER_LS c
on b.patientno = c.patientno
where a.bigdata_data_tag  = 1
'''

sql_20_ist = '''
insert into form_complaint_inhos_temp(
empi,
patient_no,
patient_name, 
id_number,
inpatient_number,
ward, 
dept_name, 
inhospital_time, 
complaint,
present_ill_history
) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# -- # 21 表41 随访主诉及现病史 form_complaint_outcome

sql_21 = '''
select 
distinct
c.empi as empi
,c.patientno as patient_no
,a.BRXM as patient_name
,a.HDSD0002025 as id_number
,a.HDSD0003025 as outpatient_number
,a.SourceName as ward
,a.HDSD0003024 as dept_name
,a.HDSD0003023 as visit_time
,a.HDSD0103010 as is_first_visit
,a.HDSD0003057 as complaint
,a.HDSD0003038 as present_ill_history
from cdr_tb_mjzbl a
join cdr_V_OUTPATIENTVISITRECORD b
on a.HDSD0003025 = b.patid
join skzbk.fs_INPATIENTNUMBER_LS c
on b.patientno = c.patientno
where a.bigdata_data_tag  = 1
'''

sql_21_ist = '''
insert into form_complaint_outcome_temp(
empi,
patient_no,
patient_name, 
id_number,
outpatient_number,
ward, 
dept_name, 
visit_time, 
is_first_visit, 
complaint,
present_ill_history
) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 手术治疗
sql_22 = '''
select
h.*
,k.reportname
,substr(k.tsexam,0,10) as bl_date
,m.examconclusion
from
(select
distinct
a.empi as empi
,a.patientno as patientno
,a.inhospitaltime as inhospitaltime
,b.admissionnumber as inpatientnumber
,b.id as encounterid
,b.inhospitaldatetime as inhospitaldatetime
,d.HDSD0106074 as operatename
,d.HDSD0006074 as operatecode
,c.HDSD0006043 as deptname -- 科室
,c.HDSD0006085 as doctorname
,d.HDSD0006078 as operate_start_time-- 手术开始时间
,d.HDSD0006077 as operate_end_time
,to_date(concat_ws('-',substr(c.HDSD0006068,0,4),substr(c.HDSD0006068,5,2),substr(c.HDSD0006068,7,2))) as operate_time
,c.HDSD0106044 as mzff-- 麻醉方法
,c.HDSD0006055 as mzys--麻醉医生
,c.HDSD0006073 as ssgc
,c.HDSD0006104 as sqzd
,c.HDSD0106104 as qszdbm
,c.HDSD0006100 as shzd
,c.HDSD0106100 as shzdbm
from 
skzbk.fs_INPATIENTNUMBER_LS a
join cdr_V_INPATIENTVISITRECORD b
on a.patientno = b.patientno
join cdr_tb_ybssjl c
on b.admissionnumber = c.HDSD0006144
left join cdr_tb_ybssjl_ss d
on c.id = d.refid) h
left join (select * from cdr_v_OTHERREPORT where reportclasscode = 'BL') k
on k.patientno = h.patientno and k.encounterid = h.encounterid and substr(k.tsexam,0,10) = h.operate_time
left join cdr_v_OTHERRESULT m
on k.id = m.reportid
where to_date(h.operate_time) > to_date(h.inhospitaltime)
'''

sql_22_ist = '''
insert into form_operate_treatment_temp(
empi,
patient_no,
inhospitaltime_rz,
inpatient_number,
encounter_id,
in_hospitaltime_datetime,
operate_name,
operate_code,
dept_name,
operate_doctor_name,
operate_datetime_s,
operate_datetime_e,
operate_datetime,
anesthesia_method,
anesthesia_doctor_name,
operate_proc_desc,
diagbose_name_before,
diagbose_name_code_before,
diagbose_name_after,
diagbose_name_code_after,
bl_reportname,
bl_date,
operate_pathology
) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''
