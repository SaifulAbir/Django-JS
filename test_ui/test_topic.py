import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addTopic(driver: webdriver.Chrome, data):
    add_topic = driver.find_element_by_class_name('addlink')
    add_topic.click()
    time.sleep(2)
    try:
        subject_id = driver.find_element_by_name('subject_id')
        subject_id.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_subject_id']):
            subject_id.send_keys(data['_subject_id'])
            subject_id.send_keys('\n')
            time.sleep(1)

        topic_name = driver.find_element_by_name('name')
        topic_name.clear()
        if not pd.isna(data['_name']):
            topic_name.send_keys(data['_name'])
            time.sleep(1)

        topic_save = driver.find_element_by_name('_save')
        topic_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0
