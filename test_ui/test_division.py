import time

from selenium.webdriver.chrome.webdriver import WebDriver

from .config import *


def addDivision(driver, data):
    try:
        driver.get(ADMIN_URL + DIVISION_URL)
        add_division = driver.find_element_by_class_name('addlink')
        add_division.click()
        time.sleep(DELAY_SHORT)
        division_name = driver.find_element_by_name('name')
        division_name.send_keys(data['_division'])
        save_button = driver.find_element_by_name('_save')
        save_button.click()
        time.sleep(DELAY_SHORT)
        # check that saved
        driver.find_element_by_class_name('success')
        return 1
    except Exception as ex:
        return 0


def deleteDivision(driver: WebDriver, data):
    driver.get(ADMIN_URL + DIVISION_URL)
    try:
        delete = driver.find_element_by_class_name('js-delete-division').click()
        deleteConfirm = driver.find_element_by_class_name('btn-danger').click()
        deleteDs = driver.find_element_by_class_name('js-delete-district').click()
        deleteDsConfirm = driver.find_element_by_class_name('btn-danger').click()
        deleteUp = driver.find_element_by_class_name('js-delete-upazilla').click()
        deleteUpConfirm = driver.find_element_by_class_name('btn-danger').click()
        deleteUn = driver.find_element_by_class_name('js-delete-union').click()
        deleteUnConfirm = driver.find_element_by_class_name('btn-danger').click()

        return 1
    except Exception as ex:
        return 0