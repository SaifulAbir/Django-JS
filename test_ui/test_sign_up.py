import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addSignUp(driver: webdriver.Chrome, data):
    menu = driver.find_element_by_class_name('navbar-toggler-icon').click()
    add_professional = driver.find_element_by_link_text('Register')
    add_professional.click()
    # driver.get('http://127.0.0.1/professional/register/')
    try:

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

        password = driver.find_element_by_id('password')
        password.clear()
        time.sleep(1)
        if not pd.isna(data['_password']):
            password.send_keys(data['_password'])
            time.sleep(1)

        con_password = driver.find_element_by_name('confirm_password')
        con_password.clear()
        time.sleep(1)
        if not pd.isna(data['_con_password']):
            con_password.send_keys(data['_con_password'])
            time.sleep(1)

        accept = driver.find_element_by_class_name('dot')
        time.sleep(1)
        if not pd.isna(data['_accept']):
            if data['_accept'] == '1':
                accept.click()

        save = driver.find_element_by_xpath('//*[@id="sign-up"]/button')
        save.submit()
        time.sleep(DELAY_LONG)

        try:
            driver.find_element_by_class_name('swal2-success-ring')
            return 1
        except NoSuchElementException:
            return 0
    except NoSuchElementException:
        return 0
