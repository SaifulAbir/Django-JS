import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver
from .config import *

def addSkill(driver, data):
    try:
        driver.get(ADMIN_URL + SKILL_URL)
        add_skill = driver.find_element_by_class_name('addlink')
        add_skill.click()
        if not pd.isna(data['_name']):
            skill_name = driver.find_element_by_name('name')
            skill_name.send_keys(data['_name'])

        skill_date = driver.find_element_by_name('created_date_0')
        skill_date.clear()
        if not pd.isna(data['_date']):
            skill_date.send_keys(data['_date'])
            time.sleep(1)

        skill_time = driver.find_element_by_name('created_date_1')
        skill_time.clear()
        if not pd.isna(data['_time']):
            skill_time.send_keys(data['_time'])
            time.sleep(1)

        save_button = driver.find_element_by_name('_save')
        save_button.click()
        time.sleep(DELAY_SHORT)
        # check that saved
        driver.find_element_by_class_name('success')
        return 1
    except Exception as ex:
        return 0

# def deleteSkill(driver: WebDriver, data):
#     driver.get(ADMIN_URL + DIVISION_URL)
#     try:
#         delete = driver.find_element_by_class_name('js-delete-division').click()
#         deleteConfirm = driver.find_element_by_class_name('btn-danger').click()
#         deleteDs = driver.find_element_by_class_name('js-delete-district').click()
#         deleteDsConfirm = driver.find_element_by_class_name('btn-danger').click()
#         deleteUp = driver.find_element_by_class_name('js-delete-upazilla').click()
#         deleteUpConfirm = driver.find_element_by_class_name('btn-danger').click()
#         deleteUn = driver.find_element_by_class_name('js-delete-union').click()
#         deleteUnConfirm = driver.find_element_by_class_name('btn-danger').click()
#
#         return 1
#     except Exception as ex:
#         return 0