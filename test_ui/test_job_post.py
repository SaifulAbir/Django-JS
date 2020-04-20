import time
from datetime import date
import ast
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.select import Select

from .config import *


def addJobHome(driver: WebDriver, data):

    try:
        job_post = driver.find_element_by_link_text('Post a Job')
        job_post.click()

        if not pd.isna(data['_job_title']):
            job_title = driver.find_element_by_id('title')
            job_title.send_keys(data['_job_title'])
        time.sleep(1)
        if not pd.isna(data['_job_title']):
            company_name = driver.find_element_by_id('industry')
            company_name.send_keys('IT & Telecommunication')
            time.sleep(1)
        if not pd.isna(data['_job_location']):
            job_location = driver.find_element_by_id('job_location')
            job_location.send_keys(data['_job_location'])
        time.sleep(1)
        if not pd.isna(data['_employment_status']):
            employment_status = driver.find_element_by_id('employment_status')
            employment_status.send_keys('Full Time')
        time.sleep(1)
        if not pd.isna(data['_experience']):
            experience = driver.find_element_by_id('experience')
            experience.send_keys('1 Year')
        time.sleep(1)

        if not pd.isna(data['_salary']):
            salary = driver.find_element_by_id('salary')
            if data['_salary'] != "Negotiable":
                salary.send_keys(data['_salary'])
            elif data['_salary'] != "Salary Range":
                salary.send_keys(data['_salary'])

                if not pd.isna(data['_currency']):
                    currency = driver.find_element_by_id('currency')
                    currency.send_keys(data['_currency'])
                time.sleep(1)

                if not pd.isna(data['_salary_min']):
                    salary_min = driver.find_element_by_id('salary_min')
                    if data['_salary_min'] >= "5000":
                        salary_min.send_keys(data['_salary_min'])
                    else:
                        salary_min.send_keys('5000')
                time.sleep(1)
                if not pd.isna(data['_salary_max']):
                    salary_max = driver.find_element_by_id('salary_max')
                    if data['_salary_max'] <= "500000":
                        salary_max.send_keys(data['_salary_max'])
                    else:
                        salary_max.send_keys('500000')

        time.sleep(1)
        if not pd.isna(data['_job_title']):
            gender = driver.find_element_by_id('gender')
            gender.send_keys('Male')
        time.sleep(1)
        if not pd.isna(data['_qualification']):
            qualification = driver.find_element_by_id('qualification')
            qualification.send_keys('Graduate / Fazil')
        time.sleep(1)
        if not pd.isna(data['_deadline']):
            deadline = driver.find_element_by_id('application_deadline')
            deadline.send_keys('04/13/2020')
        time.sleep(1)

        if not pd.isna(data['_vacancy']):
            deadline = driver.find_element_by_id('application_deadline')
            deadline.send_keys('04/13/2020')
        time.sleep(1)

        if not pd.isna(data['_job_descriptions']):
            bullet = driver.find_element_by_xpath('//*[@id="mceu_3"]/button[1]/i')
            bullet.click()
            driver.switch_to.frame(driver.find_element_by_id("descriptions_ifr"))
            job_requirment = driver.find_element_by_class_name('mce-content-body')
            requirment = data['_job_descriptions']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
            # for i in range(len(requirment)):
                job_requirment.send_keys(i)
                if count < size:
                    job_requirment.send_keys('\n')
                count = count+1
            driver.switch_to.default_content()
        time.sleep(1)

        if not pd.isna(data['_job_responsibilities']):
            bullet = driver.find_element_by_xpath('//*[@id="mceu_23"]/button[1]/i')
            bullet.click()
            driver.switch_to.frame(driver.find_element_by_id("responsibilities_ifr"))
            job_responsibilities = driver.find_element_by_class_name('mce-content-body')
            requirment = data['_job_responsibilities']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
            # for i in range(len(requirment)):
                job_responsibilities.send_keys(i)
                if count < size:
                    job_responsibilities.send_keys('\n')
                count = count+1
            driver.switch_to.default_content()
        time.sleep(1)


        if not pd.isna(data['_education']):
            bullet = driver.find_element_by_xpath('//*[@id="mceu_35"]/button[1]/i')
            bullet.click()
            driver.switch_to.frame(driver.find_element_by_id("education_ifr"))
            educational_requirment = driver.find_element_by_class_name('mce-content-body')
            requirment = data['_education']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
            # for i in range(len(requirment)):
                educational_requirment.send_keys(i)
                if count < size:
                    educational_requirment.send_keys('\n')
                count = count+1
            driver.switch_to.default_content()
        time.sleep(1)


        if not pd.isna(data['_other_benefits']):
            bullet = driver.find_element_by_xpath('//*[@id="mceu_47"]/button[1]/i')
            bullet.click()
            driver.switch_to.frame(driver.find_element_by_id("other_benefits_ifr"))
            other_benefit = driver.find_element_by_class_name('mce-content-body')
            requirment = data['_other_benefits']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
            # for i in range(len(requirment)):
                other_benefit.send_keys(i)
                if count < size:
                    other_benefit.send_keys('\n')
                count = count+1
            driver.switch_to.default_content()
        time.sleep(1)



        if not pd.isna(data['_division']):
            division = driver.find_element_by_id('division')
            division.send_keys(data['_division'])
        time.sleep(1)
        if not pd.isna(data['_district']):
            district = driver.find_element_by_id('district')
            district.send_keys(data['_district'])
        time.sleep(1)
        if not pd.isna(data['_job_title']):
            zipcode = driver.find_element_by_id('zipcode')
            zipcode.send_keys('1100')
        time.sleep(1)
        if not pd.isna(data['_company_location']):
            company_location = driver.find_element_by_id('company_location')
            company_location.send_keys(data['_company_location'])
        if not pd.isna(data['_company_name']):
            company = driver.find_element_by_id('company')
            company.send_keys(data['_company_name'])
            # company.send_keys('2RA Technology Limited')
        if not pd.isna(data['_web_address']):
            web_address = driver.find_element_by_id('web_address')
            web_address.send_keys(data['_web_address'])
        time.sleep(1)
        if not pd.isna(data['_company_profile']):
            company_profile = driver.find_element_by_id('company_profile')
            company_profile.send_keys(data['_company_profile'])
        time.sleep(1)
        if not pd.isna(data['_job_title']):
            dot = driver.find_element_by_class_name('dot')
            dot.click()
        time.sleep(1)
        save_button = driver.find_element_by_xpath('//*[@id="job-post-form"]/div/div[10]/div/button')
        save_button.click()
        time.sleep(2)
        driver.find_element_by_css_selector('div[class="alert alert-success-customized"')
        return 1
    except Exception as ex:
        return 0

def addJobDetailHome(driver: WebDriver, data):

    try:
        job_post = driver.find_element_by_link_text('Post a Job')
        job_post.click()

        if not pd.isna(data['_job_title']):
            job_title = driver.find_element_by_id('title')
            job_title.send_keys(data['_job_title'])
        time.sleep(1)
        if not pd.isna(data['_job_title']):
            company_name = driver.find_element_by_id('industry')
            company_name.send_keys('IT & Telecommunication')
            time.sleep(1)
        if not pd.isna(data['_job_location']):
            job_location = driver.find_element_by_id('job_location')
            job_location.send_keys(data['_job_location'])
        time.sleep(1)
        if not pd.isna(data['_employment_status']):
            employment_status = driver.find_element_by_id('employment_status')
            employment_status.send_keys('Full Time')
        time.sleep(1)
        if not pd.isna(data['_experience']):
            experience = driver.find_element_by_id('experience')
            experience.send_keys('1 Year')
        time.sleep(1)

        if not pd.isna(data['_salary']):
            salary = driver.find_element_by_id('salary')
            if data['_salary'] != "Negotiable":
                salary.send_keys(data['_salary'])
            elif data['_salary'] != "Salary Range":
                salary.send_keys(data['_salary'])

                if not pd.isna(data['_currency']):
                    currency = driver.find_element_by_id('currency')
                    currency.send_keys(data['_currency'])
                time.sleep(1)

                if not pd.isna(data['_salary_min']):
                    salary_min = driver.find_element_by_id('salary_min')
                    if data['_salary_min'] >= "5000":
                        salary_min.send_keys(data['_salary_min'])
                    else:
                        salary_min.send_keys('5000')
                time.sleep(1)
                if not pd.isna(data['_salary_max']):
                    salary_max = driver.find_element_by_id('salary_max')
                    if data['_salary_max'] <= "500000":
                        salary_max.send_keys(data['_salary_max'])
                    else:
                        salary_max.send_keys('500000')

        time.sleep(1)
        if not pd.isna(data['_job_title']):
            gender = driver.find_element_by_id('gender')
            gender.send_keys('Male')
        time.sleep(1)
        if not pd.isna(data['_qualification']):
            qualification = driver.find_element_by_id('qualification')
            qualification.send_keys('Graduate / Fazil')
        time.sleep(1)
        if not pd.isna(data['_deadline']):
            deadline = driver.find_element_by_id('application_deadline')
            deadline.send_keys('04/13/2020')
        time.sleep(1)

        if not pd.isna(data['_vacancy']):
            deadline = driver.find_element_by_id('application_deadline')
            deadline.send_keys('04/13/2020')
        time.sleep(1)

        if not pd.isna(data['_job_descriptions']):
            bullet = driver.find_element_by_xpath('//*[@id="mceu_3"]/button[1]/i')
            bullet.click()
            driver.switch_to.frame(driver.find_element_by_id("descriptions_ifr"))
            job_requirment = driver.find_element_by_class_name('mce-content-body')
            requirment = data['_job_descriptions']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
            # for i in range(len(requirment)):
                job_requirment.send_keys(i)
                if count < size:
                    job_requirment.send_keys('\n')
                count = count+1
            driver.switch_to.default_content()
        time.sleep(1)

        if not pd.isna(data['_job_responsibilities']):
            bullet = driver.find_element_by_xpath('//*[@id="mceu_23"]/button[1]/i')
            bullet.click()
            driver.switch_to.frame(driver.find_element_by_id("responsibilities_ifr"))
            job_responsibilities = driver.find_element_by_class_name('mce-content-body')
            requirment = data['_job_responsibilities']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
            # for i in range(len(requirment)):
                job_responsibilities.send_keys(i)
                if count < size:
                    job_responsibilities.send_keys('\n')
                count = count+1
            driver.switch_to.default_content()
        time.sleep(1)

        if not pd.isna(data['_education']):
            bullet = driver.find_element_by_xpath('//*[@id="mceu_35"]/button[1]/i')
            bullet.click()
            driver.switch_to.frame(driver.find_element_by_id("education_ifr"))
            educational_requirment = driver.find_element_by_class_name('mce-content-body')
            requirment = data['_education']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
            # for i in range(len(requirment)):
                educational_requirment.send_keys(i)
                if count < size:
                    educational_requirment.send_keys('\n')
                count = count+1
            driver.switch_to.default_content()
        time.sleep(1)


        if not pd.isna(data['_other_benefits']):
            bullet = driver.find_element_by_xpath('//*[@id="mceu_47"]/button[1]/i')
            bullet.click()
            driver.switch_to.frame(driver.find_element_by_id("other_benefits_ifr"))
            other_benefit = driver.find_element_by_class_name('mce-content-body')
            requirment = data['_other_benefits']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
            # for i in range(len(requirment)):
                other_benefit.send_keys(i)
                if count < size:
                    other_benefit.send_keys('\n')
                count = count+1
            driver.switch_to.default_content()
        time.sleep(1)

        if not pd.isna(data['_division']):
            division = driver.find_element_by_id('division')
            division.send_keys(data['_division'])
        time.sleep(1)
        if not pd.isna(data['_district']):
            district = driver.find_element_by_id('district')
            district.send_keys(data['_district'])
        time.sleep(1)
        if not pd.isna(data['_job_title']):
            zipcode = driver.find_element_by_id('zipcode')
            zipcode.send_keys('1100')
        time.sleep(1)
        if not pd.isna(data['_company_location']):
            company_location = driver.find_element_by_id('company_location')
            company_location.send_keys(data['_company_location'])
        if not pd.isna(data['_company_name']):
            company = driver.find_element_by_id('company')
            company.send_keys(data['_company_name'])
            # company.send_keys('2RA Technology Limited')
        if not pd.isna(data['_web_address']):
            web_address = driver.find_element_by_id('web_address')
            web_address.send_keys(data['_web_address'])
        time.sleep(1)
        if not pd.isna(data['_company_profile']):
            company_profile = driver.find_element_by_id('company_profile')
            company_profile.send_keys(data['_company_profile'])
        time.sleep(1)
        if not pd.isna(data['_job_title']):
            dot = driver.find_element_by_class_name('dot')
            dot.click()
        time.sleep(1)
        save_button = driver.find_element_by_xpath('//*[@id="job-post-form"]/div/div[10]/div/button')
        save_button.click()
        time.sleep(2)
        driver.find_element_by_css_selector('div[class="alert alert-success-customized"')
        return 1
    except Exception as ex:
        return 0


def addJobAdmin(driver: WebDriver, data):
    driver.get('http://127.0.0.1/admin/job/job/add/')
    try:
        if not pd.isna(data['_job_title']):
            job_title = driver.find_element_by_name('title')
            job_title.send_keys(data['_job_title'])
        time.sleep(1)

        if not pd.isna(data['_job_title']):
            company_name = driver.find_element_by_name('industry')
            company_name.send_keys('IT & Telecommunication')
            time.sleep(1)

        if not pd.isna(data['_employment_status']):
            employment_status = driver.find_element_by_name('employment_status')
            employment_status.send_keys('Full Time')
        time.sleep(1)

        if not pd.isna(data['_job_location']):
            job_location = driver.find_element_by_name('job_location')
            job_location.send_keys(data['_job_location'])
        time.sleep(1)

        if not pd.isna(data['_experience']):
            experience = driver.find_element_by_name('experience')
            experience.send_keys('1 Year')
        time.sleep(1)

        if not pd.isna(data['_salary']):
            salary_min = driver.find_element_by_name('salary_min')
            if data['_salary'] != "Negotiable":
                salary_min.send_keys(data['_salary'])
            else:
                salary_min.send_keys('5000')
        time.sleep(1)

        if not pd.isna(data['_salary']):
            salary_max = driver.find_element_by_name('salary_max')
            if data['_salary'] != "Negotiable":
                salary_max.send_keys(data['_salary'])
            else:
                salary_max.send_keys('10000')

        time.sleep(1)

        if not pd.isna(data['_educational_requirment']):
            qualification = driver.find_element_by_name('qualification')
            qualification.send_keys('Graduate / Fazil')
        time.sleep(1)

        if not pd.isna(data['_job_title']):
            gender = driver.find_element_by_name('gender')
            gender.send_keys('Male')
        time.sleep(1)

        if not pd.isna(data['_deadline']):
            deadline = driver.find_element_by_name('application_deadline')
            deadline.send_keys('02/13/2020')
        time.sleep(1)

        if not pd.isna(data['_job_requirment']):
            job_description = driver.find_element_by_name('descriptions')
            requirment = data['_job_requirment']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
                job_description.send_keys(i)
                if count < size:
                    job_description.send_keys('\n')
                count = count+1
        time.sleep(1)

        if not pd.isna(data['_job_responsibilities']):
            job_responsibilities = driver.find_element_by_name('responsibilities')
            requirment = data['_job_responsibilities']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
            # for i in range(len(requirment)):
                job_responsibilities.send_keys(i)
                if count < size:
                    job_responsibilities.send_keys('\n')
                count = count+1
        time.sleep(1)


        if not pd.isna(data['_educational_requirment']):
            educational_requirment = driver.find_element_by_name('education')
            requirment = data['_educational_requirment']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
            # for i in range(len(requirment)):
                educational_requirment.send_keys(i)
                if count < size:
                    educational_requirment.send_keys('\n')
                count = count+1
        time.sleep(1)


        if not pd.isna(data['_other_benefit']):
            other_benefit = driver.find_element_by_name('other_benefits')
            requirment = data['_other_benefit']
            requirment = requirment.replace('\\r', '').replace('\\', '')
            requirment = ast.literal_eval(requirment)
            count = 1
            size = len(requirment)
            for i in requirment:
                other_benefit.send_keys(i)
                if count < size:
                    other_benefit.send_keys('\n')
                count = count+1
        time.sleep(1)

        if not pd.isna(data['_company_name']):
            company = driver.find_element_by_name('company_name')
            company.send_keys(data['_company_name'])
        time.sleep(1)

        if not pd.isna(data['_job_title']):
            division = driver.find_element_by_name('division')
            division.send_keys('Dhaka')
        time.sleep(1)
        if not pd.isna(data['_job_title']):
            district = driver.find_element_by_name('district')
            district.send_keys('Gazipur')
        time.sleep(1)
        if not pd.isna(data['_job_title']):
            zipcode = driver.find_element_by_name('zipcode')
            zipcode.send_keys('1100')
        time.sleep(1)
        if not pd.isna(data['_job_title']):
            company_location = driver.find_element_by_name('company_location')
            company_location.send_keys('Dhaka')

        if not pd.isna(data['_job_title']):
            company_profile = driver.find_element_by_name('company_profile')
            company_profile.send_keys('')
        time.sleep(1)

        if not pd.isna(data['_job_title']):
            latitude = driver.find_element_by_name('latitude')
            latitude.send_keys('1001')
        time.sleep(1)

        if not pd.isna(data['_job_title']):
            longitude = driver.find_element_by_name('longitude')
            longitude.send_keys('2002')
        time.sleep(1)

        if not pd.isna(data['_job_title']):
            web_address = driver.find_element_by_name('web_address')
            web_address.send_keys('')
        time.sleep(1)

        if not pd.isna(data['_job_title']):
            created_date = driver.find_element_by_name('created_date')
            created_date.clear()
            created_date.send_keys('24-02-2020')
        else:
            deadline = driver.find_element_by_xpath('//*[@id="job_form"]/div/fieldset/div[24]/div/span[1]/a[1]')
            deadline.click()
        time.sleep(1)

        save_btn = driver.find_element_by_name('_save')
        save_btn.click()
        time.sleep(10)
        try:
            driver.find_element_by_class_name('success')
            return 1
        except NoSuchElementException:
            return 0
    except NoSuchElementException:
        return 0
