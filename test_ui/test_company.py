import os
import time

from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from .config import *
from selenium.webdriver.ie.webdriver import WebDriver


def addCompany(driver: WebDriver, data):
    add_company = driver.find_element_by_class_name('addlink')
    add_company.click()
    time.sleep(1)

    try:
        if not pd.isna(data['_com_name']):
            company_name = driver.find_element_by_name('name')
            company_name.send_keys(data['_com_name'])
        if not pd.isna(data['_com_address']):
            company_address = driver.find_element_by_name('address')
            company_address.send_keys(data['_com_address'])
        if not pd.isna(data['_com_phone_1']):
            company_phone1 = driver.find_element_by_name('company_contact_no_one')
            company_phone1.send_keys(data['_com_phone_1'])
        if not pd.isna(data['_com_phone_2']):
            company_phone2 = driver.find_element_by_name('company_contact_no_two')
            company_phone2.send_keys(data['_com_phone_2'])
        if not pd.isna(data['_com_phone_3']):
            company_phone3 = driver.find_element_by_name('company_contact_no_three')
            company_phone3.send_keys(data['_com_phone_3'])
        if not pd.isna(data['_official_email']):
            ofc_email = driver.find_element_by_name('email')
            ofc_email.send_keys(data['_official_email'])
        if not pd.isna(data['_cont_per_name']):
            contact_person_name = driver.find_element_by_name('contact_person')
            contact_person_name.send_keys(data['_cont_per_name'])
        if not pd.isna(data['_cont_per_designation']):
            contact_person_designation = driver.find_element_by_name('contact_person_designation')
            contact_person_designation.send_keys(data['_cont_per_designation'])
        if not pd.isna(data['_cont_per_mobile']):
            contact_person_mobile = driver.find_element_by_name('contact_person_mobile_no')
            contact_person_mobile.send_keys(data['_cont_per_mobile'])
        if not pd.isna(data['_cont_per_email']):
            contact_person_email = driver.find_element_by_name('contact_person_email')
            contact_person_email.send_keys(data['_cont_per_email'])
        if not pd.isna(data['_total_hr']):
            total_hr = driver.find_element_by_name('total_number_of_human_resources')
            total_hr.send_keys(data['_total_hr'])
        if not pd.isna(data['_it_hr']):
            IT_hr = driver.find_element_by_name('no_of_it_resources')
            IT_hr.send_keys(data['_it_hr'])
        save_btn = driver.find_element_by_name('_save')
        save_btn.click()
        time.sleep(1)
        try:
            driver.find_element_by_class_name('success')
            return 1
        except NoSuchElementException:
            return 0
    except NoSuchElementException:
        return 0
