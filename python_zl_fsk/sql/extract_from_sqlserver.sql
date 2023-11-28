/*
入院记录表:
cdr_tb_ryjl
cdr_tb_ryjl_fzjc
cdr_tb_ryjl_gms
cdr_tb_ryjl_hys
cdr_tb_ryjl_jzs
cdr_tb_ryjl_sss

一般手术记录表:
cdr_tb_ybssjl
cdr_tb_ybssjl_ss
cdr_tb_ybssjl_yy
*/


-- 表4 主诉及现病史 1. 主诉描述：34-入院记录_主诉 2. 主诉症状：34-入院记录_现病史
-- form_complaint_inhos

select 
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

-- 表41 随访主诉及现病史 1. 主诉描述：02-门诊病历_主诉 2. 主诉症状：02-门诊病历_现病史
-- form_complaint_outcome;

select 
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
