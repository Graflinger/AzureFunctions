import logging
import io
import azure.functions as func
import pandas as pd 
import openpyxl
from openpyxl import load_workbook


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    #getting file from request body
    body = req.get_body()
    
    #open new file for saving binary data into file
    with open("test.xlsx",'wb') as input_file: ## Open temporary file as bytes
         input_file.write(body)      
    
    #read file into pandas dataframe
    df = pd.read_excel("test.xlsx")
    
    ################
    #Do 
    #some
    #logic
    ################
   
    #writing file back to a binary array 
    with open("test.xlsx", "rb") as binary_file:
        #Read the whole file at once
        data = binary_file.read()
    
    #returning binary data back to caller 
    return func.HttpResponse(data)