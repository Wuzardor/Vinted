import os
import json
import logging
import glob

###  CONSTANTE(S)  ###
LOGGER = logging.getLogger()

## Block Auth to Google Sheet ##
# Source: https://www.analyticsvidhya.com/blog/2020/07/read-and-update-google-spreadsheets-with-python/
# importing the required libraries
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
# file containing credential generate with google API (cf. source link above)
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Mypath/myfile.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('MySpreadSheetName')

## End of the block Auth ##

# To implement in a V2
# dirname : retrieve the path of the directory
# abspath : retrieve the abolut path of th file
# __file__ : variable which allow the path of the current script
# CUR_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(CUR_DIR, "data")

my_json = "C:/Mypath/data/mydatagfile.json"

final_list = []
with open(my_json, "r") as js:
    js_dict = json.load(js)
    js_list = js_dict["invoice_lines"]

    for dico in js_list:
        typ = dico["type"]
        title = dico["title"]
        subtit = dico["subtitle"]
        dat = dico["date"]
        amount = dico["amount"]
        # List of list construction to use Dataframe method
        curr_list = typ + "," + title + "," + subtit + "," + dat + "," + amount
        curr_list = curr_list.split(",")
        final_list.append(curr_list)

    records_df = pd.DataFrame.from_dict(final_list)
    ## UPDATE A SHEET
    # add a sheet with 200 rows and 6 columns
    sheet.add_worksheet(rows=200,cols=6,title='MyNewSheetName')

    # get the instance of the second sheet
    sheet_runs = sheet.get_worksheet(6)

    sheet_runs.insert_rows(records_df.values.tolist())
