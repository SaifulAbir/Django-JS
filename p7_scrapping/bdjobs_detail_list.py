# -*- coding: utf-8 -*-

"""
Crawl IT jobs from bdjobs.com
"""

import requests
from bs4 import BeautifulSoup
import csv
import time, datetime

job_links = []
now = datetime.datetime.now()
current_date = now.strftime("%b %-1d, %Y")
unknown_company = "Unknown"
UNKNOWN_VACANCY = 9999
last_scrapping_date = '2020-01-01 00:00:00.000000'
scrapping_status = True
main_site = 'http://127.0.0.1:8000/'
bdjobs = 'http://jobs.bdjobs.com/'
# Job search url
url = f'{bdjobs}/jobsearch.asp?fcatId=8'

COMPANY_LIST_API = main_site+'company/'
JOB_LIST_API = main_site+'api/job_create/'
JOB_LIST_API_KEY = '96d56aceeb9049debeab628ac760aa11'
API_HEADER = {'api-key': JOB_LIST_API_KEY}

# Post data 'dictionary' for different crieteria.
# 'fcat' for 'Job Category'
# 'pg' for 'Pagination'. Value is 1 by default.
# Other keys are not being used
bdjobs_post_data = {'Country': '0',
             'MPostings': '',
             'Newspaper': '0',
             'fcat': '8',
             'hidJobSearch': 'JobSearch',
             'hidOrder': '',
             'iCat': '0',
             'pg': '1',
             'qAge': '0',
             'qDeadline': '0',
             'qExp': '0',
             'qJobLevel': '0',
             'qJobNature': '0',
             'qJobSpecialSkill': '-1',
             'qOT': '0',
             'qPosted': '0',
             'txtsearch': '',
             'ver': ''
             }


def main():
    global scrapping_status
    page_no = 1 # At least 1 page should be available
    max_page_no = 10

    total_jobs = 0  # Total jobs counting
    s = requests.Session() 
    while page_no <= max_page_no:
        print('Page No : {0}'.format(page_no))
        bdjobs_post_data['pg'] = page_no # Assign new page no.
        resp = s.post(url, bdjobs_post_data)

        html = BeautifulSoup(resp.content, 'html.parser')
        data = html.find_all('div', {'class': ['sout-jobs-wrapper','norm-jobs-wrapper']})

        if page_no == 1:
            max_page_no = html.find('div', {'id': 'topPagging'}).find_all('li')[-1].text.strip().replace('.', '')
            max_page_no = int(max_page_no)

        for dt in data:
            # A dictionary to pass data to function
            data_dict = {}

            # Fetching desired content using its tag and class
            try:
                title = dt.find('div', {'class': 'job-title-text'})
            except Exception as ex:
                title = "JOB TITLE"

            try:
                data_dict['web_address'] = bdjobs + title.find('a', {'href': True})['href']
            except Exception as ex:
                data_dict['web_address'] = "JOB LINK"

            try:
                data_dict['title'] = title.text.strip()
            except Exception as ex:
                data_dict['title'] = "JOB TITLE TEXT"

            try:
                data_dict['company_name_id'] = dt.find('div', {'class': 'comp-name-text'}).text.strip()
                response = requests.get(COMPANY_LIST_API, json=data_dict, headers=API_HEADER)
                josnResponse = response.json()

                companyName = unknown_company
                for company in josnResponse:
                    if company['name'] == data_dict['company_name_id']:
                        companyName = companyName['name']
                data_dict['company_name_id'] = companyName

            except Exception as ex:
                data_dict['company'] = unknown_company

            try:
                data_dict['application_deadline'] = dt.find('div', {'class': 'dead-text-d'}).text.strip()
                datetimeobject = datetime.datetime.strptime(data_dict['application_deadline'], "%b %d, %Y")
                data_dict['application_deadline'] = datetimeobject.strftime('%Y-%m-%d')
            except Exception as ex:
                data_dict['deadline'] = "DEADLINE"


            try:
                data_dict['education'] = dt.find('div', {'class': 'edu-text-d'}).text.strip()
            except Exception as ex:
                data_dict['education'] = "EDUCATION"

            # try:
            #     data_dict['experience'] = dt.find('div', {'class': 'exp-text-d'}).text.strip()
            # except Exception as ex:
            #     data_dict['experience'] = "EXPERIENCE"

            try:
                resp_detail = s.post(bdjobs + title.find('a', {'href': True})['href'])
                html_detail = BeautifulSoup(resp_detail.content, 'html.parser')
                data_detail = html_detail.find('div', {'class': 'job-preview'})
                try:
                    data_dict['raw_content'] = data_detail.text
                except Exception as ex:
                    data_dict['raw_content'] = ""


                try:
                    published_date = data_detail.find('div', {'class': 'panel-body'}).findNext('h4').text.strip().replace(u'\xa0',u'').replace(u'Published on:',u'')
                    datetimeobject = datetime.datetime.strptime(published_date, "%b %d, %Y")
                    data_dict['created_date'] = datetimeobject.strftime('%Y-%m-%d') + " 00:00:00.000000"
                except Exception as ex:
                    data_dict['created_date'] = "Error"


                try:
                    data_dict['vacancy'] = data_detail.find(text="Vacancy").findNext('p').text.strip()

                    if data_dict['vacancy'] == 'Not specific':
                        data_dict['vacancy'] = UNKNOWN_VACANCY
                except Exception as ex:
                    data_dict['no_of_vacancy'] = "Error"

                # try:
                #     data_dict['employment_status'] = data_detail.find('div', {'class': 'job_nat'}).findNext('p').text.strip()
                # except Exception as ex:
                #     data_dict['employment_status'] = "Error"

                try:
                    data_dict['job_location'] = data_detail.find(text="Job Location").findNext('p').text.strip()
                except Exception as ex:
                    data_dict['job_location'] = "Error"

                # try:
                #     data_dict['salary'] = data_detail.find(text="Salary").findNext('ul').text.strip()
                # except Exception as ex:
                #     data_dict['salary'] = "Error"

                try:
                    data_dict['responsibilities'] = data_detail.find('div', {'class': 'job_des'}).text
                except Exception as ex:
                    data_dict['responsibilities'] = "Error"
                

                # try:
                #     data_dict['educational_requirements'] = [x.text for x in data_detail.find('div', {'class': 'edu_req'}).find_all('li')]
                #     # data_detail.find('div',{'class': 'edu_req'}).text.strip()
                # except Exception as ex:
                #     data_dict['educational_requirements'] = "Error"

                # try:
                #     data_dict['job_requirements'] = [x.text for x in data_detail.find('div', {'class': 'job_req'}).find_all('li')]
                #     # data_detail.find('div', {'class': 'job_req'}).text.strip()
                # except Exception as ex:
                #     data_dict['job_requirements'] = "Error"


                try:
                    data_dict['other_benefits'] = [x.text for x in data_detail.find('div', {'class': 'oth_ben'}).find_all('li')]
                except Exception as ex:
                    data_dict['other_benefits'] = "Error"

            except Exception as ex:
                print("Detail Data error")


            if data_dict['created_date'] == last_scrapping_date:
                scrapping_status = False
                break
            
            if data_dict['web_address'] in job_links:
                continue

            job_links.append(data_dict['web_address'])
            response = requests.post(JOB_LIST_API,json=data_dict, headers=API_HEADER)

            # Increment of total_jobs
            total_jobs += 1

            print(f"{total_jobs}: {data_dict['title']}")
            print(response.status_code)

        # Increment page no.
        page_no += 1
        if scrapping_status == False:
            break


    print('Successfully completed!')

    # Total jobs
    print('Total Job : {0}'.format(total_jobs))

if __name__ == "__main__":
    main()