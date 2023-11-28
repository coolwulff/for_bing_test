
-- 1.5肝脏描述、1.9脾脏长径 、1.10脾脏厚径 

-- form_ris_info

ALTER TABLE form_ris_info Add gzms VARCHAR(20) comment '1.5肝脏描述';
ALTER TABLE form_ris_info Add gzcj VARCHAR(20) comment '1.9脾脏长径';
ALTER TABLE form_ris_info Add gzhj VARCHAR(20) comment '1.10脾脏厚径';

-- 
ALTER TABLE form_focus_diagnosis_followup Add inpatient_number VARCHAR(36) comment '住院号';
