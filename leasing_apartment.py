# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 18:26:26 2022

@author: sarat
"""
import selenium
from selenium import webdriver 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select 
from webdriver_manager.chrome import ChromeDriverManager 

from datetime import datetime 
from time import sleep 

from bs4 import BeautifulSoup

import pandas as pd 

import requests 
from bs4 import BeautifulSoup
import gspread as gc

import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from oauth2client.service_account import ServiceAccountCredentials
import gspread_dataframe as gd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
    
####### lattitude apartment###############

with requests.Session() as session:
    page = requests.get("https://www.livewithlatitude.com/arlington/latitude/conventional/")
    
soup = BeautifulSoup(page.content, "html.parser")
for link in soup.find_all("a"):
    print("Inner Text: {}".format(link.text))
    print("Title: {}".format(link.get("title")))
    print("href: {}".format(link.get("href")))
    


soup.find_all("div", {"class": "property-page-content"})

# Fetch the page and create a Beautiful Soup object
page = requests.get("https://www.livewithlatitude.com/arlington/latitude/conventional/")
soup = BeautifulSoup(page.text, "lxml")

# Locate every div tags that has "quote" in its name
d = soup.find_all( "div", class_ = "fp-col rent" )
rent_list = []
n = len(d)

for i in range(n):
    rent_list.append(d[i].text)
    

#### Title 

d1 = soup.find_all( class_ = "fp-name-link" )
name_list = []
n = len(d1)

for i in range(n):
    name_list.append(d1[i].text)
    



d2 = soup.find_all( class_ = "fp-col sq-feet" )
sqft_list = []
n = len(d2)

for i in range(n):
    sqft_list.append(d2[i].text)

df = pd.DataFrame (list(zip(name_list, sqft_list, rent_list)), 
                   columns = ['name', 'sqft', 'rent'])




scope =["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/sarat/downloads/lattitude-361301-82ca12695bca.json', scope)

# authorize the clientsheet 
client = gspread.authorize(creds)


sheet = client.open('Lattitude Rent')
new_worksheet = sheet.add_worksheet(title='{}'.format(datetime.today().strftime('%Y-%m-%d')), rows=50, cols =4)


set_with_dataframe(new_worksheet, df)




#ws = gc.open(sheet).worksheet(datetime.today().strftime('%Y-%m-%d'))
#existing = gd.get_as_dataframe(ws)
#updated = existing.append(df)

#new_worksheet.update( df)













##################################################################################
