# Libraries for google spreadsheet API and functions!
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Libraries for date and time!
from datetime import datetime
from datetime import date

# Libraries for scraping weather off of the internet!
import bs4
from bs4 import BeautifulSoup
import requests, json
from pprint import pprint

from weather_data import degToCompass
from weather_data import get_weather

# Function to find the next available row in our spreadsheet
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("temp_humidity_logger").sheet1

# First, let's make a timestamp!
now = datetime.now()
current_time = now.strftime("%H:%M:%S") #format into text
today = date.today()
current_date = today.strftime("%m/%d/%Y") #format into text


# Get the weather!
weather = get_weather()

# Let's update the next available location
next_row = next_available_row(sheet)

# Begin filling out the information!
sheet.update_cell(next_row, 1, current_date)
sheet.update_cell(next_row, 2, current_time)
# sheet.update_cell(next_row, 3, internal_temperature)
# sheet.update_cell(next_row, 4, internal_humidity)
sheet.update_cell(next_row, 5, weather[0])
sheet.update_cell(next_row, 6, weather[1])
sheet.update_cell(next_row, 7, weather[2])
sheet.update_cell(next_row, 8, weather[3])
sheet.update_cell(next_row, 9, weather[4])
sheet.update_cell(next_row, 10, weather[5])
sheet.update_cell(next_row, 11, weather[6])
