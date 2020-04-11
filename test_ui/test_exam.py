import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from .config import *


class Actions(object):
    pass


def addExam(driver: webdriver.Chrome, data):
    add_qtype = driver.find_element_by_class_name('addlink')
    add_qtype.click()
    time.sleep(1)

    try:
        if not pd.isna(data['_exam_code']):
            exam_code = driver.find_element_by_name("exam_code")
            exam_code.send_keys(data['_exam_code'])
            time.sleep(1)

        if not pd.isna(data['_exam_name']):
            exam_name = driver.find_element_by_name("exam_name")
            exam_name.send_keys(data['_exam_name'])
            time.sleep(1)

        if not pd.isna(data['_pass_mark']):
            pass_mark = driver.find_element_by_name("pass_mark")
            pass_mark.send_keys(data['_pass_mark'])
            time.sleep(1)

        if not pd.isna(data['_duration']):
            duration = driver.find_element_by_name("duration")
            duration.send_keys(data['_duration'])
            time.sleep(1)

        exam_category = driver.find_element_by_name('exam_category')
        exam_category.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_exam_category']):
            exam_category.send_keys('/n')
            time.sleep(1)
            exam_category.send_keys(data['_exam_category'])
            time.sleep(1)

        exam_level = driver.find_element_by_name('exam_level')
        exam_level.send_keys('------')
        time.sleep(1)
        if not pd.isna(data['_exam_level']):
            exam_level.send_keys('/n')
            time.sleep(1)
            exam_level.send_keys(data['_exam_level'])
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

        is_featured = driver.find_element_by_id('id_is_featured')
        if not pd.isna(data['_is_featured']):
            is_featured.send_keys('/n')
            time.sleep(1)
            is_featured.send_keys(data['_is_featured'])
            time.sleep(1)

        if not pd.isna(data['_instruction']):
            driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
            question_field = driver.find_element_by_xpath("/html/body/p")
            question_field.send_keys(data['_instruction'])
            driver.switch_to.default_content()
            time.sleep(1)

        if not pd.isna(data['_question_selection_type']):
            question_selection_type = driver.find_element_by_name("question_selection_type")
            question_selection_type.send_keys('')
            time.sleep(1)

        if not pd.isna(data['_exam_type']):
            exam_type = driver.find_element_by_name("exam_type")
            exam_type.send_keys('')
            time.sleep(1)

        if not pd.isna(data['_exam_fee']):
            exam_fee = driver.find_element_by_name("exam_fee")
            exam_fee.send_keys('')
            time.sleep(1)

        if not pd.isna(data['_promo_code']):
            promo_code = driver.find_element_by_name("promo_code")
            promo_code.send_keys('')
            time.sleep(1)

        if not pd.isna(data['_discount_price']):
            exam_code = driver.find_element_by_name("discount_price")
            exam_code.send_keys('50 tk')
            time.sleep(1)

        if not pd.isna(data['_discount_percent']):
            discount_percent = driver.find_element_by_name("discount_percent")
            discount_percent.send_keys('')
            time.sleep(1)

        if not pd.isna(data['_re_registration_delay']):
            re_registration_delay = driver.find_element_by_name("re_registration_delay")
            re_registration_delay.send_keys('')
            time.sleep(1)

        if not pd.isna(data['_questionnaire']):
            questionnaire = data['_questionnaire'].split(',')
            c = len(questionnaire)
            for row in range(len(questionnaire)):
                try:
                    if c - row <= 3:
                        if c - row <= 1:
                            add_questionnaire = driver.find_element_by_name('examquestionnairedetails_set-'+str(row)+'-questionnaire')
                        else:
                            add_questionnaire = driver.find_element_by_name('examquestionnairedetails_set-'+str(row)+'-questionnaire')
                        add_questionnaire.send_keys(questionnaire[row])
                        time.sleep(1)

                    else:
                        add_questionnaire = driver.find_element_by_name('examquestionnairedetails_set-'+str(row)+'-questionnaire')
                        add_questionnaire.send_keys(questionnaire[row])
                        time.sleep(1)
                        driver.find_element_by_xpath('//*[@id="examquestionnairedetails_set-group"]/fieldset/div[5]/a').click()
                        time.sleep(1)

                except Exception as ex:
                    print("Print Row " + row)

        question_save = driver.find_element_by_name('_save')
        question_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0
