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

from HTS221_oneshot_measurement import HTS221_oneshot_measurement

# Function to find the next available row in our spreadsheet
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(creds)

# Get the spreadsheet
logger_spreadsheet = gc.open("temp_humidity_logger")

# Current measurement is on sheet 0
sheet_current = logger_spreadsheet.get_worksheet(0)

# First, let's make a timestamp!
now = datetime.now()
current_time = now.strftime("%H:%M:%S") #format into text
today = date.today()
current_date = today.strftime("%m/%d/%Y") #format into text

# Get internal measurement
internal_measurement = HTS221_oneshot_measurement()

# Get the weather!
weather = get_weather()

# Begin filling out the information for current
sheet_current.update_cell(2, 1, current_date) # Todays Date
sheet_current.update_cell(2, 2, current_time) # Current Time
sheet_current.update_cell(2, 3, internal_measurement[0]) # Internal temperature
sheet_current.update_cell(2, 4, internal_measurement[1]) # Internal humidity
sheet_current.update_cell(2, 5, weather[0]) # External temperature
sheet_current.update_cell(2, 6, weather[1]) # External Humidity
sheet_current.update_cell(2, 7, weather[2]) # Wind speed
# sheet_current.update_cell(2, 8, weather[3]) # Wind gusts
sheet_current.update_cell(2, 8, weather[3]) # Wind Direction
sheet_current.update_cell(2, 9, weather[4]) # Description of weather
sheet_current.update_cell(2, 10, weather[5]) # Pressure


# Let us fill out the historical sheet on sheet one
sheet_history = logger_spreadsheet.get_worksheet(1)

# Get the next empty row for update location
next_row = next_available_row(sheet_history)

# Begin filling out the information for history
sheet_history.update_cell(next_row, 1, current_date) # Todays Date
sheet_history.update_cell(next_row, 2, current_time) # Current Time
sheet_history.update_cell(next_row, 3, internal_measurement[0]) # Internal temperature
sheet_history.update_cell(next_row, 4, internal_measurement[1]) # Internal humidity
sheet_history.update_cell(next_row, 5, weather[0]) # External temperature
sheet_history.update_cell(next_row, 6, weather[1]) # External Humidity
sheet_history.update_cell(next_row, 7, weather[2]) # Wind speed
# sheet.update_cell(next_row, 8, weather[3]) # Wind gusts
sheet_history.update_cell(next_row, 8, weather[3]) # Wind Direction
sheet_history.update_cell(next_row, 9, weather[4]) # Description of weather
sheet_history.update_cell(next_row, 10, weather[5]) # Pressure
