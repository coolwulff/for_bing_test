/*
 Navicat Premium Data Transfer

 Source Server         : 10.1.192.113
 Source Server Type    : MySQL
 Source Server Version : 50712
 Source Host           : 10.1.192.113:3306
 Source Schema         : kidney_tumor_dev

 Target Server Type    : MySQL
 Target Server Version : 50712
 File Encoding         : 65001

 Date: 10/01/2022 11:10:53
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cdr_patient_info
-- ----------------------------
DROP TABLE IF EXISTS `cdr_patient_info`;
CREATE TABLE `cdr_patient_info`  (
  `id` int(8) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `empi` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT 'EMPI',
  `patient_no` int(20) NOT NULL COMMENT '患者ID',
  `patient_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '患者姓名',
  `sex` char(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '性别',
  `age` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '年龄',
  `id_number` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '身份证',
  `card_no` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '卡号',
  `inpatient_number` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '住院号',
  `in_hospital_date_time` datetime(0) NULL DEFAULT NULL COMMENT '住院就诊日期',
  `inpatient_primary_diagnose` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '住院主要诊断',
  `operate_date` datetime(0) NULL DEFAULT NULL COMMENT '手术日期',
  `outpatient_number` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '门诊号',
  `visit_date_time` datetime(0) NULL DEFAULT NULL COMMENT '门诊就诊日期',
  `outpatient_primary_diagnose` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '门诊主要诊断',
  `hospital_code` varchar(36) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '所属医院编码',
  `hospital_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '所属医院名称',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `id_index`(`empi`) USING BTREE,
  INDEX `idxs_hospital`(`hospital_code`, `card_no`) USING BTREE,
  INDEX `idx_idcard`(`hospital_code`, `id_number`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;


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

DROP TABLE if exists form_focus_diagnosis_followup;
CREATE TABLE IF NOT EXISTS form_focus_diagnosis_followup(
id INT(8) NOT NULL AUTO_INCREMENT COMMENT '关系ID',
empi VARCHAR(36) NOT NULL COMMENT 'EMPI',
patient_no INT(20) NOT NULL COMMENT '患者ID',
patient_name VARCHAR(36) COMMENT '姓名', 
outpatient_number VARCHAR(36) COMMENT '门诊号',
visit_date VARCHAR(36) COMMENT '就诊日期',
diagnose_time VARCHAR(36) COMMENT '诊断时间', 
category_name VARCHAR(36) COMMENT '门诊类别名称：初诊，复诊', 
primary_diagnosis VARCHAR(36) COMMENT '主要诊断名称',
primary_diagnosis_code VARCHAR(36) COMMENT '主要诊断名称编码',
create_date datetime(0) COMMENT '创建时间',
update_date datetime(0) COMMENT '更新时间',
last_update_date datetime(0) COMMENT '最后一次回填时间',
hospital_code VARCHAR(36) COMMENT '医疗机构代码',
delete_flag INT(20) COMMENT '删除标识',
PRIMARY KEY (id)
);
CREATE INDEX id_index ON form_focus_diagnosis_followup (empi) USING BTREE;

-- 修改时间，并增加 encounter_id
DROP TABLE if exists form_focus_diagnosis_followup;
CREATE TABLE IF NOT EXISTS form_focus_diagnosis_followup(
id INT(8) NOT NULL AUTO_INCREMENT COMMENT '关系ID',
empi VARCHAR(36) NOT NULL COMMENT 'EMPI',
patient_no INT(20) NOT NULL COMMENT '患者ID',
patient_name VARCHAR(36) COMMENT '姓名', 
outpatient_number VARCHAR(36) COMMENT '门诊号',
encounter_id VARCHAR(36) COMMENT '就诊ID',
registration_datetime VARCHAR(36) COMMENT '挂号时间日期',
visit_datetime VARCHAR(36) COMMENT '就诊时间日期', 
category_name VARCHAR(36) COMMENT '门诊类别名称：初诊，复诊', 
primary_diagnosis VARCHAR(36) COMMENT '主要诊断名称',
primary_diagnosis_code VARCHAR(36) COMMENT '主要诊断名称编码',
create_date datetime(0) COMMENT '创建时间',
update_date datetime(0) COMMENT '更新时间',
last_update_date datetime(0) COMMENT '最后一次回填时间',
hospital_code VARCHAR(36) COMMENT '医疗机构代码',
delete_flag INT(20) COMMENT '删除标识',
PRIMARY KEY (id)
);
CREATE INDEX id_index ON form_focus_diagnosis_followup (empi) USING BTREE;


DROP TABLE if exists form_outcome;
CREATE TABLE IF NOT EXISTS form_outcome(
id INT(8) NOT NULL AUTO_INCREMENT COMMENT '关系ID',
empi VARCHAR(36) NOT NULL COMMENT 'EMPI',
patient_no INT(20) NOT NULL COMMENT '患者ID',
patient_name VARCHAR(36) COMMENT '姓名', 
inpatient_number VARCHAR(36) COMMENT '门诊号',
outpatient_number VARCHAR(36) COMMENT '门诊号',
inhospital_time VARCHAR(36) COMMENT '入院时间', 
outhospital_time VARCHAR(36) COMMENT '出院时间', 
outhospital_result VARCHAR(36) COMMENT '转归情况:1.治愈， 2.好转， 3.未愈， 4.死亡， 5.其他',
create_date datetime(0) COMMENT '创建时间',
update_date datetime(0) COMMENT '更新时间',
last_update_date datetime(0) COMMENT '最后一次回填时间',
hospital_code VARCHAR(36) COMMENT '医疗机构代码',
delete_flag INT(20) COMMENT '删除标识',
PRIMARY KEY (id)
);
CREATE INDEX id_index ON form_outcome (empi) USING BTREE;


-- 表4 主诉及现病史 1. 主诉描述：34-入院记录_主诉 2. 主诉症状：34-入院记录_现病史
DROP TABLE if exists form_complaint_inhos;
CREATE TABLE IF NOT EXISTS form_complaint_inhos(
id INT(8) NOT NULL AUTO_INCREMENT COMMENT '关系ID',
empi VARCHAR(36) COMMENT 'EMPI',
patient_no INT(20) COMMENT '患者ID',
patient_name VARCHAR(36) COMMENT '姓名', 
id_number varchar(36) COMMENT '身份证',
inpatient_number VARCHAR(36) COMMENT '住院号',
ward VARCHAR(36) COMMENT '病区', 
dept_name VARCHAR(36) COMMENT '科室', 
inhospital_time VARCHAR(36) COMMENT '入院时间', 
complaint VARCHAR(8000) COMMENT '主诉',
present_ill_history VARCHAR(8000) COMMENT '现病史',
create_date datetime(0) COMMENT '创建时间',
update_date datetime(0) COMMENT '更新时间',
last_update_date datetime(0) COMMENT '最后一次回填时间',
hospital_code VARCHAR(36) COMMENT '医疗机构代码',
delete_flag INT(20) COMMENT '删除标识',
PRIMARY KEY (id)
);



-- 表41 随访主诉及现病史 1. 主诉描述：02-门诊病历_主诉 2. 主诉症状：02-门诊病历_现病史
DROP TABLE if exists form_complaint_outcome;
CREATE TABLE IF NOT EXISTS form_complaint_outcome(
id INT(8) NOT NULL AUTO_INCREMENT COMMENT '关系ID',
empi VARCHAR(36) COMMENT 'EMPI',
patient_no INT(20) COMMENT '患者ID',
patient_name VARCHAR(36) COMMENT '姓名', 
id_number varchar(36) COMMENT '身份证',
outpatient_number VARCHAR(36) COMMENT '门诊号',
ward VARCHAR(36) COMMENT '病区', 
dept_name VARCHAR(36) COMMENT '科室', 
visit_time VARCHAR(36) COMMENT '就诊时间', 
is_first_visit VARCHAR(36) COMMENT '初诊标识', 
complaint VARCHAR(8000) COMMENT '主诉',
present_ill_history VARCHAR(8000) COMMENT '现病史',
create_date datetime(0) COMMENT '创建时间',
update_date datetime(0) COMMENT '更新时间',
last_update_date datetime(0) COMMENT '最后一次回填时间',
hospital_code VARCHAR(36) COMMENT '医疗机构代码',
delete_flag INT(20) COMMENT '删除标识',
PRIMARY KEY (id)
);


-- temp 表

-- form_complaint_inhos_temp
DROP TABLE if exists form_complaint_inhos_temp;
CREATE TABLE IF NOT EXISTS form_complaint_inhos_temp(
empi VARCHAR(36) COMMENT 'EMPI',
patient_no INT(20) COMMENT '患者ID',
patient_name VARCHAR(36) COMMENT '姓名', 
id_number varchar(36) COMMENT '身份证',
inpatient_number VARCHAR(36) COMMENT '住院号',
ward VARCHAR(36) COMMENT '病区', 
dept_name VARCHAR(36) COMMENT '科室', 
inhospital_time VARCHAR(36) COMMENT '入院时间', 
complaint VARCHAR(8000) COMMENT '主诉',
present_ill_history VARCHAR(8000) COMMENT '现病史',
create_date datetime(0) COMMENT '创建时间',
update_date datetime(0) COMMENT '更新时间',
last_update_date datetime(0) COMMENT '最后一次回填时间',
hospital_code VARCHAR(36) COMMENT '医疗机构代码',
delete_flag INT(20) COMMENT '删除标识',
PRIMARY KEY (id)
);


-- form_complaint_outcome_temp
DROP TABLE if exists form_complaint_outcome_temp;
CREATE TABLE IF NOT EXISTS form_complaint_outcome_temp(
empi VARCHAR(36) COMMENT 'EMPI',
patient_no INT(20) COMMENT '患者ID',
patient_name VARCHAR(36) COMMENT '姓名', 
id_number varchar(36) COMMENT '身份证',
outpatient_number VARCHAR(36) COMMENT '门诊号',
ward VARCHAR(36) COMMENT '病区', 
dept_name VARCHAR(36) COMMENT '科室', 
visit_time VARCHAR(36) COMMENT '就诊时间', 
is_first_visit VARCHAR(36) COMMENT '初诊标识', 
complaint VARCHAR(8000) COMMENT '主诉',
present_ill_history VARCHAR(8000) COMMENT '现病史',
create_date datetime(0) COMMENT '创建时间',
update_date datetime(0) COMMENT '更新时间',
last_update_date datetime(0) COMMENT '最后一次回填时间',
hospital_code VARCHAR(36) COMMENT '医疗机构代码',
delete_flag INT(20) COMMENT '删除标识',
PRIMARY KEY (id)
);
