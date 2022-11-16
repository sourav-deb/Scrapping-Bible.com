from os import replace
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import numpy as np
import cv2
import re
import pandas as pd
from selenium.webdriver.common.by import By


PATH = "C:/Users/PC-SOURAV/Desktop/MY DRIVE/Projects/Scrapping/bibleScrape/chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://my.bible.com/en-GB/sign-in")

# Credentials:  sourav.deb298@gmail.com   Basketball123

driver.find_element_by_id("signin-username").send_keys("sourav.deb298@gmail.com")
driver.find_element_by_id("signin-password").send_keys("Basketball123")
button = driver.find_element_by_xpath("/html/body/div[2]/div/div/article/div/div/form[3]/p[5]/button")
button.click()

driver.get("https://my.bible.com/en-GB/bible")

GENESIS = '18'
url = "https://my.bible.com/bible/406/GEN."+GENESIS+".ERV?parallel=2671"
driver.get(url)
# url = "https://my.bible.com/bible/406/GEN.1.ERV?parallel=2671"


# Check English----------
engReader = driver.find_element_by_xpath("//*[@id='react-app-Bible']/div/div/div[1]/div[2]/div[2]/div/div[1]/div/div/div/div")
engV = engReader.find_elements(By.CLASS_NAME,'verse')
engVerse = []

for i in engV:
        engVerse.append(i.text) 

def remove(engVerse):
    pattern = '[0-9]'
    newline = '[\n]'
    engVerse = [re.sub(pattern, '', i) for i in engVerse]
    engVerse = [re.sub(newline, ' ', i) for i in engVerse]
    return engVerse
    
newEngVerse = remove(engVerse)
# print(newEngVerse)

print("----------") 
newEngVerse = [i for i in newEngVerse if i]
# print(newEngVerse)
print(len(newEngVerse))
print("----------")

# Check Nepali----------

nepReader = driver.find_element_by_xpath("//*[@id='react-app-Bible']/div/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div/div")
nepV = nepReader.find_elements(By.CLASS_NAME,'verse')
nepVerse = []

for i in nepV:
    nepVerse.append(i.text) 

def remove(nepVerse):
    pattern = '[0-9]'
    newline = '[\n]'
    nepVerse = [re.sub(pattern, '', i) for i in nepVerse]
    nepVerse = [re.sub(newline, ' ', i) for i in nepVerse]
    return nepVerse
    
newNepVerse = remove(nepVerse)
# print(newEngVerse)

print("----------")  
newNepVerse = [i for i in newNepVerse if i]   
# print(newNepVerse)
print(len(newNepVerse))
print("----------")
    
driver.quit()

# Creating a new data frame
df = pd.DataFrame()

# ----------------- for 1st execution only
# newDataframe['Serial'] = newDataframe.index.values
df['English'] = newEngVerse
df['Nepali'] = newNepVerse

# Converting the data frame to an excel file

df = df.to_excel('GENESIS '+GENESIS+'.xlsx', index = True, index_label='Serial')
print("Done...")
# -----------------





# excel_data_df = pd.read_excel('Chapter1.xlsx')
# excelEng = excel_data_df['English']
# excelNep = excel_data_df['Nepali']

# # excelEng & newEngVerse
# # excelNep & newNepVerse two lists
# # -----------------

# for i in excelEng:
#     newEngVerse.insert(-1,i)
    
# for i in excelNep:
#     newNepVerse.insert(-1,i)
    
# # newDataframe['Serial'] = newDataframe.index.values
# df['English'] = newEngVerse
# df['Nepali'] = newNepVerse

# # Converting the data frame to an excel file
# df = df.to_excel('Chapter1.xlsx', index = False)

# print("Done...")








