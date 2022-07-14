import glob
from locale import currency                         # this module helps in selecting files 
import pandas as pd                 # this module helps in processing CSV files
import xml.etree.ElementTree as ET  # this module helps in processing XML files.
from datetime import datetime
import ETL_functions as ETL
import os

dir_path=os. getcwd()
target_path=dir_path+'/example_3/'


logfile=target_path+"logfile.txt"            # all event logs will be stored in this file
targetfile = target_path+"bank_market_cap_gbp.csv"   # file where transformed data is stored




ETL.log("ETL Job Started",logfile)
ETL.log("Extract phase Started",logfile)
extracted_data = ETL.extract_banks(target_path)
ETL.log("Extract phase Ended",logfile)
ETL.log("Transform phase Started",logfile)
transformed_data = ETL.transform_currency(extracted_data)
ETL.log("Transform phase Ended",logfile)
ETL.log("Load phase Started",logfile)
ETL.load_bank(targetfile,transformed_data)
ETL.log("Load phase Ended",logfile)
ETL.log("ETL Job Ended",logfile)

