from tkinter import *
import os
import re
import threading
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from pathlib import Path
import webbrowser
import time
import random
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import openpyxl
import pyinputplus as pyip
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl.styles import Font


'''
#  or bill sebil sam ivan, password or waimaolang2022


'''


def saveExcelNew(wb, name):
    try:
        wb.save(name)
    except Exception as e:
        print(e)


def process_g():
    ''' Main logic '''

    driver = webdriver.Firefox()
    driver.implicitly_wait(30)

    driver.get('https://crm2.waimaolang.cn/#/main/find/index/findSocialMedia/Facebook/led/global')
    driver.find_element(by=By.CSS_SELECTOR, value='input.el-input__inner[placeholder="用户名"]').send_keys('dido')
    driver.find_element(by=By.CSS_SELECTOR, value='input.el-input__inner[placeholder="公司名称"]').send_keys('深圳市经纬集运国际货运代理有限公司')
    driver.find_element(by=By.CSS_SELECTOR, value='input.el-input__inner[type="password"]').send_keys('kingtrans123') # or bill sebil sam ivan, password or waimaolang2022

    number_of_pages = pyip.inputInt(prompt="Enter pages: ", min=1)

    counter = 0
    currentPageDataList = []
    while True:
        # try:
        

        infoCard = driver.find_elements(by=By.CSS_SELECTOR, value='div.public-bottom-list-item')
        print('Total cards: ', len(infoCard))
        for i, item in enumerate(infoCard):
            title = item.find_element(by=By.CSS_SELECTOR, value='a').text
            title_url = item.find_element(by=By.CSS_SELECTOR, value='a').get_attribute('href')
            innerInfoList = item.find_elements(by=By.CSS_SELECTOR, value='div.public-bottom-list-item-text>div')
            cacheText = '%'
            cacheText += (title + '%')
            cacheText += (title_url + '%')
            for div in innerInfoList:
                cacheText += (div.text + '%')
            currentPageDataList.append(cacheText)
            print(f"{counter+1}-{i+1}\n{cacheText}\n\n")
        driver.execute_script('arguments[0].click()', driver.find_element(by=By.CSS_SELECTOR, value='button.btn-next'))
        time.sleep(random.random() * 17 + 2)
        print('Clicked!!')
        counter += 1
        if counter >= number_of_pages:
            break

    print('END')
    driver.close()
    # print(currentPageDataList[:2])
    print(f"Total found: {len(currentPageDataList)}")
    return currentPageDataList





remove_words = ["邮箱地址", "联系电话", "公司主页", "所属分类", "产品介绍", "公司简介", "地区/地点","地 区/地点", "ta的全名", "个人标签", "自我介绍", "公司名称", "主要行业", "职位/等级", "公司网址", "个人标签 " ]

def clean(text):
    for word in remove_words:
        text = text.replace(word, "")
    return text.strip()

raw_lt = process_g()
clean_lt = list(map(clean, raw_lt))
print(clean_lt, len(clean_lt))

# print('\n'*10)
# print(clean_lt[0])



def generate_excel(data_list, file_name):
    # Create a new Workbook and select the active sheet
    wb = openpyxl.Workbook()
    ws = wb.active

    # Iterate over each item in the list
    for row_index, item in enumerate(data_list, start=1):
        # Split the item by '%' and filter out empty strings
        cell_values = [val for val in item.split('%') if val]
        
        # Iterate over each value and place it in the corresponding cell
        for col_index, value in enumerate(cell_values, start=1):
            ws.cell(row=row_index, column=col_index, value=value)

    # Save the Workbook to the specified file
    wb.save(file_name)

file_name = "output.xlsx"
generate_excel(clean_lt, file_name)    