import time
import unittest
import pandas as pd

from selenium import webdriver

from test_ui.public_ui.test_home import *
from test_ui.public_ui.test_sign_up import *
from test_ui.public_ui.test_login import *
from .config import *



class TestUI(unittest.TestCase):

    # def setUpClass():
    #     print("Data Entry started ..")
    #     TestUI.dataEntry()
    #

    def setUp(self):
        print("Setup function is running")
        self.driver = webdriver.Chrome(CHROME_DRIVER_LOCATION)
        self.driver.get(MAIN_URL)
        self.driver.maximize_window()
        time.sleep(DELAY_SHORT)

    def dataEntry():
        driver = webdriver.Chrome(CHROME_DRIVER_LOCATION)
        adminLogin(driver, {'_email': 'admin', '_password': '@dmin123#', 'name': 'admin'})


    def testPublicHome(self):
        # adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/data/data_public_home.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(MAIN_URL)
            actual = publicHome(self.driver, row)
        #     try:
        #         self.assertEqual(row['expected_result'], str(actual))
        #         print(row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
        #     except Exception as ex:
        #         print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row['test_description'])
        #         f = f + 1
        # if f != 0:
        #     raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        # else:
        #     print("All passed")


if __name__ == '__main__':
    unittest.main()
