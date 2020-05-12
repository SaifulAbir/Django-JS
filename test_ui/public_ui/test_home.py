import time
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from selenium import webdriver
from .config import *

def publicHome(driver: webdriver.Chrome, data):
    driver.maximize_window()
    welcome = driver.find_element_by_name('keyword')
    welcome.send_keys('I am in TOp Section ')
    try:
        page_title = driver.title
        print(page_title)
        logo = driver.find_element_by_class_name('img-fluid').get_attribute('src')
        print(logo)

        main_nav = driver.find_element_by_class_name('main-nav')
        buttons = main_nav.find_elements_by_tag_name("li")
        for button in buttons:
            text = button.text
            print(text)
        main_facebook_url = driver.find_element_by_class_name('facebook-url').get_attribute('href')
        main_linkedin_url = driver.find_element_by_class_name('linkedin-url').get_attribute('href')
        main_twitter_url = driver.find_element_by_class_name('twitter-url').get_attribute('href')
        print(main_facebook_url + '\n' + main_linkedin_url + '\n' + main_twitter_url + '\n\n')

        main_facebook_src = driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/div/li[6]/a[1]/i/img').get_attribute("src")
        main_linkedin_src = driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/div/li[6]/a[2]/i/img').get_attribute('src')
        main_twitter_src = driver.find_element_by_xpath('//*[@id="navbarSupportedContent"]/div/li[6]/a[3]/i/img').get_attribute('src')
        print(main_facebook_src + '\n' + main_linkedin_src + '\n' + main_twitter_src)

        page_title = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/h1')
        main_title = page_title.text
        print(main_title)

        page_sub_title = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/p')
        sub_title = page_sub_title.text
        print(sub_title)


        # qtype_save = driver.find_element_by_name('_save')
        # qtype_save.submit()
        # time.sleep(1)
        # driver.find_element_by_class_name('addlink')



        return 1
    except NoSuchElementException:
        return 0
