import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addExaminee(driver: webdriver.Chrome, data):
    add_examinee = driver.find_element_by_class_name('addlink')
    add_examinee.click()
    time.sleep(1)
    try:
        username = driver.find_element_by_name('username')
        username.clear()
        time.sleep(1)
        if not pd.isna(data['_username']):
            username.send_keys(data['_username'])
            time.sleep(1)

        name = driver.find_element_by_name('name')
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

        password = driver.find_element_by_name('password')
        password.clear()
        time.sleep(1)
        if not pd.isna(data['_password']):
            password.send_keys(data['_password'])
            time.sleep(1)

        examinee_type = driver.find_element_by_name('examinee_type')
        examinee_type.send_keys('--------')
        time.sleep(1)
        if not pd.isna(data['_examinee_type']):
            examinee_type.send_keys(data['_examinee_type'])
            time.sleep(1)

        batch_number = driver.find_element_by_name('batch_number')
        batch_number.clear()
        time.sleep(1)
        if not pd.isna(data['_batch_number']):
            batch_number.send_keys(data['_batch_number'])
            time.sleep(1)

        mobile_number = driver.find_element_by_name('mobile_number')
        mobile_number.clear()
        time.sleep(1)
        if not pd.isna(data['_mobile_number']):
            mobile_number.send_keys(data['_mobile_number'])
            time.sleep(1)

        father_name = driver.find_element_by_name('father_name')
        father_name.clear()
        time.sleep(1)
        if not pd.isna(data['_father_name']):
            father_name.send_keys(data['_father_name'])
            time.sleep(1)

        mother_name = driver.find_element_by_name('mother_name')
        mother_name.clear()
        time.sleep(1)
        if not pd.isna(data['_mother_name']):
            mother_name.send_keys(data['_mother_name'])
            time.sleep(1)

        national_id_number = driver.find_element_by_name('national_id_number')
        national_id_number.clear()
        time.sleep(1)
        if not pd.isna(data['_national_id_number']):
            national_id_number.send_keys(data['_national_id_number'])
            time.sleep(1)

        address = driver.find_element_by_name('address')
        address.clear()
        time.sleep(1)
        if not pd.isna(data['_address']):
            address.send_keys(data['_address'])
            time.sleep(1)

        signup_verification_code = driver.find_element_by_name('signup_verification_code')
        signup_verification_code.clear()
        time.sleep(1)
        if not pd.isna(data['_signup_v_code']):
            signup_verification_code.send_keys(data['_signup_v_code'])
            time.sleep(1)

        status = driver.find_element_by_name('status')
        status.click()
        time.sleep(1)
        # if not pd.isna(data['_status']):
        #     status.send_keys(data['_status'])
        #     time.sleep(1)

        # examinee_create_date = driver.find_element_by_name('created_date_0')
        # examinee_create_date.clear()
        # if not pd.isna(data['_date']):
        #     examinee_create_date.send_keys(data['_date'])
        #     time.sleep(1)
        #
        # examinee_create_time = driver.find_element_by_name('created_date_1')
        # examinee_create_time.clear()
        # if not pd.isna(data['_time']):
        #     examinee_create_time.send_keys(data['_time'])
        #     time.sleep(1)


        save = driver.find_element_by_name('_save')
        save.submit()
        time.sleep(1)

        driver.find_element_by_class_name('addlink')
        return 1
    except NoSuchElementException:
        return 0

