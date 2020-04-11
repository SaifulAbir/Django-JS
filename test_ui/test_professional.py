import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addProfessional(driver: webdriver.Chrome, data):
    add_professional = driver.find_element_by_class_name('addlink')
    add_professional.click()
    time.sleep(1)
    try:
        professional_id = driver.find_element_by_name('professional_id')
        professional_id.clear()
        time.sleep(1)
        if not pd.isna(data['_id']):
            professional_id.send_keys(data['_id'])
            time.sleep(1)

        name = driver.find_element_by_name('full_name')
        name.clear()
        time.sleep(1)
        if not pd.isna(data['_name']):
            name.send_keys(data['_name'])
            time.sleep(1)

        email = driver.find_element_by_name('email')
        email.clear()
        time.sleep(1)
        if not pd.isna(data['_email']):
            email.send_keys(data['_email'])
            time.sleep(1)

        phone = driver.find_element_by_name('phone')
        phone.clear()
        time.sleep(1)
        if not pd.isna(data['_phone']):
            phone.send_keys(data['_phone'])
            time.sleep(1)

        address = driver.find_element_by_name('address')
        time.sleep(1)
        if not pd.isna(data['_address']):
            address.send_keys(data['_address'])
            time.sleep(1)

        industry_expertise = driver.find_element_by_name('industry_expertise')
        time.sleep(1)
        if not pd.isna(data['_industry_expertise']):
            industry_expertise.send_keys(data['_industry_expertise'])
            time.sleep(1)

        about_me = driver.find_element_by_name('about_me')
        about_me.clear()
        time.sleep(1)
        if not pd.isna(data['_about_me']):
            about_me.send_keys(data['_about_me'])
            time.sleep(1)

        terms = driver.find_element_by_name('terms_and_condition_status')
        time.sleep(1)
        if not pd.isna(data['_terms_and_con']):
            if data['_terms_and_con'] == '1':
                terms.click()
        time.sleep(1)

        password = driver.find_element_by_name('password')
        password.clear()
        time.sleep(1)
        if not pd.isna(data['_password']):
            password.send_keys(data['_password'])
            time.sleep(5)



        save = driver.find_element_by_name('_save')
        save.submit()
        time.sleep(1)

        try:
            driver.find_element_by_class_name('success')
            return 1
        except NoSuchElementException:
            return 0
    except NoSuchElementException:
        return 0
