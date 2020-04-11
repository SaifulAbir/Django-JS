import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addExamCategory(driver: webdriver.Chrome, data):
    add_exam_cat = driver.find_element_by_class_name('addlink')
    add_exam_cat.click()
    time.sleep(2)
    try:
        exam_cat_name = driver.find_element_by_name('name')
        exam_cat_name.clear()
        if not pd.isna(data['_name']):
            exam_cat_name.send_keys(data['_name'])
            time.sleep(1)

        exam_cat_save = driver.find_element_by_name('_save')
        exam_cat_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0

