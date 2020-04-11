import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addExamineeType(driver: webdriver.Chrome, data):
    add_e_type = driver.find_element_by_class_name('addlink')
    add_e_type.click()
    time.sleep(1)
    try:
        examinee_type = driver.find_element_by_name('name')
        examinee_type.clear()
        time.sleep(1)
        if not pd.isna(data['_examinee_type']):
            examinee_type.send_keys(data['_examinee_type'])
            time.sleep(1)

        save = driver.find_element_by_name('_save')
        save.submit()
        time.sleep(1)

        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0

