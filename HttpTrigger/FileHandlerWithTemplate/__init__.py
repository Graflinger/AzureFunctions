import logging
import io
import os
import azure.functions as func
import pandas as pd 
import openpyxl
from openpyxl import load_workbook


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        body = req.get_body()
        
        #reading input bytes into a temp file
        with open("input.csv",'wb') as input_file: ## Open temporary file as bytes
            input_file.write(body)    

        #readinf file into df
        df = pd.read_csv("input.csv", encoding='ISO-8859-1', skiprows = 3, sep= ";")

        #start processing of the file
        df =df["ID"].dropna()

        einsatz_id_list = list(set(list(df)))
        einsatz_id_list.sort()

        try:
            for id in einsatz_id_list:
                if "BAG" not in id:
                    einsatz_id_list.remove(id)
                elif " " == id:
                    einsatz_id_list.remove(id)
        except:
            logging.error("Wrong file")

        

        #fill template
        
        #get the template file from the same folder where the function is saved
        book = load_workbook(filename = os.path.join("//home/site/wwwroot/HttpTrigger", "template_example.xlsx"))
        
        
        sheet = book.get_sheet_by_name("Tabelle1")
        list_used_columns = ["A"]    
        start_row_tepmpalte = 2
        for i in range(0, len(einsatz_id_list)) :
            sheet["A"+str(i + start_row_tepmpalte)] = einsatz_id_list[i]
        book.save("template_example_tmp.xlsx") 
        with open("template_example.xlsx", "rb") as binary_file:
            data = binary_file.read()

        return func.HttpResponse(data)
    except:
        return "FileError"

    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')
    
    # if name:
    #     return func.HttpResponse(f"Hello {name}!")
    # else:
    #     return func.HttpResponse(
    #          "Please pass a name on the query string or in the request body",
    #          status_code=400
    #     )


#curl --request POST --data-binary "@/mnt/c/Users/S49500/Desktop/temp_Statistik/Final/export.xlsx" http://localhost:7071/api/HttpTrigger?name=test