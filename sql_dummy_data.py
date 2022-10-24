import dbm
import pandas as pd 
import sqlalchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from faker import Faker # https://faker.readthedocs.io/en/master/
import uuid
import random

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

##### creating fake data ##### 

fake = Faker()

## creating a dictionary within a list of fake patient information 

fake_patients = [
    {
        'mrn': str(uuid.uuid4())[:5],  #keep just the first 5 characters of the uuid
        'first_name':fake.first_name(), 
        'last_name':fake.last_name(),
        'zip_code':fake.zipcode(),
        'dob':(fake.date_between(start_date='-90y', end_date='-20y')).strftime("%Y-%m-%d"),
        'gender': fake.random_element(elements=('M', 'F')),
        'contact_mobile':fake.phone_number(),
        'contact_email':fake.email()
    } for x in range(20)
]

df_fake_patients = pd.DataFrame(fake_patients) ## turn the list into a dataframe
df_fake_patients = df_fake_patients.drop_duplicates(subset=['mrn']) 

##### loading in some real data ##### 

ndc_codes = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/FDA_NDC_CODES/main/NDC_2022_product.csv')
list(ndc_codes.columns)
ndc_codes_1k = ndc_codes.sample(n=1000, random_state=1)
# drop duplicates from ndc_codes_1k
ndc_codes_1k = ndc_codes_1k.drop_duplicates(subset=['PRODUCTNDC'], keep='first')

cpt_codes = pd.read_csv('https://gist.githubusercontent.com/lieldulev/439793dc3c5a6613b661c33d71fdd185/raw/25c3abcc5c24e640a0a5da1ee04198a824bf58fa/cpt4.csv')
list(cpt_codes.columns)
cpt_codes.rename(columns={'com.medigy.persist.reference.type.clincial.CPT.code':'CPT code'}, inplace=True) ## renaming the column name
cpt_codes_1k = cpt_codes.sample(n=1000, random_state=1)
cpt_codes_1k = cpt_codes_1k.drop_duplicates(subset=['CPT code'], keep='first')

icd10_code = pd.read_csv('https://raw.githubusercontent.com/Bobrovskiy/ICD-10-CSV/master/2020/diagnosis.csv')
list(icd10_code.columns)
icd10_code_short = icd10_code[['CodeWithSeparator', 'ShortDescription']]
icd10_code_short_1k = icd10_code_short.sample(n=1000, random_state=1)
icd10_code_short_1k = icd10_code_short_1k.drop_duplicates(subset=['CodeWithSeparator'], keep='first')

loinc_code = pd.read_csv('LOINC CODE.csv')
list(loinc_code.columns)
loinc_code.drop_duplicates(subset=['LOINC Code'], keep='first')

#####  #####