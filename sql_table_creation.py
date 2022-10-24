import dbm
import pandas as pd 
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

##### loading in the credentials from the .env file ##### 

load_dotenv('credentials.env')

GCP_MYSQL_HOSTNAME = os.getenv('GCP_MYSQL_HOSTNAME')
GCP_MYSQL_USER = os.getenv('GCP_MYSQL_USER')
GCP_MYSQL_PASSWORD = os.getenv('GCP_MYSQL_PASSWORD')
GCP_MYSQL_DATABASE = os.getenv('GCP_MYSQL_DATABASE')

##### connecting to the database #####

connection_string = f'mysql+pymysql://{GCP_MYSQL_USER}:{GCP_MYSQL_PASSWORD}@{GCP_MYSQL_HOSTNAME}/{GCP_MYSQL_DATABASE}'
db = create_engine(connection_string)

tables_names = db.table_names()
print(tables_names) ## confirming connection worked in addition to printing the current tables within the connected database 

##### creating the necessary tables within this database #####

patients = """
create table if not exists patients (
    id int auto_increment,
    mrn varchar(255),
    first_name varchar(255) NOT NULL,
    last_name varchar(255) NOT NULL,
    zip_code varchar(255) NOT NULL,
    dob varchar(255),
    gender varchar(255),
    contact_mobile varchar(255) NOT NULL,
    contact_email varchar(225) NOT NULL,
    PRIMARY KEY (id) 
); 
"""

medications = """
create table if not exists medications (
    id int auto_increment,
    med_ndc varchar(255) default null unique,
    med_human_name varchar(255) default null,
    med_is_dangerous varchar(255) default null,
    PRIMARY KEY (id)
); 
"""

treatments_procedures = """
create table if not exist treatments_procedure (
    id int auto_increment,
    treatment_cpt_code varchar(225) default null unique, 
    cpt_code_description varchar(225) default null unique,
    PRIMARY KEY (id)
);
"""

conditions = """
create table if not exist conditions (
    id int auto_increment,
    icd10_code varchar(255) default null unique,
    icd10_description varchar(255) default null,
    PRIMARY KEY (id) 
);
"""

social_determinant = """
create table if not exist social_determinant (
    id int auto_increment, 
    social_determinant_loinc_code varchar(225) default null unique, 
    loinc_code_desciprtion varchar(225) defualt null, 
    PRIMARY KEY (id)
);
"""

patient_current_info = """
create table if not exist patient_current_info (
    id int auto_increment, 
    mrn varchar(225) default null, 
    icd10_code varchar (225) default null,
    loinc_code varchar (225) defualt null, 
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES patients(mrn) ON DELETE CASCADE, 
    FOREIGN KEY (icd10_code) REFERENCES conditions(icd10_code) ON DELETE CASCADE, 
    FOREIGN KEY (loinc_code) REFERENCES social_determinant(social_determinant_loinc_code) ON DELETE CASCADE
);
"""

patient_medications = """
create table if not exist patient_medications (
    id int auto_increment, 
    mrn varchar(225) default null, 
    ndc_code varchar(225) default null, 
    PRIMARY KEY (id),
    FOREIGN KEY (mrn) REFERENCES patients(mrn) ON DELETE CASCADE, 
    FOREIGN KEY (ndc_code) REFERENCES patients_medications(med_ndc) ON DELETE CASCADE
);
"""

patient_treatment = """
create table if not exist patient_treatment (
    id int auto_increment,
    mrn varchar(225) default null, 
    cpt_code varchar(225) default null, 
    PRIMARY KEY (id), 
    FOREIGN KEY (mrn) REFERENCES patients(mrn) ON DELETE CASCADE, 
    FOREIGN KEY (cpt_code) REFERENCEs treatment_procedure(treatment_cpt_code) ON DELETE CASCADE
"""

##### executing the functions that contains the code to create the tables #####

db.execute(patients)
db.execute(medications)
db.execute(treatments_procedures)
db.execute(conditions)
db.execute(social_determinant)
db.execute(patient_current_info)
db.execute(patient_medications)
db.execute(patient_treatment)