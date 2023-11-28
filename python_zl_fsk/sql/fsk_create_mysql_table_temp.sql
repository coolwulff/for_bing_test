
-- 2 - qs_drz_patient不脱敏
DROP TABLE if exists qs_drz_patient_temp;
CREATE TABLE IF NOT EXISTS qs_drz_patient_temp(
patient_num VARCHAR(60),
empi VARCHAR(60), 
inpatient_number VARCHAR(60), 
patient_no VARCHAR(60), 
name VARCHAR(60), 
id_card VARCHAR(60), 
sex VARCHAR(60), 
age VARCHAR(60),
hospital_id VARCHAR(60),
hospital_code VARCHAR(60),
group_id VARCHAR(60), 
in_hospital_datetime VARCHAR(60), 
out_hospital_datetime VARCHAR(60), 
in_hospital_dept_code VARCHAR(60), 
in_hospital_dept_name VARCHAR(60), 
out_hospital_dept_name VARCHAR(60), 
ward VARCHAR(60), 
primary_diagnosis_code VARCHAR(60), 
primary_diagnosis VARCHAR(60), 
operate_date VARCHAR(60), 
operate_code VARCHAR(60), 
operate_name VARCHAR(60), 
delete_flag VARCHAR(60),
source_flag VARCHAR(60), 
operate_idx VARCHAR(60), 
create_date VARCHAR(60)
);

-- 3 - form_basic_info不脱敏
-- 旧表
/*
DROP TABLE if exists form_basic_info_temp;
CREATE TABLE IF NOT EXISTS form_basic_info_temp(
patient_no VARCHAR(60),
empi VARCHAR(60), 
encounter_id VARCHAR(60), 
patient_name VARCHAR(60), 
sex VARCHAR(60), 
countryname VARCHAR(60),
nationname VARCHAR(60), 
birth VARCHAR(60), 
in_hospital_time VARCHAR(60), 
out_hospital_time VARCHAR(60), 
id_number VARCHAR(60),
marriage VARCHAR(60),
jobname VARCHAR(60),
birth_sheng VARCHAR(60),
birth_sheng_code VARCHAR(60),
birth_shi VARCHAR(60),
birth_shi_code VARCHAR(60),
birth_qu VARCHAR(60),
birth_qu_code VARCHAR(60),
native_sheng VARCHAR(60),
native_sheng_code VARCHAR(60), 
native_shi VARCHAR(60),
native_shi_code VARCHAR(60),
current_province_code VARCHAR(60),
current_province_name VARCHAR(60),
current_city_code VARCHAR(60), 
current_city_name VARCHAR(60),
current_county_code VARCHAR(60),
current_county_name VARCHAR(60),
current_addr VARCHAR(60),
contact_tel VARCHAR(60),
by_tel VARCHAR(60),
blood_abo VARCHAR(60),
blood_rh VARCHAR(60),
payway VARCHAR(60),
hospital_code VARCHAR(60),
inpatient_number VARCHAR(60),
outpatient_number VARCHAR(60),
contactphone VARCHAR(60),
delete_flag VARCHAR(60),
create_date VARCHAR(60),
num VARCHAR(60)
);
*/

-- 新表
DROP TABLE if exists form_basic_info_temp;
CREATE TABLE IF NOT EXISTS form_basic_info_temp(
patient_no VARCHAR(60),
empi VARCHAR(60), 
encounter_id VARCHAR(60), 
patient_name VARCHAR(60), 
sex VARCHAR(60), 
countryname VARCHAR(60),
nationname VARCHAR(60), 
birth VARCHAR(60), 
in_hospital_time VARCHAR(60), 
out_hospital_time VARCHAR(60), 
id_number VARCHAR(60),
marriage VARCHAR(60),
jobname VARCHAR(60),
jobcode VARCHAR(60),
birth_sheng VARCHAR(60),
birth_sheng_code VARCHAR(60),
birth_shi VARCHAR(60),
birth_shi_code VARCHAR(60),
birth_qu VARCHAR(60),
birth_qu_code VARCHAR(60),
native_sheng VARCHAR(60),
native_sheng_code VARCHAR(60), 
native_shi VARCHAR(60),
native_shi_code VARCHAR(60),
current_province_code VARCHAR(60),
current_province_name VARCHAR(60),
current_city_code VARCHAR(60), 
current_city_name VARCHAR(60),
current_county_code VARCHAR(60),
current_county_name VARCHAR(60),
current_addr VARCHAR(60),
contact_tel VARCHAR(60),
by_tel VARCHAR(60),
blood_abo VARCHAR(60),
blood_rh VARCHAR(60),
payway VARCHAR(60),
hospital_code VARCHAR(60),
inpatient_number VARCHAR(60),
outpatient_number VARCHAR(60),
contactphone VARCHAR(60),
delete_flag VARCHAR(60),
create_date VARCHAR(60),
num VARCHAR(60)
);

--  4 - 住院记录qs_admission_history
DROP TABLE if exists qs_admission_history_temp;
CREATE TABLE IF NOT EXISTS qs_admission_history_temp(
empi VARCHAR(60), 
patient_no VARCHAR(60),
inpatient_number VARCHAR(60),
in_hospital_date VARCHAR(60),
out_hospital_date VARCHAR(60),
create_date VARCHAR(60),
admission_num VARCHAR(60)
);

-- 增加转归：入院情况和出院情况,弃用
DROP TABLE if exists qs_admission_history_temp;
CREATE TABLE IF NOT EXISTS qs_admission_history_temp(
empi VARCHAR(60), 
patient_no VARCHAR(60),
inpatient_number VARCHAR(60),
in_hospital_date VARCHAR(60),
out_hospital_date VARCHAR(60),
create_date VARCHAR(60),
ryqk VARCHAR(60),
cyqk VARCHAR(60),
admission_num VARCHAR(60)
);

-- 4_2 转归情况 form_qs_zg_temp
DROP TABLE if exists form_qs_zg_temp;
CREATE TABLE IF NOT EXISTS form_qs_zg_temp(
empi VARCHAR(60), 
patient_no VARCHAR(60),
encounter_id VARCHAR(60),
patient_name VARCHAR(60),
inhospital_time VARCHAR(60),
outhospital_time VARCHAR(60),
inpatient_number VARCHAR(60), 
outpatient_number VARCHAR(60),
inhospital_condition VARCHAR(60), 
outhospital_result VARCHAR(60),
hospital_code VARCHAR(60),
delete_flag VARCHAR(60),
create_date VARCHAR(60) 
)


-- # 5 - form_diagnose_info 旧版
/*
DROP TABLE if exists form_diagnose_info_temp;
CREATE TABLE IF NOT EXISTS form_diagnose_info_temp(
empi VARCHAR(60), 
patient_no VARCHAR(60),
encounter_id VARCHAR(60),
patient_name VARCHAR(60),
age VARCHAR(60),
inpatient_number VARCHAR(60),
outpatient_number VARCHAR(60),
in_hospital_time VARCHAR(60),
out_hospital_time VARCHAR(60), 
pay_way VARCHAR(60),
die_time VARCHAR(60),
is_die VARCHAR(60),
inhospital_ward_code VARCHAR(60),
inhospital_ward_name VARCHAR(60), 
inhospital_bed_code VARCHAR(60),
inhospital_dept_code VARCHAR(60),
inhospital_dept_name VARCHAR(60),
inhospital_way VARCHAR(60),
outhospital_dept_code VARCHAR(60),
outhospital_dept_name VARCHAR(60),
inhospital_total_cost VARCHAR(60),
inpatient_times VARCHAR(60),
isprimary VARCHAR(60),
diagnose_code VARCHAR(60),
diagnose_name VARCHAR(600),
hospital_code VARCHAR(60),
delete_flag VARCHAR(60),
create_date VARCHAR(60) 
);
*/

-- # 5 - form_diagnose_info
DROP TABLE if exists form_diagnose_info_temp;
CREATE TABLE IF NOT EXISTS form_diagnose_info_temp(
empi VARCHAR(60), 
patient_no VARCHAR(60),
encounter_id VARCHAR(60),
patient_name VARCHAR(60),
age VARCHAR(60),
inpatient_number VARCHAR(60),
outpatient_number VARCHAR(60),
in_hospital_time VARCHAR(60),
out_hospital_time VARCHAR(60), 
pay_way VARCHAR(60),
die_time VARCHAR(60),
inhospital_ward_code VARCHAR(60),
inhospital_ward_name VARCHAR(60), 
inhospital_bed_code VARCHAR(60),
inhospital_dept_code VARCHAR(60),
inhospital_dept_name VARCHAR(60),
inhospital_way VARCHAR(60),
outhospital_dept_code VARCHAR(60),
outhospital_dept_name VARCHAR(60),
inhospital_total_cost VARCHAR(60),
isprimary VARCHAR(60),
diagnose_code VARCHAR(60),
diagnose_name VARCHAR(600),
hospital_code VARCHAR(60),
delete_flag VARCHAR(60),
create_date VARCHAR(60),
is_die VARCHAR(60),
inpatient_times VARCHAR(60)
);

-- # 5 - form_diagnose_info_51_temp 
DROP TABLE if exists form_diagnose_info_51_temp;
CREATE TABLE IF NOT EXISTS form_diagnose_info_51_temp(
empi VARCHAR(60), 
patient_no VARCHAR(60),
encounter_id VARCHAR(60),
patient_name VARCHAR(60),
age VARCHAR(60),
inpatient_number VARCHAR(60),
outpatient_number VARCHAR(60),
in_hospital_time VARCHAR(60),
out_hospital_time VARCHAR(60), 
pay_way VARCHAR(60),
die_time VARCHAR(60),
inhospital_ward_code VARCHAR(60),
inhospital_ward_name VARCHAR(60), 
inhospital_bed_code VARCHAR(60),
inhospital_dept_code VARCHAR(60),
inhospital_dept_name VARCHAR(60),
inhospital_way VARCHAR(60),
outhospital_dept_code VARCHAR(60),
outhospital_dept_name VARCHAR(60),
inhospital_total_cost VARCHAR(60),
isprimary VARCHAR(60),
diagnose_code VARCHAR(60),
diagnose_name VARCHAR(600),
diagnose_type VARCHAR(60),
hospital_code VARCHAR(60),
delete_flag VARCHAR(60),
create_date VARCHAR(60),
is_die VARCHAR(60),
inpatient_times VARCHAR(60)
);

-- # 6 - form_diagnose_detail
DROP TABLE if exists form_diagnose_detail_temp;
CREATE TABLE IF NOT EXISTS form_diagnose_detail_temp(
empi VARCHAR(60), 
patient_no VARCHAR(60),
encounter_id VARCHAR(60),
patient_name VARCHAR(60),
inhospital_time VARCHAR(60),
outhospital_time VARCHAR(60),
inpatient_number VARCHAR(60), 
outpatient_number VARCHAR(60),
diagnose_time VARCHAR(60), 
diagnose_time_var VARCHAR(60),
isprimary VARCHAR(60),
diagnose_code VARCHAR(60),
diagnose_name VARCHAR(600),
hospital_code VARCHAR(60),
delete_flag VARCHAR(60),
create_date VARCHAR(60) 
);

-- # 7 - form_operation_info
DROP TABLE if exists form_operation_info_temp;
CREATE TABLE IF NOT EXISTS form_operation_info_temp(
empi VARCHAR(60), 
patient_no VARCHAR(60),
encounter_id VARCHAR(60), 
inpatient_number VARCHAR(60),
in_hospital_datetime VARCHAR(60),
out_hospital_datetime VARCHAR(60),
operate_date VARCHAR(60),
operate_code VARCHAR(60),
operate_name VARCHAR(60),
operation_dept_name VARCHAR(60),
operate_doctor_name VARCHAR(60),
anesthesia_way_code VARCHAR(60),
anesthesia_way_name VARCHAR(60),
anesthesia_doctor_name VARCHAR(60),
preoperation_diagnose_code VARCHAR(60),
preoperation_diagnose_name VARCHAR(60),
hospital_code VARCHAR(60),
delete_flag VARCHAR(60),
create_date VARCHAR(60) 
);

-- # 8 - form_medication_info
DROP TABLE if exists form_medication_info_temp;
CREATE TABLE IF NOT EXISTS form_medication_info_temp(
empi VARCHAR(60), 
patient_no VARCHAR(60),
encounter_id VARCHAR(60),
inpatient_number VARCHAR(60),
outpatient_number VARCHAR(60),
in_hospital_time VARCHAR(60),
out_hospital_time VARCHAR(60),
master_orders_id VARCHAR(60),
orders_code VARCHAR(60),
orders_name VARCHAR(60),
specifications VARCHAR(60),
dosage VARCHAR(60),
dosage_unit VARCHAR(60),
pathway VARCHAR(60),
frequency VARCHAR(60),
pc VARCHAR(60),
write_recipe_time VARCHAR(60),
project_type_code VARCHAR(60),
project_type_name VARCHAR(60),
orders_start_time VARCHAR(60),
stop_time VARCHAR(60),
solventflag VARCHAR(60),
remark VARCHAR(600),
hospital_code VARCHAR(60),
delete_flag VARCHAR(60),
create_date VARCHAR(60)
);

-- # 9 - form_physical_exam_info
DROP TABLE if exists form_physical_exam_info_temp;
CREATE TABLE IF NOT EXISTS form_physical_exam_info_temp(
empi VARCHAR(60),
patient_no VARCHAR(60),
id_number VARCHAR(60),
encounter_id VARCHAR(60),
inpatient_number VARCHAR(60),
outpatient_number VARCHAR(60),
operate_date VARCHAR(60),
operate_date_var VARCHAR(60),
height VARCHAR(60),
weight VARCHAR(60),
temperature VARCHAR(60),
systolic VARCHAR(60),
diastolic VARCHAR(60),
respiratory_rate VARCHAR(60),
heart_rate VARCHAR(60),
oxygen_saturation VARCHAR(60),
hospital_code VARCHAR(60),
create_date VARCHAR(60) 
);


-- 10 form_ris_info 检查 待确认 
DROP TABLE if exists form_ris_info_temp;
CREATE TABLE IF NOT EXISTS form_ris_info_temp(
empi VARCHAR(60),
patient_no VARCHAR(60),
id_number VARCHAR(60), 
encounter_id VARCHAR(60),
inpatient_number VARCHAR(60),
outpatient_number VARCHAR(60),
encounter_type VARCHAR(60),
question_id VARCHAR(60),
report_id VARCHAR(60),
ts_exam VARCHAR(60),
ts_exam_var VARCHAR(60), 
exam_name VARCHAR(600),
report_name VARCHAR(600),
exam_find text,
exam_conclusion text,
body_site VARCHAR(600),
create_date VARCHAR(600),
report_class_code VARCHAR(600),
report_class_name VARCHAR(600),
summary_note text
);


-- # 11 - form_lab_info
DROP TABLE if exists form_lab_info_temp;
CREATE TABLE IF NOT EXISTS form_lab_info_temp(
in_hospital_date VARCHAR(60),
empi VARCHAR(60),
patient_no VARCHAR(60),
id_number VARCHAR(60),
encounter_id VARCHAR(60),
encounter_type VARCHAR(60),
inpatient_number VARCHAR(60),
outpatient_number VARCHAR(60),
question_id VARCHAR(60),
lab_generic_id VARCHAR(60),
ts_test VARCHAR(60),
ts_test_var VARCHAR(60),
SpecimenClassName VARCHAR(60),
table_item_name VARCHAR(60),
test_item_code VARCHAR(60),
test_item_name VARCHAR(60),
print_value VARCHAR(60),
result_value VARCHAR(60),
result_unit VARCHAR(60),
reference_text text,
abnormal_flag VARCHAR(60),
abnormal_flag_name VARCHAR(60),
hospital_code VARCHAR(60),
create_date VARCHAR(60),
ts_draw VARCHAR(60),
ts_draw_var VARCHAR(60)
);

DROP TABLE if exists form_lab_info_temp_all;
CREATE TABLE IF NOT EXISTS form_lab_info_temp_all(
in_hospital_date VARCHAR(60),
empi VARCHAR(60),
patient_no VARCHAR(60),
id_number VARCHAR(60),
encounter_id VARCHAR(60),
encounter_type VARCHAR(60),
inpatient_number VARCHAR(60),
outpatient_number VARCHAR(60),
question_id VARCHAR(60),
lab_generic_id VARCHAR(60),
Examclasscode VARCHAR(600),
Examclassname VARCHAR(600),
ts_test VARCHAR(60),
ts_test_var VARCHAR(60),
SpecimenClassName VARCHAR(60),
table_item_name VARCHAR(60),
test_item_code VARCHAR(60),
test_item_name VARCHAR(60),
print_value VARCHAR(60),
result_value VARCHAR(60),
result_unit VARCHAR(60),
reference_text text,
abnormal_flag VARCHAR(60),
abnormal_flag_name VARCHAR(60),
hospital_code VARCHAR(60),
create_date VARCHAR(60),
ts_draw VARCHAR(60),
ts_draw_var VARCHAR(60)
);


-- # 12 - cdr_patient_info
DROP TABLE if exists cdr_patient_info_temp;
CREATE TABLE IF NOT EXISTS cdr_patient_info_temp(
empi VARCHAR(60),
patient_no VARCHAR(60), 
patient_name VARCHAR(60),
sex VARCHAR(60),
age VARCHAR(60),
id_number VARCHAR(60),
card_no VARCHAR(60),
inpatient_number VARCHAR(60),
in_hospital_date_time VARCHAR(60),
inpatient_primary_diagnose VARCHAR(600),
operate_date VARCHAR(60),
outpatient_number VARCHAR(60),
visit_date_time VARCHAR(60),
outpatient_primary_diagnose VARCHAR(600),
hospital_code VARCHAR(60),
hospital_name VARCHAR(60)
);

-- 15 form_focus_diagnosis_followup
DROP TABLE if exists form_focus_diagnosis_followup_temp;
CREATE TABLE IF NOT EXISTS form_focus_diagnosis_followup_temp(
empi VARCHAR(60),
patient_no VARCHAR(60), 
patient_name VARCHAR(60),
outpatient_number VARCHAR(60),
visit_time VARCHAR(60),
visit_date VARCHAR(60),
category_name VARCHAR(60), 
primary_diagnosis VARCHAR(60), 
primary_diagnosis_code VARCHAR(60)
);

-- 增加 encounter_id
DROP TABLE if exists form_focus_diagnosis_followup_temp;
CREATE TABLE IF NOT EXISTS form_focus_diagnosis_followup_temp(
empi VARCHAR(60),
patient_no VARCHAR(60), 
encounter_id VARCHAR(60),
patient_name VARCHAR(60),
outpatient_number VARCHAR(60),
registrationdatetime VARCHAR(60),
visitdatetime VARCHAR(60),
category_name VARCHAR(60), 
primary_diagnosis VARCHAR(60), 
primary_diagnosis_code VARCHAR(60)
);

-- 16 form_physical_exam_info_followup_temp

DROP TABLE if exists form_physical_exam_info_followup_temp;
CREATE TABLE IF NOT EXISTS form_physical_exam_info_followup_temp(
empi VARCHAR(60),
patient_no VARCHAR(60),
outpatient_number VARCHAR(60),
operate_date VARCHAR(60),
operate_date_var VARCHAR(60),
height VARCHAR(60),
weight VARCHAR(60), 
temperature VARCHAR(60),
systolic VARCHAR(60),
diastolic VARCHAR(60),
respiratory_rate VARCHAR(60), 
heart_rate VARCHAR(60), 
oxygen_saturation VARCHAR(60), 
hospital_code VARCHAR(60),
create_date VARCHAR(60)
);

-- 增加 encounter_id
DROP TABLE if exists form_physical_exam_info_followup_temp;
CREATE TABLE IF NOT EXISTS form_physical_exam_info_followup_temp(
empi VARCHAR(60),
patient_no VARCHAR(60),
outpatient_number VARCHAR(60),
encounter_id VARCHAR(60),
operate_date VARCHAR(60),
operate_date_var VARCHAR(60),
height VARCHAR(60),
weight VARCHAR(60), 
temperature VARCHAR(60),
systolic VARCHAR(60),
diastolic VARCHAR(60),
respiratory_rate VARCHAR(60), 
heart_rate VARCHAR(60), 
oxygen_saturation VARCHAR(60), 
hospital_code VARCHAR(60),
create_date VARCHAR(60)
);

-- 17 form_medication_info_followup_temp

DROP TABLE if exists form_medication_info_followup_temp;
CREATE TABLE IF NOT EXISTS form_medication_info_followup_temp(
empi VARCHAR(60),
patient_no VARCHAR(60),
outpatient_number VARCHAR(60),
writerecipetime_date VARCHAR(60), 
writerecipedatetime_date VARCHAR(60),
primary_diagnosis VARCHAR(60),
primary_diagnosis_code VARCHAR(60),
outpatientrecipeid VARCHAR(60),
projecttypename VARCHAR(60),
projecttypecode VARCHAR(60),
projectid VARCHAR(60),
projectcode VARCHAR(60),
projectname VARCHAR(60),
specifications VARCHAR(600),
projectnumber VARCHAR(60),
dosage VARCHAR(60),
dosageunit VARCHAR(60),
frequency VARCHAR(60),
pathway VARCHAR(60),
days VARCHAR(60),
orders VARCHAR(60),
recipeno VARCHAR(60),
hospital_code VARCHAR(60), 
create_date VARCHAR(60)
)

-- 增加 encounter_id
DROP TABLE if exists form_medication_info_followup_temp;
CREATE TABLE IF NOT EXISTS form_medication_info_followup_temp(
empi VARCHAR(60),
patient_no VARCHAR(60),
outpatient_number VARCHAR(60),
encounter_id VARCHAR(60),
writerecipetime_date VARCHAR(60), 
writerecipedatetime_date VARCHAR(60),
primary_diagnosis VARCHAR(60),
primary_diagnosis_code VARCHAR(60),
outpatientrecipeid VARCHAR(60),
projecttypename VARCHAR(60),
projecttypecode VARCHAR(60),
projectid VARCHAR(60),
projectcode VARCHAR(60),
projectname VARCHAR(60),
specifications VARCHAR(600),
projectnumber VARCHAR(60),
dosage VARCHAR(60),
dosageunit VARCHAR(60),
frequency VARCHAR(60),
pathway VARCHAR(60),
days VARCHAR(60),
orders VARCHAR(60),
recipeno VARCHAR(60),
hospital_code VARCHAR(60), 
create_date VARCHAR(60)
)

-- 18 form_lab_info_followup_temp

DROP TABLE if exists form_lab_info_followup_temp;
CREATE TABLE IF NOT EXISTS form_lab_info_followup_temp(
empi VARCHAR(60),
patient_no VARCHAR(60),
id_number VARCHAR(60),
encounter_id VARCHAR(60),
encounter_type VARCHAR(60),
patid VARCHAR(60),
visitdate VARCHAR(60),
visittime VARCHAR(60),
question_id VARCHAR(60),
lab_generic_id VARCHAR(60),
ts_test VARCHAR(60),
ts_test_var VARCHAR(60),
SpecimenClassName VARCHAR(60),
table_item_name VARCHAR(60),
test_item_code VARCHAR(60),
test_item_name VARCHAR(60),
print_value VARCHAR(60),
result_value VARCHAR(60),
result_unit VARCHAR(60),
reference_text text,
abnormal_flag VARCHAR(60),
abnormal_flag_name VARCHAR(60),
hospital_code VARCHAR(60),
create_date VARCHAR(60),
ts_draw VARCHAR(60),
ts_draw_var VARCHAR(60)
);

-- 19 form_ris_info_ followup 
DROP TABLE if exists form_ris_info_followup_temp;
CREATE TABLE IF NOT EXISTS form_ris_info_followup_temp(
empi VARCHAR(60),
patient_no VARCHAR(60),
id_number VARCHAR(60), 
encounter_id VARCHAR(60),
patid VARCHAR(60),
visitdate VARCHAR(60),
encounter_type VARCHAR(60),
question_id VARCHAR(60),
report_id VARCHAR(60),
ts_exam VARCHAR(60),
ts_exam_var VARCHAR(60), 
exam_name VARCHAR(600),
report_name VARCHAR(600),
exam_find text,
exam_conclusion text,
body_site VARCHAR(600),
create_date VARCHAR(600),
report_class_code VARCHAR(600),
report_class_name VARCHAR(600),
summary_note text
);

----------------------------------------------------------------
-- form_sql_temp_1
DROP TABLE if exists form_sql_temp_1;
CREATE TABLE IF NOT EXISTS form_sql_temp_1(
patientno VARCHAR(600),
inpatientnumber VARCHAR(600),
encounterid VARCHAR(600),
inhospitaltime VARCHAR(600),
outhospitaltime VARCHAR(600),
patientname VARCHAR(600),
age VARCHAR(600),
sex VARCHAR(600),
encountertype VARCHAR(600),
specimenclassname VARCHAR(600),
reportname VARCHAR(600),
tstest VARCHAR(600),
tsdraw VARCHAR(600),
deleteflag VARCHAR(600),
reportstatus VARCHAR(600),
tsdelete VARCHAR(600),
id VARCHAR(600),
labgenericid VARCHAR(600),
testitemcode VARCHAR(600),
testitemname VARCHAR(600),
printvalue VARCHAR(600),
resultvalue VARCHAR(600),
resultunit VARCHAR(600),
referencetext VARCHAR(600),
abnormalflag VARCHAR(600),
abnormalflagname VARCHAR(600)
);

