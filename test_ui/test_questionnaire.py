import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addQuestionnaire(driver: webdriver.Chrome, data):

    add_sub_topic = driver.find_element_by_class_name('addlink')
    add_sub_topic.click()
    time.sleep(1)
    try:

        questionnaire_name = driver.find_element_by_id('questionnaire_name')
        questionnaire_name.clear()
        if not pd.isna(data['_questionnaire_name']):
            questionnaire_name.send_keys(data['_questionnaire_name'])
            time.sleep(1)

        subject = driver.find_element_by_id('subject')
        subject.click()
        if not pd.isna(data['_subject']):
            subject.send_keys(data['_subject'])
            # remarks.send_keys('\n')
            time.sleep(1)

        topic_name = driver.find_element_by_id('topic')
        time.sleep(1)
        if not pd.isna(data['_topic']):
            topic_name.send_keys(data['_topic'])
            # topic_name.send_keys('\n')
            time.sleep(1)

        sub_topic_name = driver.find_element_by_id('sub_topic')
        time.sleep(1)
        if not pd.isna(data['_sub_topic']):
            sub_topic_name.send_keys(data['_sub_topic'])
            # sub_topic_name.send_keys('\n')
            time.sleep(1)

        remarks = driver.find_element_by_id('remarks')
        time.sleep(1)
        if not pd.isna(data['_remarks']):
            remarks.send_keys(data['_remarks'])
            # subject_id.send_keys('\n')
            time.sleep(1)

        question_btn = driver.find_element_by_xpath('//*[@id="content"]/section[2]/div/button')
        question_btn.click()
        time.sleep(1)
        if not pd.isna(data['_question']):
            question = data['_question'].split(',')
            c = len(question)
            for row in range(len(question)):
                try:
                    add_question = driver.find_element_by_id('question_contains')
                    add_question.clear()
                    add_question.send_keys(question[row])
                    time.sleep(1)
                    driver.find_element_by_id('ques_search').click()
                    time.sleep(1)
                    driver.find_element_by_link_text('Select').click()
                    time.sleep(1)

                except Exception as ex:
                    print("Print Row " + str(row))

        questionnaire_save = driver.find_element_by_id('create_questionnaire')
        questionnaire_save.click()
        time.sleep(3)
        driver.find_element_by_id('questionnaire_name')
        return 1
    except NoSuchElementException:
        return 0
