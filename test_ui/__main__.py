import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from .config import *
from .test_login import login


def main():
    driver = webdriver.Chrome(CHROME_DRIVER_LOCATION)
    driver.get(MAIN_URL)
    time.sleep(DELAY_LONG)
    # login
    data = pd.read_csv("test_ui/data/login.csv", dtype=str)
    for idx, row in data.iterrows():
        result = login(driver, row)
        if result == 0:
            print("Login failed")
            return
    #
    # # Division data
    # data = pd.read_csv("test_ui/data/division.csv", dtype=str)
    # for idx, row in data.iterrows():
    #     addDivision(driver, row)
    #
    # # District data
    # data = pd.read_csv("test_ui/data/district.csv", dtype=str)
    # for idx, row in data.iterrows():
    #     addDistrict(driver, row)
    #
    #
    # # Upazilla data
    # data = pd.read_csv("test_ui/data/upazilla.csv", dtype=str)
    # for idx, row in data.iterrows():
    #     addUpazilla(driver, row)

    # # # Union data
    # data = pd.read_csv("test_ui/data/union.csv", dtype=str)
    # for idx, row in data.iterrows():
    #     addUnion(driver, row)

    #
    #  # School data
    # data = pd.read_csv("test_ui/data/school.csv", dtype=str)
    # for idx, row in data.iterrows():
    #     addSchool(driver, row)

    # # # Headmaster data
    # data = pd.read_csv("test_ui/data/headmaster.csv", dtype=str)
    # for idx, row in data.iterrows():
    #     addHeadmaster(driver, row)

    # #Skleader data
    # data = pd.read_csv("test_ui/data/skleader.csv", dtype=str)
    # for idx, row in data.iterrows():
    #     try:
    #         addSkleaderEntry(driver, row)
    #     except WebDriverException:
    #         print("ERROR: ", row)

    # #Skmember data
    # data = pd.read_csv("test_ui/data/skmember.csv", dtype=str)
    # for idx, row in data.iterrows():
    #     try:
    #         addSkmemberEntry(driver, row)
    #     except WebDriverException:
    #         print("ERROR: ", row)

    driver.quit()


if __name__ == "__main__":
    main()
