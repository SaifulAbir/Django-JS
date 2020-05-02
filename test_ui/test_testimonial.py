import os
import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *


def addTestimonial(driver: webdriver.Chrome, data):
    addTestimonial = driver.find_element_by_class_name('addlink')
    addTestimonial.click()
    time.sleep(1)
    try:
        client_name = driver.find_element_by_name('client_name')
        client_name.clear()
        if not pd.isna(data['_client_name']):
            client_name.send_keys(data['_client_name'])
            time.sleep(1)

        comment = driver.find_element_by_name('comment')
        comment.clear()
        if not pd.isna(data['_comment']):
            comment.send_keys(data['_comment'])
            time.sleep(1)

        profile_picture = driver.find_element_by_name('profile_picture')
        profile_picture.clear()
        if not pd.isna(data['_image_path']):
            profile_picture.send_keys(data['_image_path'])
            time.sleep(1)

        qtype_save = driver.find_element_by_name('_save')
        qtype_save.submit()
        time.sleep(1)
        driver.find_element_by_class_name('success')
        return 1
    except NoSuchElementException:
        return 0
