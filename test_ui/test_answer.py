import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addAnswer(driver: webdriver.Chrome, data):
    add_topic = driver.find_element_by_class_name('addlink')
    add_topic.click()
    time.sleep(2)
    try:
        answer = driver.find_element_by_name('name')
        answer.clear()
        if not pd.isna(data['_answer']):
            answer.send_keys(data['_answer'])
            answer.send_keys('\n')
            time.sleep(1)

        question = driver.find_element_by_name('question')
        question.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_question']):
            question.send_keys('<p>'+data['_question']+'<p>')
            time.sleep(1)

        topic_save = driver.find_element_by_name('_save')
        topic_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0
