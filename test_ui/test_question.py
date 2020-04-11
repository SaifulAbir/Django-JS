import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from .config import *


class Actions(object):
    pass


def addQuestion(driver: webdriver.Chrome, data):
    add_qtype = driver.find_element_by_class_name('addlink')
    add_qtype.click()
    time.sleep(1)

    try:
        if not pd.isna(data['_question']):
            driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
            question_field = driver.find_element_by_xpath("/html/body/p")
            question_field.send_keys(data['_question'])
            driver.switch_to.default_content()
            time.sleep(1)

        qtype = driver.find_element_by_name('qtype')
        qtype.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_qtype']):
            qtype.send_keys('/n')
            time.sleep(1)
            qtype.send_keys(data['_qtype'])
            time.sleep(1)

        difficulty = driver.find_element_by_name('difficulties')
        difficulty.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_difficulty']):
            difficulty.send_keys('/n')
            time.sleep(1)
            difficulty.send_keys(data['_difficulty'])
            time.sleep(1)

        subject = driver.find_element_by_name('subject')
        subject.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_subject']):
            subject.send_keys('/n')
            time.sleep(1)
            subject.send_keys(data['_subject'])
            time.sleep(1)

        topic = driver.find_element_by_name('topic')
        topic.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_topic']):
            topic.send_keys('/n')
            time.sleep(1)
            topic.send_keys(data['_topic'])
            time.sleep(1)

        sub_topic = driver.find_element_by_name('sub_topic')
        sub_topic.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_sub_topic']):
            sub_topic.send_keys('/n')
            time.sleep(1)
            sub_topic.send_keys(data['_sub_topic'])
            time.sleep(1)

        question_id = driver.find_element_by_name('question_id')
        question_id.clear()
        time.sleep(1)
        if not pd.isna(data['_question_id']):
            question_id.send_keys(data['_question_id'])
            time.sleep(1)

        if not pd.isna(data['_answer']):
            answer = data['_answer'].split(',')
            c = len(answer)
            for row in range(len(answer)):
                try:
                    if c-row <= 2:
                        if c-row <= 1:
                            # add_answer = driver.find_element_by_name('answers-__prefix__-name')
                            add_answer = driver.find_element_by_name('answers-' + str(row) + '-name')
                        else:
                            add_answer = driver.find_element_by_name('answers-' + str(row) + '-name')

                        add_answer.clear()
                        time.sleep(1)
                        add_answer.send_keys(answer[row])
                        time.sleep(1)

                    else:
                        add_answer = driver.find_element_by_name('answers-' + str(row) + '-name')
                        add_answer.clear()
                        time.sleep(1)
                        add_answer.send_keys(answer[row])
                        time.sleep(1)
                        driver.find_element_by_xpath("//*[text()[contains(., 'Add another Answer')]]").click()
                        time.sleep(1)

                except Exception as ex:
                    print("Print Row " + row)
        correct = driver.find_element_by_id('id_answers-0-correct')
        correct.click()

        question_save = driver.find_element_by_name('_save')
        question_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0
