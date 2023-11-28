
/*
清空历史数据脚本
*/

-- 清理未入组的患者
delete from qs_drz_patient where delete_flag = 0 and hospital_code = '42502657200'

delete from form_basic_info where empi not in (select distinct empi from qs_drz_patient)


-- 更新已入组的信息
update qs_drz_patient a, qs_drz_patient_temp b
set 
a.inpatient_number = b.inpatient_number,
a.sex = b.sex,
a.age = b.age,
a.in_hospital_datetime = b.in_hospital_datetime,
a.out_hospital_datetime = b.out_hospital_datetime,
a.ward = b.ward,
a.in_hospital_dept_code = b.in_hospital_dept_code,
a.in_hospital_dept_name = b.in_hospital_dept_name,
a.primary_diagnosis_code = b.primary_diagnosis_code,
a.primary_diagnosis = b.primary_diagnosis
where a.empi = b.empi and a.patient_no = b.patient_no and a.hospital_code = '42502657200'