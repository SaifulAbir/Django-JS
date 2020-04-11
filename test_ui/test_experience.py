import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addExperience(driver: webdriver.Chrome, data):
    add_experience = driver.find_element_by_class_name('addlink')
    add_experience.click()
    time.sleep(1)
    try:

        if not pd.isna(data['_name']):
            experience_name = driver.find_element_by_name('name')
            experience_name.clear()
            experience_name.send_keys(data['_name'])
            time.sleep(1)

        if not pd.isna(data['_date']):
            created_date = driver.find_element_by_name('created_date_0')
            created_date.clear()
            created_date.send_keys(data['_date'])
        else:
            created_date = driver.find_element_by_link_text('Today')
            created_date.click()
        time.sleep(1)

        if not pd.isna(data['_time']):
            created_time = driver.find_element_by_name('created_date_1')
            created_time.clear()
            created_time.send_keys(data['_time'])
        else:
            created_time = driver.find_element_by_link_text('Now')
            created_time.click()
        time.sleep(1)

        experience_save = driver.find_element_by_name('_save')
        experience_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('success')
        return 1
    except NoSuchElementException:
        return 0


def updateExperience(driver: webdriver.Chrome, data):
    add_experience = driver.find_element_by_class_name('addlink')
    add_experience.click()
    time.sleep(1)
    try:

        if not pd.isna(data['_name']):
            experience_name = driver.find_element_by_name('name')
            experience_name.clear()
            experience_name.send_keys(data['_name'])
            time.sleep(1)

        if not pd.isna(data['_date']):
            date = driver.find_element_by_name('created_date_0')
            date.clear()
            date.send_keys(data['_date'])
        else:
            date = driver.find_element_by_link_text('Today')
            date.click()
        time.sleep(1)

        if not pd.isna(data['_time']):
            date = driver.find_element_by_name('created_date_1')
            date.clear()
            date.send_keys(data['_time'])
        else:
            date = driver.find_element_by_link_text('Now')
            date.click()
        time.sleep(1)

        experience_save = driver.find_element_by_name('_save')
        experience_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0