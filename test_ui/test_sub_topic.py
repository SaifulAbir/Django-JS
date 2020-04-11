import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addSubTopic(driver: webdriver.Chrome, data):
    add_sub_topic = driver.find_element_by_class_name('addlink')
    add_sub_topic.click()
    time.sleep(2)
    try:
        subject_id = driver.find_element_by_name('subject')
        subject_id.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_subject_id']):
            subject_id.send_keys(data['_subject_id'])
            # subject_id.send_keys('\n')
            time.sleep(1)

        topic_name = driver.find_element_by_name('topics')
        topic_name.send_keys('Select Topics')
        time.sleep(1)
        if not pd.isna(data['_topic_name']):
            topic_name.send_keys(data['_topic_name'])
            # topic_name.send_keys('\n')
            time.sleep(1)

        sub_topic_name = driver.find_element_by_name('name')
        sub_topic_name.clear()
        if not pd.isna(data['_name']):
            sub_topic_name.send_keys(data['_name'])
            time.sleep(1)

        sub_topic_save = driver.find_element_by_name('_save')
        sub_topic_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0
