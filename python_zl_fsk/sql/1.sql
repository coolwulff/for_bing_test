## 2 - qs_drz_patient不脱敏

sql_2= '''
SELECT A.patient_num as patient_num, A.EMPI as empi, A.inpatientnumber as inpatient_number, A.patientno as patient_no, A.name as name, A.idcard as id_card, CASE WHEN A.SEX='1' THEN '男' WHEN A.SEX='2' THEN '女' ELSE '未知' END as sex, A.age as age, 1 as hospital_id, '42502657200' as hospital_code, 1 as group_id, A.inhospitaltime as in_hospital_datetime, A.outhospitaltime as out_hospital_datetime, A.InHospitalDeptCode as in_hospital_dept_code, A.InHospitalDeptName as in_hospital_dept_name, A.OutHospitalDeptName as out_hospital_dept_name, A.OutHospitalWardName as ward, A.diagnosecode as primary_diagnosis_code, A.diagnosename as primary_diagnosis, A.OperateDate as operate_date, A.OperateCode as operate_code, A.OperateName as operate_name, '0' AS delete_flag, '0' AS source_flag, A.operateidx as operate_idx, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd') AS create_date 
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

# 3 - form_basic_info不脱敏
sql_3_old = '''
SELECT * FROM 
(SELECT g.*, row_number() over (partition by g.empi order by g.in_hospital_time desc) num FROM
(select distinct a.PatientNo as patient_no, NVL(i.EMPI, i.patientno) AS EMPI, a.EncounterID as encounter_id, a.PatientName as patient_name, a.Sex as sex, a.countryname as countryname, a.nationname as nationname, a.birth as birth, a.InHospitalTime as in_hospital_time, a.OutHospitalTime as out_hospital_time, a.IDNumber as id_number, a.marriage as marriage, a.jobname as jobname, a.birthprovincename as birth_sheng, a.birthprovincecode as birth_sheng_code, a.birthcityname as birth_shi, a.birthcitycode as birth_shi_code, a.birthcountyname as birth_qu, a.birthcountycode as birth_qu_code, a.NativeProvinceName as native_sheng, a.NativeProvinceCode as native_sheng_code, a.NativeCityName as native_shi, a.NativeCityCode as native_shi_code, a.CurrentProvinceCode as current_province_code, a.CurrentProvinceName as current_province_name, a.CurrentCityCode as current_city_code, a.CurrentCityName as current_city_name, a.CurrentCountyCode as current_county_code, a.CurrentCountyName as current_county_name, a.CurrentAddr as current_addr, a.contacttel as contact_tel, a.CurrentTel as by_tel, a.abo as blood_abo, a.rh as blood_rh, a.payway as payway, '42502657200' as hospital_code, a.InpatientNumber as inpatient_number, a.OutpatientNumber as outpatient_number, b.contactphone as contactphone, 0 as delete_flag, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
from (SELECT * FROM cdr_v_MedicalRecordMain where id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))) a 
left join cdr_V_PatientBasicInformation b
on a.PatientNo=b.PatientNo 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) i 
ON a.PatientNo=i.PatientNo 
where a.PatientNo in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) g) h 
WHERE h.num = 1
'''


sql_3_ist_old = '''
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
num) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 增加jobcode
sql_3 = '''
SELECT * FROM 
(SELECT g.*, row_number() over (partition by g.empi order by g.in_hospital_time desc) num FROM
(select distinct a.PatientNo as patient_no, NVL(i.EMPI, i.patientno) AS EMPI, a.EncounterID as encounter_id, a.PatientName as patient_name, a.Sex as sex, a.countryname as countryname, a.nationname as nationname, a.birth as birth, a.InHospitalTime as in_hospital_time, a.OutHospitalTime as out_hospital_time, a.IDNumber as id_number, a.marriage as marriage, a.jobname as jobname, a.jobcode as jobcode, a.birthprovincename as birth_sheng, a.birthprovincecode as birth_sheng_code, a.birthcityname as birth_shi, a.birthcitycode as birth_shi_code, a.birthcountyname as birth_qu, a.birthcountycode as birth_qu_code, a.NativeProvinceName as native_sheng, a.NativeProvinceCode as native_sheng_code, a.NativeCityName as native_shi, a.NativeCityCode as native_shi_code, a.CurrentProvinceCode as current_province_code, a.CurrentProvinceName as current_province_name, a.CurrentCityCode as current_city_code, a.CurrentCityName as current_city_name, a.CurrentCountyCode as current_county_code, a.CurrentCountyName as current_county_name, a.CurrentAddr as current_addr, a.contacttel as contact_tel, a.CurrentTel as by_tel, a.abo as blood_abo, a.rh as blood_rh, a.payway as payway, '42502657200' as hospital_code, a.InpatientNumber as inpatient_number, a.OutpatientNumber as outpatient_number, b.contactphone as contactphone, 0 as delete_flag, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
from (SELECT * FROM cdr_v_MedicalRecordMain where id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))) a 
left join cdr_V_PatientBasicInformation b
on a.PatientNo=b.PatientNo 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) i 
ON a.PatientNo=i.PatientNo 
where a.PatientNo in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) g) h 
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



# 4 - 住院记录qs_admission_history
sql_4 = '''
SELECT c.*, ROW_NUMBER() OVER(PARTITION BY c.empi ORDER BY c.in_hospital_date) AS admission_num FROM 
(SELECT distinct NVL(b.EMPI, a.PatientNo) AS EMPI, a.PatientNo as patient_no, a.inpatientnumber as inpatient_number, a.inhospitaltime as in_hospital_date, a.outhospitaltime as out_hospital_date, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
FROM cdr_V_MedicalRecordMain a 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) b 
ON a.PatientNo=b.PatientNo 
WHERE a.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))) c
'''

sql_4_wrong = '''
SELECT c.*, ROW_NUMBER() OVER(PARTITION BY c.empi ORDER BY c.in_hospital_date) AS admission_num FROM 
(SELECT distinct NVL(b.EMPI, a.PatientNo) AS EMPI, a.PatientNo as patient_no, a.inpatientnumber as inpatient_number, a.inhospitaltime as in_hospital_date, a.outhospitaltime as out_hospital_date, d.dischargediseasecode as cyqk_code, d.dischargediseasename as cyqk, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
FROM cdr_V_MedicalRecordMain a 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) b 
ON a.PatientNo=b.PatientNo 
left join cdr_V_INPATIENTVISITRECORD d
ON a.PatientNo=d.PatientNo and a.inpatientnumber = d.admissionnumber
WHERE a.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))) c
'''

sql_4_ist = '''
insert into qs_admission_history_temp(
empi, 
patient_no,
inpatient_number,
in_hospital_date,
out_hospital_date,
create_date,
admission_num) values (%s,%s,%s,%s,%s,%s,%s);
'''

# 4_2 - 住院转归情况
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
WHERE a.PatientNo in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)
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
# 旧版，可删
sql_5_old = '''
select distinct NVL(c.EMPI, c.patientno) AS EMPI, a.PatientNo as patient_no, a.encounterid as encounter_id, a.PatientName as patient_name, replace(a.age, '岁', '') as age, a.inpatientnumber as inpatient_number, a.outpatientnumber as outpatient_number, a.inhospitaltime as in_hospital_time, a.outhospitaltime as out_hospital_time, a.payway as pay_way, a.dietime as die_time, CASE WHEN a.dietime is not NULL THEN 1 ELSE 0 END as is_die, a.inhospitalwardcode as inhospital_ward_code, a.inhospitalwardname as inhospital_ward_name, a.inhospitalbedcode as inhospital_bed_code, a.inhospitaldeptcode as inhospital_dept_code, a.inhospitaldeptname as inhospital_dept_name, a.inhospitalway as inhospital_way, a.outhospitaldeptcode as outhospital_dept_code, a.outhospitaldeptname as outhospital_dept_name, a.inhospitaltotalcost as inhospital_total_cost, a.inpatienttimes as inpatient_times, b.isprimary as isprimary, b.diagnosecode as diagnose_code, b.diagnosename as diagnose_name, '42502657200' as hospital_code, 0 as delete_flag, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
from cdr_v_MedicalRecordMain a 
left join (SELECT * FROM cdr_v_PATIENTDIAGNOSIS WHERE diagnosetype = 2  AND TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) b 
ON a.patientno = b.patientno and a.encounterid = b.encounterid 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) c 
ON a.PatientNo = c.PatientNo 
WHERE a.PatientNo in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)
'''
# 参考，可删
sql_5_cankao = '''
SELECT
	f.*,
   CASE WHEN f.die_time IS NOT NULL THEN 1 ELSE 0 END AS is_die,
	ROW_NUMBER ( ) OVER ( PARTITION BY f.empi ORDER BY f.in_hospital_time ) AS inpatient_times 
FROM
	(
SELECT
	NVL ( c.EMPI, a.patientno ) AS empi,
	a.PatientNo AS patient_no,
	a.recordnumber AS record_number,
	'住院' AS encounter_type,
	a.encounterid AS encounter_id,
	a.PatientName AS patient_name,
	REPLACE ( a.age, '岁', '' ) AS age,
	a.inpatientnumber AS inpatient_number,
	a.outpatientnumber AS outpatient_number,
	SUBSTR( a.inhospitaltime, 0, 10 ) AS in_hospital_time,
	SUBSTR( a.outhospitaltime, 0, 10 ) AS out_hospital_time,
	a.payway AS pay_way,
	a.dietime AS die_time,
	a.inhospitaldeptcode AS inhospital_dept_code,
	a.inhospitaldeptname AS inhospital_dept_name,
	a.inhospitalway AS inhospital_way,
	a.outhospitalway AS outhospital_way,
	a.outhospitaldeptcode AS outhospital_dept_code,
	a.outhospitaldeptname AS outhospital_dept_name,
	a.attendingdoctorname AS attending_doctor_name,
	a.inhospitaltotalcost AS inhospital_total_cost,
	1 AS isprimary,
	concat_ws( '；', collect_set ( TRIM( b.diagnosecode ) ) ) AS diagnose_code,
	concat_ws( '；', collect_set ( TRIM( b.diagnosename ) ) ) AS diagnose_name,
	'42502657200' AS hospital_code,
	0 AS delete_flag,
	FROM_UNIXTIME( UNIX_TIMESTAMP( ), 'yyyy-MM-dd HH:mm:ss' ) AS create_date 
FROM
	( SELECT * FROM cdr_v_MedicalRecordMain WHERE id IN ( SELECT DISTINCT MedicalRecordID FROM skzbk.fs_medicalrecordmain_ls_temp ) ) a
	JOIN ( SELECT DISTINCT empi, patientno FROM dw.empi_cdw WHERE effect_flag = 1 ) c ON a.PatientNo = c.PatientNo
	LEFT JOIN ( SELECT * FROM cdr_v_MEDICALRECORDDIAGNOSE WHERE isprimary = 1) b ON a.id = b.medicalrecordid 
GROUP BY
	c.EMPI,
	a.patientno,
	a.recordnumber,
	a.healthcardnumber,
	a.encounterid,
	a.PatientName,
	a.age,
	a.inpatientnumber,
	a.outpatientnumber,
	a.inhospitaltime,
	a.outhospitaltime,
	a.payway,
	a.inhospitaldeptcode,
	a.inhospitaldeptname,
	a.inhospitalway,
	a.outhospitalway,
	a.outhospitaldeptcode,
	a.outhospitaldeptname,
	a.attendingdoctorname,
	a.inhospitaltotalcost 
	) f
'''

sql_5 = '''
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
	'42502657200' AS hospital_code,
	0 AS delete_flag,
	FROM_UNIXTIME( UNIX_TIMESTAMP( ), 'yyyy-MM-dd HH:mm:ss' ) AS create_date 
FROM
	( SELECT * FROM cdr_v_MedicalRecordMain WHERE id IN ( SELECT DISTINCT id FROM skzbk.fs_medicalrecordmain_ls_temp2 ) ) a
	left JOIN ( SELECT * FROM cdr_v_MEDICALRECORDDIAGNOSE) b ON a.id = b.medicalrecordid
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
	b.diagnosename
	) f
'''

sql_5_ist = '''
insert into form_diagnose_info_temp(
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
hospital_code,
delete_flag,
create_date,
is_die,
inpatient_times) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 51 - form_diahnose_info 增加 diagnosetype
sql_51_old = '''
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
	'42502657200' AS hospital_code,
	0 AS delete_flag,
	FROM_UNIXTIME( UNIX_TIMESTAMP( ), 'yyyy-MM-dd HH:mm:ss' ) AS create_date
FROM
	( SELECT * FROM cdr_v_MedicalRecordMain WHERE id IN ( SELECT DISTINCT id FROM skzbk.fs_medicalrecordmain_ls_temp2 ) ) a
	left JOIN ( SELECT * FROM cdr_v_MEDICALRECORDDIAGNOSE) b ON a.id = b.medicalrecordid
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
	b.diagnosetype
	) f
'''

# 修改到病人诊断表
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
	b.diagnosetype
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
hospital_code,
delete_flag,
create_date,
is_die,
inpatient_times) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 6 - form_diagnose_detail
sql_6 = '''
select distinct NVL(c.EMPI, c.patientno) AS EMPI, a.PatientNo as patient_no, a.encounterid as encounter_id, a.PatientName as patient_name, a.inhospitaltime as inhospital_time, a.outhospitaltime as outhospital_time, a.inpatientnumber as inpatient_number, a.outpatientnumber as outpatient_number, b.diagnosetime as diagnose_time, substr(b.diagnosetime, 0, 10) as diagnose_time_var, b.isprimary as isprimary, b.diagnosecode as diagnose_code, b.diagnosename as diagnose_name, '42502657200' as hospital_code, 0 as delete_flag, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
from cdr_v_MedicalRecordMain a 
JOIN (SELECT * FROM cdr_v_PATIENTDIAGNOSIS WHERE diagnosetype = 2) b
ON a.patientno = b.patientno and a.encounterid = b.encounterid 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) c 
ON a.PatientNo = c.PatientNo 
WHERE a.PatientNo in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp) AND (TRIM(b.DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) AND b.diagnosetype = 2
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
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
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
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d
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
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='3024' AND Value>=50 AND Value<=250) b WHERE b.rank = 1) c -- 身高
ON a.PatientNo = c.PatientNo and a.encounterid = c.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='1014' AND Value>=20 AND Value<=200) d WHERE d.rank = 1) e -- 体重 
ON a.PatientNo = e.PatientNo and a.encounterid = e.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='1001' AND Value>=33 AND Value<=43) f WHERE f.rank = 1) g -- 体温 
ON a.PatientNo = g.PatientNo and a.encounterid = g.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='128') h WHERE h.rank = 1) i -- 收缩压 
ON a.PatientNo = i.PatientNo and a.encounterid = i.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='1004' AND Value>=20 AND Value<=200) l WHERE l.rank = 1) m -- 呼吸频率 
ON a.PatientNo = m.PatientNo and a.encounterid = m.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='113' AND Value>=30 AND Value<=200) n WHERE n.rank = 1) o -- 心率 
ON a.PatientNo = o.PatientNo and a.encounterid = o.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='129' AND Value>=30 AND Value<=200) p WHERE p.rank = 1) q -- 氧饱和度 
ON a.PatientNo = q.PatientNo and a.encounterid = q.encounterid 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) r 
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

# 10 - form_physical_exam_info 心动图骨密度
#sql_10 = '''
#SELECT distinct NVL(f.EMPI, f.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(e.IDNumber, 4, length(e.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, e.InpatientNumber as inpatient_number, e.OutpatientNumber as outpatient_number, c.EncounterType as encounter_type, CASE WHEN a.inspectionprojectname LIKE '%骨密度%' THEN 25 ELSE 21 end as question_id, d.ReportID as report_id, c.TSExam as ts_exam, substr(c.TSExam, 0, 10) as ts_exam_var, d.examName as exam_name, c.ReportName as report_name, d.ExamFind as exam_find, d.ExamConclusion as exam_conclusion, d.BodySite as body_site, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date, c.reportclasscode as report_class_code, c.reportclassname as report_class_name, a.inspectionprojectname as inspection_project_name, a.inspectionprojectname as inspection_project_name 
#FROM cdr_V_INSPECTIONSHEETDETAIL a 
#JOIN cdr_V_INSPECTIONSHEETREPORT b 
#ON a.sheetid = b.sheetid and a.sheetno = b.sheetno 
#JOIN cdr_V_OTHERREPORT c -- B超报告（UltrasoundReport）
#ON b.reportid = c.id 
#JOIN cdr_V_OTHERRESULT d -- B超报告项目结果（UltrasoundResult）
#ON c.id = d.ReportID 
#JOIN cdr_V_MedicalRecordMain e -- 病案首页（MedicalRecordMain）
#ON c.PatientNo = e.PatientNo 
#JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) f 
#ON c.PatientNo = f.PatientNo and c.encounterid = e.encounterid 
#WHERE e.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) AND (b.inspectionprojectname LIKE '%骨密度%' or b.inspectionprojectname LIKE '%超声心动图%')
#'''

# - form_ris_info

# SELECT CASE WHEN a.reportclasscode='Electrocardio' and a.reportname like '%心电图%' THEN 20 WHEN a.reportname like '%心脏%彩超%' THEN 21 WHEN a.reportclasscode in ('Ultrasound', 'US') THEN 22 WHEN reportname='CT报告' and bodysite='胸部' THEN 23 WHEN reportname='CT报告' and bodysite like '%腹部%' THEN 24 ELSE NULL END as question_id 
sql_10_old = '''
SELECT 
distinct NVL(d.EMPI, d.PatientNo) AS EMPI, 
a.PatientNo as patient_no,
CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, 
a.EncounterID as encounter_id, 
c.InpatientNumber as inpatient_number, 
c.OutpatientNumber as outpatient_number, 
a.EncounterType as encounter_type, 
CASE WHEN a.reportclasscode='Electrocardio' and a.reportname like '%心电图%' THEN 20 WHEN a.reportname like '%心脏%彩超%' THEN 21 WHEN a.reportclasscode in ('Ultrasound', 'US') THEN 22 WHEN reportname='CT报告' and bodysite='胸部' THEN 23 WHEN reportname='CT报告' and bodysite like '%腹部%' THEN 24 ELSE NULL END as question_id, 
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
a.inspectionprojectname as inspection_project_name, 
b.summarynote as summary_note 
FROM cdr_V_OTHERREPORT a -- B超报告（UltrasoundReport）
JOIN cdr_V_OTHERRESULT b -- B超报告项目结果（UltrasoundResult）
ON a.id = b.ReportID 
JOIN cdr_V_MedicalRecordMain c -- 病案首页（MedicalRecordMain）
ON a.PatientNo = c.PatientNo and a.encounterid = c.encounterid 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON a.PatientNo = d.PatientNo 
WHERE c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) 
and (a.reportclasscode='Electrocardio' and a.reportname like '%心电图%') or a.reportname like '%心脏%彩超%' or  (a.reportclasscode in ('Ultrasound', 'US') and (b.ExamFind like '%肝%' or b.ExamFind like '%胆%' or b.ExamFind like '%胰%' or b.ExamFind like '%脾%' or b.ExamFind like '%肾%' or b.ExamFind like '%甲状腺%')) or (a.reportname='CT报告' and (b.bodysite='胸部' or b.bodysite like '%腹部%'));
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
CASE WHEN a.reportclasscode='Electrocardio' and a.reportname like '%心电图%' THEN 20 WHEN a.reportname like '%心脏%彩超%' THEN 21 WHEN a.reportclasscode in ('Ultrasound', 'US') THEN 22 WHEN reportname='CT报告' and bodysite='胸部' THEN 23 WHEN reportname='CT报告' and bodysite like '%腹部%' THEN 24 ELSE NULL END as question_id, 
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
JOIN cdr_V_MedicalRecordMain c -- 病案首页（MedicalRecordMain）
ON a.PatientNo = c.PatientNo and a.encounterid = c.encounterid 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON a.PatientNo = d.PatientNo 
join (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) h
on c.id = h.medicalrecordid
where (a.reportclasscode='Electrocardio' and a.reportname like '%心电图%') or a.reportname like '%心脏%彩超%' or  (a.reportclasscode in ('Ultrasound', 'US') and (b.ExamFind like '%肝%' or b.ExamFind like '%胆%' or b.ExamFind like '%胰%' or b.ExamFind like '%脾%' or b.ExamFind like '%肾%' or b.ExamFind like '%甲状腺%')) or (a.reportname='CT报告' and (b.bodysite='胸部' or b.bodysite like '%腹部%'))
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
summary_note) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 11 - form_lab_info

from generate_lab_code_2 import generate_sql_11

sql_11 = generate_sql_11()

# 抽取所有检查，进行分析
sql_11_0 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 27 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, b.TestItemName as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))
and to_date(c.inhospitaltime) < to_date('2018-05-03') and to_date(c.inhospitaltime) > to_date('2017-01-01')
'''
# and to_date(c.inhospitaltime) > to_date('2020-11-30')

sql_110 = '''
SELECT a.test_order as Examclasscode, a.test_order_name as Examclassname, c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 27 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, a.Reportname as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+'))
and to_date(c.inhospitaltime) > to_date('2020-05-02')
'''
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

# 住院最近的一次（利用时间相减排序，去重）、修改查询规则
## 血常规
sql_11_1 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 27 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, b.TestItemName as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '5925' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS40068') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5938' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5938' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5938' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS39943'))
'''

# where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and (b.TestItemName = '白细胞计数' or b.TestItemName = '红细胞计数' or b.TestItemName = '血红蛋白' or b.TestItemName = '血小板计数' or b.TestItemName = '嗜中性粒细胞绝对值' or b.TestItemName = '淋巴细胞绝对值' or b.TestItemName = '单核细胞绝对值' or b.TestItemName = '网织红细胞比率')

# (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS40068') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5938' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5938' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5938' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS39943')

##  尿常规
sql_11_2 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 28 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, b.TestItemName as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '5907' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5894' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5893' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7559' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5902' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7639' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5898' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7555' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7645' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '6967' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5904' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7640' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5892' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7556' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7615' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7616' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = 'PRO') or (b.TestItemCode = '5893')) and a.SpecimenClassName LIKE '%尿%'
'''

##  尿蛋白定量
sql_11_3 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 29 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '尿总蛋白肌酐比' then '尿总蛋白/肌酐比' WHEN b.TestItemName = '尿白蛋白/肌酐比值' then '尿白蛋白/肌酐比' WHEN b.TestItemName = '尿白蛋白肌酐比' then '尿白蛋白/肌酐比' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '5109' and a.specimenclasscode = 'LIS1077') or (b.TestItemCode = '5109' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = 'ACR') or (b.TestItemCode = '5105' and a.specimenclasscode = 'LIS40702') or (b.TestItemCode = '5105' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7465' and a.specimenclasscode = 'LIS40702'))
'''

##  脑脊液检查
sql_11_4 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 30 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '潘氏试验(脑脊液)' then '脑脊液常规 - 潘氏试验' WHEN b.TestItemName = '潘式试验（脑脊液）' then '脑脊液常规 - 潘氏试验' WHEN b.TestItemName = '脑脊液白细胞数' then '脑脊液常规 - 白细胞计数' WHEN b.TestItemName = '白细胞数(脑脊液)' then '脑脊液常规 - 白细胞计数' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '5103' and a.specimenclasscode = 'LIS1048') or (b.TestItemCode = '7770' and a.specimenclasscode = 'LIS1048') or (b.TestItemCode = '7033' and a.specimenclasscode = 'LIS1048') or (b.TestItemCode = '5104' and a.specimenclasscode = 'LIS1048') or (b.TestItemCode = '5106' and a.specimenclasscode = 'LIS1048') or (b.TestItemCode = '7600' and a.specimenclasscode = 'LIS1048') or (b.TestItemCode = '5088' and a.specimenclasscode = 'LIS1048') or (b.TestItemCode = '6346' and a.specimenclasscode = 'LIS1048') or (b.TestItemCode = '7771' and a.specimenclasscode = 'LIS1048') or (b.TestItemCode = '6314' and a.specimenclasscode = 'LIS1048'))
'''

##  出凝血相关
sql_11_5 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 31 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '纤维蛋白（原）降解物' then '纤维蛋白(原)降解产物' WHEN b.TestItemName = '纤维蛋白(原)降解物' then '纤维蛋白(原)降解产物' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '5986' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5986' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5986' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5996' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5996' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5996' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5996' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5996' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5996' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6007' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7578' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6007' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6007' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7578' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7578' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5997' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5997' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7850' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7850' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5997' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5993' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5993' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5993' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6441' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6441' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6441' and a.specimenclasscode = 'LIS5'))
'''

##  血生化和电解质
sql_11_6 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 32 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = 'γ谷氨酰基转移酶' then 'γ谷氨酰转肽酶' WHEN b.TestItemName = 'γ-谷氨酰转肽酶' then 'γ谷氨酰转肽酶' WHEN b.TestItemName = '肌酸激酶（CK-MB）' then '肌酸激酶' WHEN b.TestItemName = '糖化血红蛋白-A1c' then '糖化血红蛋白' WHEN b.TestItemName = '25-羟基维生素D' then '25-羟基维生素D(VITD)' WHEN b.TestItemName = '甘油三脂' then '甘油三酯' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '5079' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5079' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5079' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6891' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6891' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5073' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5073' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5039' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5039' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5039' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7013' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7013' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5077' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5077' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7011' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7011' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5064' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5064' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5049' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5049' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5049' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6893' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7091' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7091' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5038' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7010' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5038' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7010' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5038' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5060' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6892' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6892' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7703' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5046' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5046' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6889' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5052' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5052' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5052' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6890' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6890' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6890' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5053' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5053' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7702' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5080' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7702' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7702' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5080' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'jzALT') or (b.TestItemCode = 'ALT') or (b.TestItemCode = '5048' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5048' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7700' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5066' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7700' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7700' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5066' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5254' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5254' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7703' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5065' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5065' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6888' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5065' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6888' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'HbA1C') or (b.TestItemCode = '5067' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5067' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5110' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5110' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6894' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5110' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7701' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5070' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7701' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7701' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5070' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7092' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7092' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7094' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5074' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5074' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5068' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5068' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5076' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5436' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5436' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7093' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5055' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5055' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6905' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6905' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7012' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6905' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7012' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5043' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5043' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6887' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5043' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6887' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5076' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5040' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5040' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6886'))
'''

##  心梗标志物和甲状腺相关
sql_11_7 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, CASE WHEN b.TestItemName = '肌钙蛋白I' or b.TestItemName = 'BNP' THEN 33 ELSE 34 END as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, b.TestItemName as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '6453' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6449' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7016' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7016' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7016' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6449' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6449' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6449' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5467' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5467' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7712' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7712' and a.specimenclasscode = 'LIS39981') or (b.TestItemCode = '5198' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5202' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5202' and a.specimenclasscode = 'LIS39981') or (b.TestItemCode = '5202' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7725' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7725' and a.specimenclasscode = 'LIS39981') or (b.TestItemCode = '7361' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7361' and a.specimenclasscode = 'LIS39981') or (b.TestItemCode = '7713' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7713' and a.specimenclasscode = 'LIS39981') or (b.TestItemCode = '5197' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7713' and a.specimenclasscode = 'LIS5'))
'''

##  炎症标志物和免疫球蛋白
sql_11_8 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, CASE WHEN b.TestItemName = '红细胞沉降率ESR' or b.TestItemName = 'C反应蛋白' or b.TestItemName = 'C-反应蛋白' THEN 35 ELSE 36 END as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '免疫固定电泳IgG' then '免疫固定电泳 - IgG带' WHEN b.TestItemName = '免疫固定电泳IgA' then '免疫固定电泳 - IgA带' WHEN b.TestItemName = '免疫固定电泳IgM' then '免疫固定电泳 - IgM带' WHEN b.TestItemName = '免疫固定电泳kap' then '免疫固定电泳 - κ带' WHEN b.TestItemName = '免疫固定电泳lam' then '免疫固定电泳 - λ带' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '5559' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5559' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5559' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6882' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6882' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6882' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6882' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5980' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5980' and a.specimenclasscode = 'LIS40068') or (b.TestItemCode = '7325') or (b.TestItemCode = '5571' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5571' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'mygddyigm') or (b.TestItemCode = '7329') or (b.TestItemCode = '5563' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5563' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5567' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5567' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'mygddyiga') or (b.TestItemCode = 'mygddyigg') or (b.TestItemCode = '7328') or (b.TestItemCode = 'IGG4') or (b.TestItemCode = '7503' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7327') or (b.TestItemCode = '7326'))
'''

##  感染相关和补体相关
sql_11_9 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, CASE WHEN b.TestItemName = '总补体活性CH50' or b.TestItemName = '补体C3' or b.TestItemName = '补体C4' or b.TestItemName = 'C1抑制剂' or b.TestItemName = '补体C1Q' or b.TestItemName = '补体C1q' THEN 38 ELSE 37 END as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '乙肝e抗原' then '乙肝E抗原' WHEN b.TestItemName = '乙肝e抗体' then '乙肝E抗体' WHEN b.TestItemName = '抗EB病毒衣壳抗原IgG亲合力' then '抗EB病毒衣壳抗原IgG亲和力' WHEN b.TestItemName = '补体C1q' then '补体C1Q' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = 'HBeAg') or (b.TestItemCode = '5656' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5656' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5656' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5636' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5636' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5636' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7398' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7398' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6219' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6219' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7057' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5704' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5704' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5704' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6221' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7109' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7109' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7950' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7889' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7889' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5150' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5150' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7399' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7399' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5655' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5655' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5655' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7891' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7891' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'HBeAb') or (b.TestItemCode = '6228' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6228' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5705' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5705' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5705' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6229' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6229' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7898' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7898' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7115' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7115' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7017' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7017' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7017' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7017' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7192' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7192' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7149' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5554' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7149' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5554' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7148' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7148' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7118' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5555' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7150' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5555' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7150' and a.specimenclasscode = 'LIS5'))
'''

##  Coobm`s试验和其他自身抗体
sql_11_10 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, CASE WHEN b.TestItemName = '直抗' or b.TestItemName = '抗IgG' or b.TestItemName = '抗C3' or b.TestItemName = '抗体筛选' THEN 39 ELSE 40 END as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '直抗' then "Coomb's试验-直抗" WHEN b.TestItemName = '抗IgG' then "Coomb's试验-抗IgG" WHEN b.TestItemName = '抗C3' then "Coomb's试验-抗C3" WHEN b.TestItemName = '抗体筛选' then "Coomb's试验-抗体筛选" WHEN b.TestItemName = '抗GP Ⅸ抗体' then "抗血小板抗体 - 抗GP IX抗体" WHEN b.TestItemName = '抗GPⅠb抗体' then "抗血小板抗体 - 抗GP Ib抗体" WHEN b.TestItemName = '抗GP Ⅲa抗体' then "抗血小板抗体 - 抗GP IIIa抗体" WHEN b.TestItemName = '抗GP Ⅱb抗体' then "抗血小板抗体 - 抗GP IIb抗体" WHEN b.TestItemName = '抗GMP 140抗体' then "抗血小板抗体 - 抗GMP 140抗体" WHEN b.TestItemName = '线粒体抗体(AMA)' then "线粒体抗体（AMA）" WHEN b.TestItemName = '抗平滑肌抗体(ASMA)' then "抗平滑肌抗体（ASMA）" WHEN b.TestItemName = '抗可溶性肝抗原/肝胰抗原(SLA/LP)' then "抗可溶性肝抗体/肝胰抗原（SLA/LP）" WHEN b.TestItemName = '抗肝溶质抗1型抗原(LC-1)抗体' then "抗肝溶质抗1型抗原（LC-1）抗体" WHEN b.TestItemName = '抗肝肾微粒体(LKM-1)抗体' then "抗肝肾微粒体（LKM-1）抗体" WHEN b.TestItemName = '抗糖蛋白210(gp210)抗体' then "抗糖蛋白201（gp210）抗体" WHEN b.TestItemName = '抗早幼粒细胞白血病蛋白(PML)抗体' then "抗早幼粒细胞白血病蛋白（PML）抗体" WHEN b.TestItemName = '抗斑点蛋白(Sp100)抗体' then "抗斑点蛋白（Sp100）抗体" WHEN b.TestItemName = '抗2-丙酮酸脱氢酶(M2-3E)抗体' then "抗2-丙酮酸脱氢酶（M2-3E）抗体" else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '295037' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = "coomb's4") or (b.TestItemCode = '295036' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '295038' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8835' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8315' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8348' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8348' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7065' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5732' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5729' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5729' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7362' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5203' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7169' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7362' and a.specimenclasscode = 'LIS39981') or (b.TestItemCode = '6399' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6399' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8349' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8349' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6931' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6931' and a.specimenclasscode = 'LIS39981') or (b.TestItemCode = '8396' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8833' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8837' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8347' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8347' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5731' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5733' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5733' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5730' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6401' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6401' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6398' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6398' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8836' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7245' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7064' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7714' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7714' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5204' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7714' and a.specimenclasscode = 'LIS39981') or (b.TestItemCode = '5765' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5765' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8317' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6711' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6711' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6921' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7063' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5764' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5764' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6699' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8834' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6995' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8319' and a.specimenclasscode = 'LIS1075'))
'''

##  ANA+ENA+dsDNA组合
sql_11_11 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 41 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '抗SM' then '抗Sm' WHEN b.TestItemName = '抗SSB/La抗体' then '抗SSB/La' WHEN b.TestItemName = '抗Jo-1抗体' then '抗Jo-1' WHEN b.TestItemName = '抗核小体抗体' then '核小体抗体' WHEN b.TestItemName = '抗ds-DNA(ELISA法)' then '抗ds-DNA(ELISA法）' WHEN b.TestItemName = '抗ds-DNA(短膜虫法)' then '抗ds-DNA（短膜虫法）' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '7449' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7449' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5645' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5650' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5650' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5735' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5735' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6709' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8809' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6709' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5729') or (b.TestItemCode = '5652' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5652' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7081' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5641' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5641' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7080' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6707') or (b.TestItemCode = '6708' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6708' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'SM') or (b.TestItemCode = '5642' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5642' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7899' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7899' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5649' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5649' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7078' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = 'ScL-70') or (b.TestItemCode = '7079' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5653' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5650' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5653' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6400' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6400' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5651' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5651' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7082' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5652' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5641' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8593' and a.specimenclasscode = 'LIS1075'))
'''

##  抗磷脂抗体相关
sql_11_12 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 42 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '标准化狼疮比值' then '狼疮抗凝物-标准化狼疮比值（TR）' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '7069' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7069' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6947' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6947' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7051' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7070' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7070' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7071' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7071' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7052' and a.specimenclasscode = 'LIS1075'))
'''

##  免疫细胞分型
sql_11_13 = '''
SELECT c.inhospitaltime as in_hospital_date, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, CONCAT('***', SUBSTRING(c.IDNumber, 4, length(c.IDNumber)-7), '0000') as id_number, c.EncounterID as encounter_id, a.EncounterType as encounter_type, c.InpatientNumber as inpatient_number, c.OutpatientNumber as outpatient_number, 43 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '淋巴细胞绝对值（CD45+）' then '淋巴细胞(CD45+)绝对值' WHEN b.TestItemName = 'T淋巴细胞绝对值' then 'T淋巴细胞(CD3+)绝对值' WHEN b.TestItemName = 'T淋巴细胞（CD3+）' or b.TestItemName = 'T淋巴细胞CD3' then 'T淋巴细胞(CD3+)' WHEN b.TestItemName = 'Ts淋巴细胞绝对值' then 'Ts淋巴细胞(CD3+CD8+)绝对值' WHEN b.TestItemName = 'Th淋巴细胞绝对值' then 'Th淋巴细胞(CD3+CD4+)绝对值' WHEN b.TestItemName = 'Th淋巴细胞（CD3+CD4+）' then 'Th淋巴细胞(CD3+CD4+)' WHEN b.TestItemName = 'B淋巴细胞绝对值' then 'B淋巴细胞(CD3-CD19+)绝对值' WHEN b.TestItemName = 'B淋巴细胞（CD3-CD19+）' then 'B淋巴细胞(CD3-CD19+)' WHEN b.TestItemName = '自然杀伤细胞绝对值' then '自然杀伤细胞(CD3-CD16+CD56+)绝对值' WHEN b.TestItemName = 'CD3-CD20+' then 'CD20细胞比值(CD3-CD20+)' WHEN b.TestItemName = 'CD45/3/14/38/19/27(浆细胞/B细胞比率)' then '浆细胞(CD45/3/14/38/19/27)' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_MedicalRecordMain c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.EncounterID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where c.id in (SELECT medicalrecordid FROM cdr_v_MedicalRecordDiagnose WHERE TRIM(DiagnoseCode) IN ('A18.400x001', 'A18.409', 'A18.410', 'D68.600x011', 'D86.300x002', 'F06.800x021', 'H01.100x006', 'K71.500x002', 'K73.200x011', 'K75.400x001', 'L73.801', 'L93.000x002', 'L93.001', 'L93.100', 'L93.200', 'L93.200x001', 'L93.200x003', 'L93.201', 'L93.202', 'M32.000', 'M32.100', 'M32.100x001', 'M32.100x006', 'M32.100x007', 'M32.100x008', 'M32.100x014', 'M32.100x016', 'M32.100x018', 'M32.100x021', 'M32.101†', 'M32.102†', 'M32.103†', 'M32.104†', 'M32.105†', 'M32.106†', 'M32.107†', 'M32.108†', 'M32.109†', 'M32.110†', 'M32.111†', 'M32.112†', 'M32.113†', 'M32.114†', 'M32.115†', 'M32.800', 'M32.900', 'M32.901', 'O99.811', 'M32.101+', 'M32.102+', 'M32.103+', 'M32.104+', 'M32.105+', 'M32.106+', 'M32.107+', 'M32.108+', 'M32.109+', 'M32.110+', 'M32.111+', 'M32.112+', 'M32.113+', 'M32.114+', 'M32.115+')) and ((b.TestItemCode = '6955' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7339' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7339' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5432' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5432' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6953' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6953' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6181' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6181' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7337' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7337' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6959' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6959' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6956' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6956' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6960') or (b.TestItemCode = '6181' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '8488' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5538' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5538' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8109' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8109' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6958' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6958' and a.specimenclasscode = 'LIS5'))
'''


sql_11_ist = '''
insert into form_lab_info_temp(
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
ts_draw_var) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 12 - cdr_patient_info

sql_12 = '''
SELECT distinct m.empi as empi, a.patientno as patient_no, a.patientname as patient_name, a.sexname as sex, c.age as age, a.idno as id_number, a.cardno as card_no, d.AdmissionNumber as inpatient_number, d.inhospitaldatetime as in_hospital_date_time, d.PrimaryDiagnosis as inpatient_primary_diagnose, c.OperateDate as operate_date, e.PatID as outpatient_number, e.VisitDateTime as visit_date_time, e.PrimaryDiagnosis as outpatient_primary_diagnose, c.HospitalCode as hospital_code, c.HospitalName as hospital_name 
FROM cdr_V_PatientBasicInformation a 
join (SELECT * FROM (select f.*, row_number() over(partition by f.patientno order by f.OperateDate desc) as rn from (SELECT b.patientno, b.age, b.HospitalCode, b.HospitalName, l.* from cdr_V_MedicalRecordMain b join cdr_V_MedicalRecordOperate l on b.id = l.MedicalRecordID WHERE year(b.InHospitalTime) = 2021) f) g WHERE g.rn = 1) c 
on a.patientno = c.patientno 
join (SELECT * FROM (select h.*, row_number() over(partition by h.patientno order by h.inhospitaldatetime desc) as rn from cdr_V_InpatientVisitRecord h WHERE year(h.inhospitaldatetime) = 2021) i WHERE i.rn = 1) d 
on a.patientno = d.patientno 
join (SELECT * FROM (select j.*, row_number() over(partition by j.patientno order by j.VisitDateTime desc) as rn from cdr_V_OutpatientVisitRecord j WHERE year(j.VisitDateTime) = 2021) k WHERE k.rn = 1) e 
on a.patientno = e.patientno 
join (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) m 
on a.patientno = m.patientno 
where year(c.OperateDate) = 2021
'''

sql_12_ist = '''
insert into cdr_patient_info_temp(
empi,
patient_no, 
patient_name,
sex,
age,
id_number,
card_no,
inpatient_number,
in_hospital_date_time,
inpatient_primary_diagnose,
operate_date,
outpatient_number,
visit_date_time,
outpatient_primary_diagnose,
hospital_code,
hospital_name) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# 15 - 门诊诊断 form_focus_diagnosis_followup

# visit_date都为空 
# 直接抽门诊就诊记录
sql_15_old = '''
select 
distinct
b.empi as empi,
b.PatientNo as patient_no,
a.patientname as patient_name,
a.patid as outpatient_number,
a.visittime as visit_time,
a.visitdate as visit_date,
a.categoryname as category_name,
a.primarydiagnosis as primary_diagnosis,
a.primarydiagnosiscode as primary_diagnosis_code
FROM cdr_v_OUTPATIENTVISITRECORD a 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) b 
ON a.PatientNo=b.PatientNo
WHERE a.PatientNo 
in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)
'''

# 关联诊断表
sql_15_old2 = '''
select 
distinct
b.empi as empi,
b.PatientNo as patient_no,
a.patientname as patient_name,
a.patid as outpatient_number,
c.diagnosetime as visit_time,
a.visitdate as visit_date,
c.encountertype as category_name,
c.diagnosename as primary_diagnosis,
c.diagnosecode as primary_diagnosis_code
FROM cdr_v_OUTPATIENTVISITRECORD a 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) b 
ON a.PatientNo=b.PatientNo
JOIN cdr_v_PATIENTDIAGNOSIS c
ON a.PatientNo=c.PatientNo and a.id = c.encounterid
WHERE a.PatientNo 
in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)
and c.isprimary = '1'
'''

# 直接抽门诊就诊记录，换时间
sql_15_old3 = '''
select 
distinct
b.empi as empi,
b.PatientNo as patient_no,
a.id as encounter_id,
a.patientname as patient_name,
a.patid as outpatient_number,
a.registrationdatetime as registrationdatetime,
a.visitdatetime as visitdatetime,
a.categoryname as category_name,
a.primarydiagnosis as primary_diagnosis,
a.primarydiagnosiscode as primary_diagnosis_code
FROM cdr_v_OUTPATIENTVISITRECORD a 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) b 
ON a.PatientNo=b.PatientNo
WHERE a.PatientNo 
in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)
'''

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
c.diagnosecode as primary_diagnosis_code
FROM cdr_v_OUTPATIENTVISITRECORD a 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1) b 
ON a.PatientNo=b.PatientNo
JOIN (select * from cdr_v_PATIENTDIAGNOSIS where  diagnosetype = 0 and isprimary = 1) c
ON a.PatientNo=c.PatientNo and a.id = c.encounterid
WHERE a.PatientNo 
in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)
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
primary_diagnosis_code
) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''


# 16 - form_physical_exam_info_followup
# 数据都是空的
sql_16 = '''
SELECT 
NVL(r.EMPI, r.PatientNo) AS EMPI, 
a.PatientNo as patient_no, 
a.patid as outpatient_number, 
c.operatedate as operate_date, 
substr(c.operatedate, 0, 10) as operate_date_var, 
c.Value as height, 
e.Value as weight, 
g.Value as temperature, 
CASE WHEN i.Value IS NOT NULL THEN split(i.Value, '/')[0] ELSE NULL END as systolic, 
CASE WHEN i.Value IS NOT NULL THEN split(i.Value, '/')[1] ELSE NULL END as diastolic,
m.Value as respiratory_rate, 
o.Value as heart_rate, 
q.Value as oxygen_saturation, 
'42502657200' as hospital_code, 
FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date 
FROM cdr_v_OUTPATIENTVISITRECORD a 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='3024' AND Value>=50 AND Value<=250) b WHERE b.rank = 1) c -- 身高
ON a.PatientNo = c.PatientNo and a.id = c.encounterid
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='1014' AND Value>=20 AND Value<=200) d WHERE d.rank = 1) e -- 体重 
ON a.PatientNo = e.PatientNo and a.id = e.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='1001' AND Value>=33 AND Value<=43) f WHERE f.rank = 1) g -- 体温 
ON a.PatientNo = g.PatientNo and a.id = g.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='128') h WHERE h.rank = 1) i -- 收缩压 
ON a.PatientNo = i.PatientNo and a.id = i.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='1004' AND Value>=20 AND Value<=200) l WHERE l.rank = 1) m -- 呼吸频率 
ON a.PatientNo = m.PatientNo and a.id = m.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='113' AND Value>=30 AND Value<=200) n WHERE n.rank = 1) o -- 心率 
ON a.PatientNo = o.PatientNo and a.id = o.encounterid 
LEFT JOIN 
(select * from (SELECT patientno, encounterid, operatedate, Value, row_number() over (partition by patientno, encounterid order by operatedate desc) rank FROM cdr_v_PATIENTVITALSIGN WHERE VitalSignId='129' AND Value>=30 AND Value<=200) p WHERE p.rank = 1) q -- 氧饱和度 
ON a.PatientNo = q.PatientNo and a.id = q.encounterid 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) r 
ON a.PatientNo = r.PatientNo 
'''

sql_16_ist = '''
insert into form_physical_exam_info_followup_temp(
empi,
patient_no, 
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
create_date ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
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
in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)
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

from generate_lab_code_2 import generate_sql_18_sf

sql_18 = generate_sql_18_sf()

# 心动图和骨密度，有4条数据

sql_18_0 = '''
SELECT 
distinct NVL(f.EMPI, f.PatientNo) AS EMPI, 
c.PatientNo as patient_no, 
c.EncounterID as encounter_id, 
e.patid as outpatient_number, 
c.EncounterType as encounter_type, 
CASE WHEN a.inspectionprojectname LIKE '%骨密度%' THEN 63 ELSE 62 end as question_id,
d.ReportID as report_id, 
c.TSExam as ts_exam, 
substr(c.TSExam, 0, 10) as ts_exam_var, 
d.examName as exam_name, 
c.ReportName as report_name, 
d.ExamFind as exam_find, 
d.ExamConclusion as exam_conclusion, 
d.BodySite as body_site, 
FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date, 
c.reportclasscode as report_class_code, 
c.reportclassname as report_class_name,
a.inspectionprojectname as inspection_project_name, 
a.inspectionprojectcode as inspection_project_code 
FROM cdr_V_INSPECTIONSHEETDETAIL a 
JOIN cdr_V_INSPECTIONSHEETREPORT b 
ON a.sheetid = b.sheetid and a.sheetno = b.sheetno 
JOIN cdr_V_OTHERREPORT c -- B超报告（UltrasoundReport）
ON b.reportid = c.id 
JOIN cdr_V_OTHERRESULT d -- B超报告项目结果（UltrasoundResult）
ON c.id = d.ReportID 
JOIN cdr_V_OUTPATIENTVISITRECORD e -- 门诊
ON c.PatientNo = e.PatientNo and c.Encounterid = e.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) f 
ON c.PatientNo = f.PatientNo
where (a.inspectionprojectname LIKE '%骨密度%' or a.inspectionprojectname LIKE '%超声心动图%');
'''



#-- 血常规
sql_18_1 = '''
SELECT c.visittime as visittime, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, null as id_number, c.ID as encounter_id, a.EncounterType as encounter_type, c.patid as patid, c.visitdate as visitdate, 27 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, b.TestItemName as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_OUTPATIENTVISITRECORD c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where ((b.TestItemCode = '5925' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5925' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6107' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS40068') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5960' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5932' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5914' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5938' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5938' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5938' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS39943') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5934' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5957' and a.specimenclasscode = 'LIS39943'))
'''

# -- 尿常规
sql_18_2 = '''
SELECT c.visittime as visittime, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, null as id_number, c.ID as encounter_id, a.EncounterType as encounter_type, c.patid as patid, c.visitdate as visitdate, 28 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, b.TestItemName as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_OUTPATIENTVISITRECORD c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where ((b.TestItemCode = '5907' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5894' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5893' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7559' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5902' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7639' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5898' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7555' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7645' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '6967' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5904' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7640' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '5892' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7556' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7615' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7616' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = 'PRO') or (b.TestItemCode = '5893')) and a.SpecimenClassName LIKE '%尿%'
'''

# -- 尿蛋白定量
sql_18_3 = '''
SELECT c.visittime as visittime, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, null as id_number, c.ID as encounter_id, a.EncounterType as encounter_type, c.patid as patid, c.visitdate as visitdate, 29 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '尿总蛋白肌酐比' then '尿总蛋白/肌酐比' WHEN b.TestItemName = '尿白蛋白/肌酐比值' then '尿白蛋白/肌酐比' WHEN b.TestItemName = '尿白蛋白肌酐比' then '尿白蛋白/肌酐比' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_OUTPATIENTVISITRECORD c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where ((b.TestItemCode = '5109' and a.specimenclasscode = 'LIS1077') or (b.TestItemCode = '5109' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = 'ACR') or (b.TestItemCode = '5105' and a.specimenclasscode = 'LIS40702') or (b.TestItemCode = '5105' and a.specimenclasscode = 'LIS7') or (b.TestItemCode = '7465' and a.specimenclasscode = 'LIS40702'))
'''

# -- 血生化和电解质
sql_18_4 = '''
SELECT c.visittime as visittime, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, null as id_number, c.ID as encounter_id, a.EncounterType as encounter_type, c.patid as patid, c.visitdate as visitdate, 32 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = 'γ谷氨酰基转移酶' then 'γ谷氨酰转肽酶' WHEN b.TestItemName = 'γ-谷氨酰转肽酶' then 'γ谷氨酰转肽酶' WHEN b.TestItemName = '肌酸激酶（CK-MB）' then '肌酸激酶' WHEN b.TestItemName = '糖化血红蛋白-A1c' then '糖化血红蛋白' WHEN b.TestItemName = '25-羟基维生素D' then '25-羟基维生素D(VITD)' WHEN b.TestItemName = '甘油三脂' then '甘油三酯' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_OUTPATIENTVISITRECORD c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where ((b.TestItemCode = '5079' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5079' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5079' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6891' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6891' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5073' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5073' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5039' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5039' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5039' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7013' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7013' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5077' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5077' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7011' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7011' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5064' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5064' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5049' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5049' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5049' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6893' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7091' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7091' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5038' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7010' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5038' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7010' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5038' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5060' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6892' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6892' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7703' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5046' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5046' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6889' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5052' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5052' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5052' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6890' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6890' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6890' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5053' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5053' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7702' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5080' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7702' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7702' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5080' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'jzALT') or (b.TestItemCode = 'ALT') or (b.TestItemCode = '5048' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5048' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7700' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5066' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7700' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7700' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5066' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5254' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5254' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7703' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5065' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5065' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6888' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5065' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6888' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'HbA1C') or (b.TestItemCode = '5067' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5067' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5110' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5110' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6894' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5110' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7701' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5070' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7701' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7701' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5070' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7092' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7092' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7094' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5074' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5074' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5068' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5068' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5076' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5436' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5436' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7093' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5055' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5055' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6905' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6905' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7012' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6905' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7012' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5043' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5043' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6887' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5043' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6887' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5076' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5040' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5040' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6886'))
'''


# -- 炎症标志物和免疫球蛋白
sql_18_5 = '''
SELECT c.visittime as visittime, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, null as id_number, c.ID as encounter_id, a.EncounterType as encounter_type, c.patid as patid, c.visitdate as visitdate, CASE WHEN b.TestItemName = '红细胞沉降率ESR' or b.TestItemName = 'C反应蛋白' or b.TestItemName = 'C-反应蛋白' THEN 35 ELSE 36 END as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '免疫固定电泳IgG' then '免疫固定电泳 - IgG带' WHEN b.TestItemName = '免疫固定电泳IgA' then '免疫固定电泳 - IgA带' WHEN b.TestItemName = '免疫固定电泳IgM' then '免疫固定电泳 - IgM带' WHEN b.TestItemName = '免疫固定电泳kap' then '免疫固定电泳 - κ带' WHEN b.TestItemName = '免疫固定电泳lam' then '免疫固定电泳 - λ带' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_OUTPATIENTVISITRECORD c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where ((b.TestItemCode = '5559' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5559' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5559' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6882' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6882' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6882' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6882' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5980' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5980' and a.specimenclasscode = 'LIS40068') or (b.TestItemCode = '7325') or (b.TestItemCode = '5571' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5571' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'mygddyigm') or (b.TestItemCode = '7329') or (b.TestItemCode = '5563' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5563' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5567' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5567' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'mygddyiga') or (b.TestItemCode = 'mygddyigg') or (b.TestItemCode = '7328') or (b.TestItemCode = 'IGG4') or (b.TestItemCode = '7503' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7327') or (b.TestItemCode = '7326'))
'''

# -- 感染相关和补体相关
sql_18_6 = '''
SELECT c.visittime as visittime, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, null as id_number, c.ID as encounter_id, a.EncounterType as encounter_type, c.patid as patid, c.visitdate as visitdate, CASE WHEN b.TestItemName = '总补体活性CH50' or b.TestItemName = '补体C3' or b.TestItemName = '补体C4' or b.TestItemName = 'C1抑制剂' or b.TestItemName = '补体C1Q' or b.TestItemName = '补体C1q' THEN 38 ELSE 37 END as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '乙肝e抗原' then '乙肝E抗原' WHEN b.TestItemName = '乙肝e抗体' then '乙肝E抗体' WHEN b.TestItemName = '抗EB病毒衣壳抗原IgG亲合力' then '抗EB病毒衣壳抗原IgG亲和力' WHEN b.TestItemName = '补体C1q' then '补体C1Q' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_OUTPATIENTVISITRECORD c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where ((b.TestItemCode = 'HBeAg') or (b.TestItemCode = '5656' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5656' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5656' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5636' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5636' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5636' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7398' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7398' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6219' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '6219' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7057' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5704' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5704' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5704' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6221' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7109' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7109' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7950' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7889' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7889' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5150' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5150' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7399' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7399' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5655' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5655' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5655' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7891' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7891' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'HBeAb') or (b.TestItemCode = '6228' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6228' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5705' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5705' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '5705' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6229' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6229' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7898' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7898' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7115' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7115' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7017' and a.specimenclasscode = 'LIS1074') or (b.TestItemCode = '7017' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7017' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7017' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7192' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7192' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7149' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5554' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7149' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5554' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7148' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7148' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7118' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5555' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7150' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5555' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7150' and a.specimenclasscode = 'LIS5'))
'''


# --  ANA+ENA+dsDNA组合
sql_18_7 = '''
SELECT c.visittime as visittime, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, null as id_number, c.ID as encounter_id, a.EncounterType as encounter_type, c.patid as patid, c.visitdate as visitdate, 41 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '抗SM' then '抗Sm' WHEN b.TestItemName = '抗SSB/La抗体' then '抗SSB/La' WHEN b.TestItemName = '抗Jo-1抗体' then '抗Jo-1' WHEN b.TestItemName = '抗核小体抗体' then '核小体抗体' WHEN b.TestItemName = '抗ds-DNA(ELISA法)' then '抗ds-DNA(ELISA法）' WHEN b.TestItemName = '抗ds-DNA(短膜虫法)' then '抗ds-DNA（短膜虫法）' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_OUTPATIENTVISITRECORD c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where ((b.TestItemCode = '7449' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7449' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5645' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5650' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5650' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5735' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5735' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6709' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8809' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6709' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5729') or (b.TestItemCode = '5652' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5652' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7081' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5641' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5641' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7080' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6707') or (b.TestItemCode = '6708' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6708' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = 'SM') or (b.TestItemCode = '5642' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5642' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7899' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '7899' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5649' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5649' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7078' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = 'ScL-70') or (b.TestItemCode = '7079' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5653' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5650' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5653' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6400' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '6400' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5651' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5651' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7082' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5652' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '5641' and a.specimenclasscode = 'LIS1075') or (b.TestItemCode = '8593' and a.specimenclasscode = 'LIS1075'))
'''


# -- 免疫细胞分型
sql_18_8 = '''
SELECT c.visittime as visittime, NVL(d.EMPI, d.PatientNo) AS EMPI, c.PatientNo as patient_no, null as id_number, c.ID as encounter_id, a.EncounterType as encounter_type, c.patid as patid, c.visitdate as visitdate, 43 as question_id, b.LabGenericID as lab_generic_id, a.TSTest as ts_test, substr(a.TSTest, 0, 10) as ts_test_var, a.SpecimenClassName, CASE WHEN b.TestItemName = '淋巴细胞绝对值（CD45+）' then '淋巴细胞(CD45+)绝对值' WHEN b.TestItemName = 'T淋巴细胞绝对值' then 'T淋巴细胞(CD3+)绝对值' WHEN b.TestItemName = 'T淋巴细胞（CD3+）' or b.TestItemName = 'T淋巴细胞CD3' then 'T淋巴细胞(CD3+)' WHEN b.TestItemName = 'Ts淋巴细胞绝对值' then 'Ts淋巴细胞(CD3+CD8+)绝对值' WHEN b.TestItemName = 'Th淋巴细胞绝对值' then 'Th淋巴细胞(CD3+CD4+)绝对值' WHEN b.TestItemName = 'Th淋巴细胞（CD3+CD4+）' then 'Th淋巴细胞(CD3+CD4+)' WHEN b.TestItemName = 'B淋巴细胞绝对值' then 'B淋巴细胞(CD3-CD19+)绝对值' WHEN b.TestItemName = 'B淋巴细胞（CD3-CD19+）' then 'B淋巴细胞(CD3-CD19+)' WHEN b.TestItemName = '自然杀伤细胞绝对值' then '自然杀伤细胞(CD3-CD16+CD56+)绝对值' WHEN b.TestItemName = 'CD3-CD20+' then 'CD20细胞比值(CD3-CD20+)' WHEN b.TestItemName = 'CD45/3/14/38/19/27(浆细胞/B细胞比率)' then '浆细胞(CD45/3/14/38/19/27)' else b.TestItemName end as table_item_name, b.TestItemCode as test_item_code, b.TestItemName as test_item_name, b.PrintValue as print_value, b.ResultValue as result_value, b.ResultUnit as result_unit, b.ReferenceText as reference_text, b.AbnormalFlag as abnormal_flag, b.AbnormalFlagName as abnormal_flag_name, '42502657200' as hospital_code, FROM_UNIXTIME(UNIX_TIMESTAMP(),'yyyy-MM-dd HH:mm:ss') as create_date , a.tsdraw as ts_draw, substr(a.tsdraw, 0, 10) as ts_draw_var
FROM cdr_V_LabGenericReport a 
JOIN cdr_V_LabGenericResult b 
ON a.id = b.LabGenericID 
JOIN cdr_V_OUTPATIENTVISITRECORD c 
ON a.PatientNo = c.PatientNo and a.Encounterid = c.ID 
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON c.PatientNo = d.PatientNo 
where ((b.TestItemCode = '6955' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7339' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7339' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '5432' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5432' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6953' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6953' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6181' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6181' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '7337' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '7337' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6959' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6959' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6956' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '6956' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6960') or (b.TestItemCode = '6181' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '8488' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5538' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '5538' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8109' and a.specimenclasscode = 'LIS5') or (b.TestItemCode = '8109' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6958' and a.specimenclasscode = 'LIS6') or (b.TestItemCode = '6958' and a.specimenclasscode = 'LIS5'))
'''

sql_18_ist = '''
insert into form_lab_info_followup_temp(
visittime,
empi,
patient_no,
id_number,
encounter_id,
encounter_type,
patid,
visitdate,
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
ts_draw_var) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
'''

# -- # 19 随访检查

sql_19 = '''
SELECT 
distinct NVL(d.EMPI, d.PatientNo) AS EMPI, 
a.PatientNo as patient_no,
null as id_number, 
a.EncounterID as encounter_id, 
c.patid as patid, 
c.visitdate as visitdate, 
a.EncounterType as encounter_type, 
CASE WHEN a.reportclasscode='Electrocardio' and a.reportname like '%心电图%' THEN 20 WHEN a.reportname like '%心脏%彩超%' THEN 21 WHEN a.reportclasscode in ('Ultrasound', 'US') THEN 22 WHEN reportname='CT报告' and bodysite='胸部' THEN 23 WHEN reportname='CT报告' and bodysite like '%腹部%' THEN 24 ELSE NULL END as question_id, 
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
JOIN (select distinct empi, patientno from dw.empi_cdw where effect_flag = 1 and patientno in (SELECT DISTINCT patientno FROM skzbk.fs_medicalrecordmain_ls_temp)) d 
ON a.PatientNo = d.PatientNo 
where (a.reportclasscode='Electrocardio' and a.reportname like '%心电图%') or a.reportname like '%心脏%彩超%' or  (a.reportclasscode in ('Ultrasound', 'US') and (b.ExamFind like '%肝%' or b.ExamFind like '%胆%' or b.ExamFind like '%胰%' or b.ExamFind like '%脾%' or b.ExamFind like '%肾%' or b.ExamFind like '%甲状腺%')) or (a.reportname='CT报告' and (b.bodysite='胸部' or b.bodysite like '%腹部%'))
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