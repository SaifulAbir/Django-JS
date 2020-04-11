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

        questionnaire_name = driver.find_element_by_name('name')
        questionnaire_name.clear()
        if not pd.isna(data['_questionnaire_name']):
            questionnaire_name.send_keys(data['_questionnaire_name'])
            time.sleep(1)

        remarks = driver.find_element_by_name('remarks')
        remarks.clear()
        if not pd.isna(data['_remarks']):
            remarks.send_keys(data['_remarks'])
            # remarks.send_keys('\n')
            time.sleep(1)

        subject_id = driver.find_element_by_name('subject')
        subject_id.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_subject_id']):
            subject_id.send_keys(data['_subject_id'])
            # subject_id.send_keys('\n')
            time.sleep(1)

        topic_name = driver.find_element_by_name('topic')
        topic_name.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_topic']):
            topic_name.send_keys(data['_topic'])
            # topic_name.send_keys('\n')
            time.sleep(1)

        sub_topic_name = driver.find_element_by_name('sub_topic')
        sub_topic_name.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_sub_topic']):
            sub_topic_name.send_keys(data['_sub_topic'])
            # sub_topic_name.send_keys('\n')
            time.sleep(1)

        if not pd.isna(data['_question']):
            question = data['_question'].split(',')
            c = len(question)
            for row in range(len(question)):
                try:
                    if c-row <= 5:
                        if c-row <= 1:
                            # add_answer = driver.find_element_by_name('answers-__prefix__-name')
                            add_question = driver.find_element_by_name('questionnairedetail_set-' + str(row) + '-question_id')
                        else:
                            add_question = driver.find_element_by_name('questionnairedetail_set-' + str(row) + '-question_id')

                        add_question.send_keys('---------')
                        time.sleep(1)
                        add_question.send_keys('<p>'+question[row]+'</p>')
                        time.sleep(1)

                    else:
                        add_question = driver.find_element_by_name('questionnairedetail_set-' + str(row) + '-question_id')
                        add_question.send_keys('---------')
                        time.sleep(1)
                        add_question.send_keys('<p>'+question[row]+'</p>')
                        time.sleep(1)
                        driver.find_element_by_link_text("Add another Questionnaire Detail").click()
                        time.sleep(1)

                except Exception as ex:
                    print("Print Row " + row)

        questionnaire_save = driver.find_element_by_name('_save')
        questionnaire_save.submit()
        time.sleep(1)
        # driver.find_element_by_class_name('addlink')
        driver.find_element_by_class_name('messagelist')
        return 1
    except NoSuchElementException:
        return 0
