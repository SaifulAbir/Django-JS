import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addSubject(driver: webdriver.Chrome, data):
    add_qtype = driver.find_element_by_class_name('addlink')
    add_qtype.click()
    time.sleep(2)
    try:
        qtype_name = driver.find_element_by_name('name')
        qtype_name.clear()
        if not pd.isna(data['_name']):
            qtype_name.send_keys(data['_name'])
            time.sleep(1)

        qtype_save = driver.find_element_by_name('_save')
        qtype_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0

    # if not pd.isna(data['_subjectcode']):
    #    subject_code = driver.find_element_by_name('subject_code')
    #    subject_code.send_keys(data['_subjectcode'])
    #
    # if not pd.isna(data['_subjectname']):
    #    subject_name = driver.find_element_by_name('subject_text')
    #    subject_name.send_keys(data['_subjectname'])
    #
    # save_button = driver.find_element_by_name('_save')
    # save_button.click()
    #
    #
    # try:
    #    time.sleep(DELAY_LONG)
    #    driver.find_element_by_link_text(data['_subjectname'])
    #    return 1
    # except NoSuchElementException:
    #    return 0
    #
