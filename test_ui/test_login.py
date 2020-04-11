import os
import time

from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from .config import *
from selenium.webdriver.ie.webdriver import WebDriver


def login(driver: WebDriver, data):
    menu = driver.find_element_by_class_name('navbar-toggler-icon').click()
    driver.get('http://127.0.0.1/professional/sign-in/')

    try:

        sign_in = driver.find_element_by_id("sign-in")
        sign_in.click()
        name = driver.find_element_by_name("email")
        name.clear()
        name.send_keys(data['_email'])
        password = driver.find_element_by_name("password")
        password.clear()
        password.send_keys(data['_password'])
        submit_button = driver.find_element_by_xpath('//*[@id="sign-in"]/button')
        submit_button.click()
        time.sleep(DELAY_SHORT)
        try:
            menu = driver.find_element_by_class_name('navbar-toggler-icon').click()
            driver.find_element_by_xpath('//*[@id="sign-out"]/a')
            return 1
        except NoSuchElementException:
            return 0
    except NoSuchElementException:
        return 1

def adminLogin(driver: WebDriver, data):
    driver.get(ADMIN_URL)

    try:

        name = driver.find_element_by_id("id_username")
        name.clear()
        name.send_keys(data['_email'])
        password = driver.find_element_by_id("id_password")
        password.clear()
        password.send_keys(data['_password'])
        submit_button = driver.find_element_by_xpath('//*[@id="login-form"]/div[3]/input')
        submit_button.click()
        time.sleep(DELAY_SHORT)
        try:
            driver.find_element_by_xpath('//*[@id="user-tools"]/a[3]')
            return 1
        except NoSuchElementException:
            return 0
    except NoSuchElementException:
        return 1

def logout(driver):
    sign_out = driver.find_element_by_id('sign-out')
    sign_out.click()
    time.sleep(DELAY_SHORT)

def adminLogout(driver):
    sign_out = driver.find_element_by_xpath('//*[@id="user-tools"]/a[3]')
    sign_out.click()
    time.sleep(DELAY_SHORT)

def updateProfile(driver: WebDriver, data):
    profile_name = driver.find_element_by_class_name('dropdown-toggle')
    profile_name.click()
    driver.find_element_by_link_text('Profile').click()
    time.sleep(DELAY_SHORT)
    driver.find_element_by_link_text('Edit Profile').click()
    time.sleep(DELAY_SHORT)
    try:
        if not pd.isna(data['_name']):
            try:
                profile_name = driver.find_element_by_name('PF-first_name')
            except:
                profile_name = driver.find_element_by_name('first_name')
            profile_name.clear()
            profile_name.send_keys(data['_name'])
            time.sleep(1)
        if not pd.isna(data['_email']):
            try:
                profile_email = driver.find_element_by_name('PF-email')
            except:
                profile_email = driver.find_element_by_name('email')
            profile_email.clear()
            profile_email.send_keys(data['_email'])
            time.sleep(1)
        if not pd.isna(data['_password']):
            try:
                profile_password = driver.find_element_by_name('PF-password')
            except:
                profile_password = driver.find_element_by_name('password')
            profile_password.clear()
            profile_password.send_keys(data['_password'])
            time.sleep(1)
        if not pd.isna(data['_con_password']):
            try:
                profile_con_password = driver.find_element_by_name('PF-confirm_password')
            except:
                profile_con_password = driver.find_element_by_name('confirm_password')
            profile_con_password.clear()
            profile_con_password.send_keys(data['_con_password'])
            time.sleep(1)
        #
        # profile_image = driver.find_element_by_id('id_PF-image').click()
        # time.sleep(1)
        # profile_image.send_keys("/images/profile.jpg")
        # time.sleep(1)

        save_button = driver.find_element_by_id('save-btn')
        save_button.click()
        time.sleep(DELAY_LONG)
        driver.find_element_by_link_text('Edit Profile')
        return 1
    except Exception as ex:
        return 0
