import glob                         # this module helps in selecting files 
import pandas as pd                 # this module helps in processing CSV files
import xml.etree.ElementTree as ET  # this module helps in processing XML files.
from datetime import datetime
import os

dir_path=os. getcwd()
target_path=dir_path+'/example_3/'

### Extract
def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe

def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process,lines=True)
    return dataframe

def extract_from_json_bank(file_to_process):
    dataframe = pd.read_json(file_to_process)
    return dataframe

def extract_from_xml_person(file_to_process):
    dataframe = pd.DataFrame(columns=["name", "height", "weight"])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)
        dataframe = dataframe.append({"name":name, "height":height, "weight":weight}, ignore_index=True)
    return dataframe


def extract_from_xml_cars(file_to_process):
    dataframe = pd.DataFrame(columns=['car_model','year_of_manufacture','price','fuel'])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        car_model = person.find("car_model").text
        year_of_manufacture = int(person.find("year_of_manufacture").text)
        price = float(person.find("price").text)
        fuel=person.find("fuel").text
        dataframe = dataframe.append({"car_model":car_model, "year_of_manufacture":year_of_manufacture, "price":price, "fuel":fuel}, ignore_index=True)
    return dataframe

def extract_person(path_source):
    extracted_data = pd.DataFrame(columns=['name','height','weight']) # create an empty data frame to hold extracted data
    
    #process all csv files
    for csvfile in glob.glob(path_source+"*.csv"):
        extracted_data = extracted_data.append(extract_from_csv(csvfile), ignore_index=True)
        
    #process all json files
    for jsonfile in glob.glob(path_source+"*.json"):
        extracted_data = extracted_data.append(extract_from_json(jsonfile), ignore_index=True)
    
    #process all xml files
    for xmlfile in glob.glob(path_source+"*.xml"):
        extracted_data = extracted_data.append(extract_from_xml_person(xmlfile), ignore_index=True)
        
    return extracted_data

def extract_cars(path_source):
    extracted_data = pd.DataFrame(columns=['car_model','year_of_manufacture','price', 'fuel']) # create an empty data frame to hold extracted data
    
    #process all csv files
    for csvfile in glob.glob(path_source+"*.csv"):
        extracted_data = extracted_data.append(extract_from_csv(csvfile), ignore_index=True)
        
    #process all json files
    for jsonfile in glob.glob(path_source+"*.json"):
        extracted_data = extracted_data.append(extract_from_json(jsonfile), ignore_index=True)
    
    #process all xml files
    for xmlfile in glob.glob(path_source+"*.xml"):
        extracted_data = extracted_data.append(extract_from_xml_cars(xmlfile), ignore_index=True)
        
    return extracted_data

def extract_banks(path_source):
    extracted_data = pd.DataFrame(columns=['Name','Market Cap (US$ Billion)']) # create an empty data frame to hold extracted data
        
    #process all json files
    for jsonfile in glob.glob(path_source+"*.json"):
        extracted_data = extracted_data.append(extract_from_json_bank(jsonfile), ignore_index=True)
    
    return extracted_data


#Transform
def transform_round(data):
        #Convert height which is in inches to millimeter
        #Convert the datatype of the column into float
        #data.height = data.height.astype(float)
        #Convert inches to meters and round off to two decimals(one inch is 0.0254 meters)
        data['price'] = round(data.price,2)
        return data


def transform_units(data):
        #Convert height which is in inches to millimeter
        #Convert the datatype of the column into float
        #data.height = data.height.astype(float)
        #Convert inches to meters and round off to two decimals(one inch is 0.0254 meters)
        data['height'] = round(data.height * 0.0254,2)
        
        #Convert weight which is in pounds to kilograms
        #Convert the datatype of the column into float
        #data.weight = data.weight.astype(float)
        #Convert pounds to kilograms and round off to two decimals(one pound is 0.45359237 kilograms)
        data['weight'] = round(data.weight * 0.45359237,2)
        return data

def transform_currency(data):
        #Convert height which is in inches to millimeter
        #Convert the datatype of the column into float
        #data.height = data.height.astype(float)
        #Convert inches to meters and round off to two decimals(one inch is 0.0254 meters)
        # data['Market Cap (US$ Billion)'] = data[1] * exchange_rate
        df=extract_from_csv(target_path+'exchange_rates.csv')
        df.columns=['Currency','Rates']
        exchange_rate=df[df['Currency']=='GBP'].iloc[0][1]
        data['Market Cap (US$ Billion)'] = round(data['Market Cap (US$ Billion)'].apply(lambda x: x*exchange_rate),3)
        data.rename(columns = {'Market Cap (US$ Billion)':'Market Cap (GBP$ Billion)'}, inplace = True)
        
        return data

#Load
def load(targetfile,data_to_load):
    data_to_load.to_csv(targetfile)  

#Load
def load_bank(targetfile,data_to_load):
    data_to_load.to_csv(targetfile, index=False)  


#log file
def log(message,logfile):
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open(logfile,"a") as f:
        f.write(timestamp + ',' + message + '\n')