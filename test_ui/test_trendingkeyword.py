import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addTrendingkeyword(driver: webdriver.Chrome, data):
    add_addTrendingkeyword = driver.find_element_by_class_name('addlink')
    add_addTrendingkeyword.click()
    time.sleep(1)
    try:
        keyword_name = driver.find_element_by_name('keyword')
        keyword_name.clear()
        if not pd.isna(data['_keyword']):
            keyword_name.send_keys(data['_keyword'])
            time.sleep(1)

        location = driver.find_element_by_name('location')
        location.clear()
        if not pd.isna(data['_location']):
            location.send_keys(data['_location'])
            time.sleep(1)

        keyword_date = driver.find_element_by_name('created_date')
        keyword_date.clear()
        if not pd.isna(data['_date']):
            keyword_date.send_keys(data['_date'])
            time.sleep(1)

        qtype_save = driver.find_element_by_name('_save')
        qtype_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('success')
        return 1
    except NoSuchElementException:
        return 0
