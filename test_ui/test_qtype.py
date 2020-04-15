import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *

def addQtype(driver: webdriver.Chrome, data):
    add_qtype = driver.find_element_by_class_name('addlink')
    add_qtype.click()
    time.sleep(1)
    try:
        qtype_name = driver.find_element_by_name('name')
        qtype_name.clear()
        if not pd.isna(data['_name']):
            qtype_name.send_keys(data['_name'])
            time.sleep(1)

        qtype_date = driver.find_element_by_name('created_date_0')
        qtype_date.clear()
        if not pd.isna(data['_date']):
            qtype_date.send_keys(data['_date'])
            time.sleep(1)

        qtype_time = driver.find_element_by_name('created_date_1')
        qtype_time.clear()
        if not pd.isna(data['_time']):
            qtype_time.send_keys(data['_time'])
            time.sleep(1)

        qtype_save = driver.find_element_by_name('_save')
        qtype_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0


def updateQtype(driver: webdriver.Chrome, data):
    add_qtype = driver.find_element_by_class_name('addlink')
    add_qtype.click()
    time.sleep(2)
    try:
        qtype_name = driver.find_element_by_name('name')
        qtype_name.clear()
        if not pd.isna(data['_name']):
            qtype_name.send_keys(data['_name'])
            time.sleep(1)

        # qtype_date = driver.find_element_by_name('created_date_0')
        # qtype_date.clear()
        # if not pd.isna(data['_date']):
        #     qtype_date.send_keys(data['_date'])
        #     time.sleep(1)
        #
        # qtype_time = driver.find_element_by_name('created_date_1')
        # qtype_time.clear()
        # if not pd.isna(data['_time']):
        #     qtype_time.send_keys(data['_time'])
        #     time.sleep(1)

        qtype_save = driver.find_element_by_name('_save')
        qtype_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('success')
        return 1
    except NoSuchElementException:
        return 0
