import pygsheets
import pandas as pd
import os
import time


#authorization
gc = pygsheets.authorize(service_file=os.getcwd()+'/client_secret.json')

df = pd.DataFrame()

# Create a column
df['name'] = ['John', 'Steve', 'Sarah']

try:
    sh = gc.open('Idealo_Scraper')
except:
    sh = gc.create('Idealo_Scraper')

def add_to_sheet(data_col):
    # Get Date
    date = time.strftime("%d-%m-%Y")
    # Open Subsheet by date
    try:
        wks = sh.worksheet_by_title(date)
    except:
        wks = sh.add_worksheet(date)
        try:
            wks.append_table(["Name", "Buy Price Brutto", "Current Amazon Price Brutto", "30 day Average", "BSR", "Rating Count", "Amazon Link", "Idealo Link", "Marge", "Marge %"])
        except:
            pass
    try:
        wks.append_table(data_col)
    except:
        pass
    

if __name__ == "__main__":
    add_to_sheet(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    add_to_sheet(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
    add_to_sheet(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
