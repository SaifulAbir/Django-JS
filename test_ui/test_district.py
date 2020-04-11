import time

from .config import *


def addDistrict(driver, data):
    try:
        driver.get(ADMIN_URL + DISTRICT_URL)
        add_district = driver.find_element_by_class_name('addlink')
        add_district.click()
        time.sleep(DELAY_SHORT)
        division_name = driver.find_element_by_name('division')
        division_name.send_keys(data['_division'])
        district_name = driver.find_element_by_name('name')
        district_name.send_keys(data['_district'])
        save_button = driver.find_element_by_name('_save')
        save_button.click()
        time.sleep(DELAY_SHORT)
        # check that saved
        driver.find_element_by_class_name('success')
        return 1
    except Exception as ex:
        return 0