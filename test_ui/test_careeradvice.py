import os
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addCareeradvice(driver: webdriver.Chrome, data):
    addCareeradvice = driver.find_element_by_class_name('addlink')
    addCareeradvice.click()
    time.sleep(1)
    try:
        title = driver.find_element_by_name('title')
        title.clear()
        if not pd.isna(data['_title']):
            title.send_keys(data['_title'])
            time.sleep(1)

        short_description = driver.find_element_by_name('short_description')
        short_description.clear()
        if not pd.isna(data['_short_description']):
            short_description.send_keys(data['_short_description'])
            time.sleep(1)

        description = driver.find_element_by_name('description')
        description.clear()
        if not pd.isna(data['_description']):
            description.send_keys(data['_description'])
            time.sleep(1)

        author = driver.find_element_by_name('author')
        author.clear()
        if not pd.isna(data['_author']):
            author.send_keys(data['_author'])
            time.sleep(1)

        qtype_save = driver.find_element_by_name('_save')
        qtype_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('success')
        return 1
    except NoSuchElementException:
        return 0
