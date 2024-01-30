import time
import numpy as np
import cv2
import re
import pandas as pd
import os
from xlsxwriter import Workbook


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

print(selenium.__version__)

# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=options)
driver = webdriver.Edge()
# driver = webdriver.Chrome()


driver.get("https://my.bible.com/en-GB/sign-in")

time.sleep(3)

try:
    driver.find_element(By.ID,"signin-username").send_keys("sourav.deb298@gmail.com")
    driver.find_element(By.ID,"signin-password").send_keys("Basketball123")
    button= driver.find_element(By.XPATH,"//*[@id='signin_form']/p[5]/button")
    # button = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/article/div/div/form[3]/p[5]/button")
    # button = driver.find_element(By.NAME,"button")
    time.sleep(10)
    
    print("Button Detected....")
    driver.execute_script("arguments[0].click();", button)
    # button.click
    print("SIGNED IN....")
except:
    print("Sign In ERROR")
    driver.quit()
    exit()

time.sleep(10)

def bibleChapter(a,b):

    # VERSE = None
    # CHAPTER = '1'
    url = "https://my.bible.com/bible/406/"+VERSE+"."+CHAPTER+".ERV?parallel=2671"
    # url = "https://my.bible.com/bible/406/GEN.1.ERV?parallel=2671"
    driver.get(url)
    time.sleep(10)

    print("Testing.....")


    Ecol = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[1]/div[2]/div[2]/div/div[1]/div/div/div/div")
    Ncol = driver.find_element(By.XPATH,"/html/body/div[2]/div/div/div/div[1]/div[2]/div[3]/div/div[1]/div/div/div/div")
        
    #  ENGLISH EXTRACTION
    print("ENGLISH EXTRACTION")

    engV = Ecol.find_elements(By.CLASS_NAME,'verse')
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

    #  NEPALI EXTRACTION
    print("NEPALI EXTRACTION")

    nepV = Ncol.find_elements(By.CLASS_NAME,'verse')
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
    # print(newNepVerse)

    print("----------") 
    newNepVerse = [i for i in newNepVerse if i]
    # print(newNepVerse)
    print(len(newNepVerse))
    print("----------")

    time.sleep(5)

    if not os.path.exists(VERSE):
        os.mkdir(VERSE)
        print(f"'{VERSE}' Folder Created.")
    else:
        print(f"Folder '{VERSE}' already exists.")


    if len(newEngVerse) == len(newNepVerse):
        # Creating a new data frame
        df = pd.DataFrame()

        # ----------------- for 1st execution only
        # newDataframe['Serial'] = newDataframe.index.values
        df['English'] = newEngVerse
        df['Nepali'] = newNepVerse
        
        # Converting the data frame to an excel file
        df.to_excel('./'+VERSE+'/'+VERSE+' '+CHAPTER+'.xlsx', index = True, index_label='Serial')
        print("EXCEL CREATED.")
        # print(df)
        # -----------------

    else:
        print("English Rows != Nepali Rows")

        unmatchedEng = pd.DataFrame()
        unmatchedEng['English'] = newEngVerse
        unmatchedNep = pd.DataFrame()
        unmatchedNep['Nepali'] = newNepVerse

        unmatchedEng.to_excel('./'+VERSE+'/'+VERSE+' '+CHAPTER+'.xlsx', sheet_name='English', index = True, index_label='Serial')

        unmatchedPath = './'+VERSE+'/'+VERSE+' '+CHAPTER+'.xlsx'
        # with pd.ExcelWriter(unmatchedPath, engine='xlsxwriter',mode='a') as writer:
            # unmatchedNep.to_excel(writer, sheet_name='Nepali', index=True, index_label='Serial')
        
        writer = pd.ExcelWriter(unmatchedPath, engine = 'xlsxwriter')
        unmatchedEng.to_excel(writer, sheet_name = 'English')
        unmatchedNep.to_excel(writer, sheet_name = 'Nepali')
        writer.close()
        print("EXCEL CREATED.")


        # unmatchedNep.to_excel('./'+VERSE+'/'+VERSE+' '+CHAPTER+'.xlsx', sheet_name='Nepali', index = True, index_label='Serial')

        
        # try:
        #     filePath = './'+VERSE+'/record.xlsx'
        #     recordExcel = pd.ExcelFile(filePath)

        #     parsedExcel = recordExcel.parse('Sheet1')

        #     record = pd.DataFrame()
        #     record['verse'] = VERSE
        #     record['chapter'] = CHAPTER
        #     record['lenEngVerse'] = len(newEngVerse)
        #     record['lenNepVerse'] = len(newNepVerse)

        #     record = pd.concat([parsedExcel, record], ignore_index=True)
        #     record.to_excel('./'+VERSE+'/record.xlsx', sheet_name='Sheet1', index = False)
        #     print("Unscraped Data Updated in record.xlsx")
        
        # except:
        #     record = pd.DataFrame()
        #     record['verse'] = VERSE
        #     record['chapter'] = CHAPTER
        #     record['lenEngVerse'] = len(newEngVerse)
        #     record['lenNepVerse'] = len(newNepVerse)

        #     record.to_excel('./'+VERSE+'/record.xlsx', sheet_name='Sheet1', index = False)
        #     print("Unscraped Data Updated in record.xlsx")

#Change it according to Verse & its Chapters
# VERSE = '2KI'
# Chap = 25

# VERSE = ['GEN','EXO','LEV','NUM','DEU','JOS','JDG','RUT','1SA','2SA','1KI','2KI','1CH','2CH','EZR','NEH','EST','JOB','PSA']
# Chap = [50,40,27,36,34,24,21,4,31,24,22,25,29,36,10,13,10,42,150]

VERSES = {'REV' : 22}

for j in VERSES:
    VERSE = j
    Chap = VERSES[j]
    i = 18
    while(i<=Chap):
        CHAPTER = i
        CHAPTER = str(CHAPTER)
        print("CHAPTER "+ CHAPTER)
        bibleChapter(VERSE,CHAPTER)
        i+=1
    print(f'VERSE {VERSE} CREATED!')


driver.quit()




# i = 1
# while(i<=Chap):
#     CHAPTER = i
#     CHAPTER = str(CHAPTER)
#     print("CHAPTER "+ CHAPTER)
#     bibleChapter(VERSE,CHAPTER)
#     i+=1

# driver.quit()

