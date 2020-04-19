# -*- coding: utf-8 -*-

"""
Crawl IT jobs from bdjobs.com
"""

# Load necessary modules
import requests
from bs4 import BeautifulSoup
import csv
import time, datetime

now = datetime.datetime.now()
current_date = now.strftime("%b %-1d, %Y")


# Define a function to write into file
# Function starts from here
def write_csv_file(data):
    # 'global' keyword for using the variable initialized outside the function

    """job_title_text = data['job_title_text']
    company_name = data['company_name']
    education = data['education']
    experience = data['experience']
    deadline = data['deadline']
    job_link = data['job_link']"""

    # Writing into the csv file
    try:
        csv_writer.writerow(
            {'Published Date': data['published_date'],'Job Title': data['job_title_text'], 'Company Name': data['company_name'], 'Education': data['education'],
             'Experience': data['experience'], 'Deadline': data['deadline'], 'Vacancy': data_dict['no_of_vacancy'],
             'Job Responsibilities': data_dict['job_responsibilities'],
             'Employment Status': data_dict['employment_status'],
             'Educational Requirment': data_dict['educational_requirements'],
             'Job Requirment': data_dict['job_requirements'],
             'Job Location': data_dict['job_location'], 'Salary': data_dict['salary'],
             'Other Benefit': data_dict['other_benefit'], 'Job Link': data['job_link']})
    except:
        print('Exception occurred! No problem. Keep going.')


# Function ends here

# Open a csv file with 'write' mode
job_list_file_obj = open('bdjobs_detail_list.csv', 'w', newline='')

main_site = 'http://jobs.bdjobs.com/'

# Job search url
url = 'http://jobs.bdjobs.com/jobsearch.asp?fcatId=8'

# Post data 'dictionary' for different crieteria.
# 'fcat' for 'Job Category'
# 'pg' for 'Pagination'. Value is 1 by default.
# Other keys are not being used


post_data = {'Country': '0',
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
column_names = ['Published Date','Job Title', 'Company Name', 'Education', 'Experience', 'Deadline', 'Vacancy', 'Job Responsibilities', 'Employment Status', 'Educational Requirment', 'Job Requirment', 'Job Location', 'Salary', 'Other Benefit', 'Job Link']

# Creating csv writer
csv_writer = csv.DictWriter(job_list_file_obj, fieldnames=column_names)

# Write column name
csv_writer.writeheader()

csv_writer.writerow({'Published Date':'','Job Title': '', 'Company Name': '', 'Education': '', 'Experience': '', 'Deadline': '', 'Vacancy': '', 'Job Responsibilities': '', 'Employment Status': '', 'Educational Requirment': '', 'Job Requirment': '', 'Job Location': '', 'Salary': '', 'Other Benefit': '', 'Job Link': ''})

# At least 1 page should be available
page_no = 1
max_page_no = 4

# Total jobs counting
total_jobs = 0

while page_no <= max_page_no:
    print('Page No : {0}'.format(page_no))

    # Assign new page no.
    post_data['pg'] = page_no

    resp = requests.post(url)

    html = BeautifulSoup(resp.content, 'html.parser')

    data = html.find_all('div', {'class': 'norm-jobs-wrapper'})

    if page_no == 1:
        max_page_no = html.find('div', {'id': 'topPagging'}).find_all('li')[-1].text.strip().replace('.', '')
        max_page_no = int(max_page_no)

    for dt in data:
        # A dictionary to pass data to function
        data_dict = {};

        # Fetching desired content using its tag and class
        # done
        try:
            title = dt.find('div', {'class': 'job-title-text'})
        except Exception as ex:
            title = "JOB TITLE"
        # done
        try:
            data_dict['created_date'] = '2020-02-29 00:00:00.000000'
        except Exception as ex:
            data_dict['created_date'] = "2020-02-29 00:00:00.000000"
        try:
            data_dict['raw_content'] = '2020-02-29 00:00:00.000000'
        except Exception as ex:
            data_dict['raw_content'] = "2020-02-29 00:00:00.000000"

        try:
            data_dict['job_link'] = main_site + title.find('a', {'href': True})['href']
        except Exception as ex:
            data_dict['job_link'] = "JOB LINK"

        try:
            data_dict['job_title_text'] = title.text.strip()
        except Exception as ex:
            data_dict['job_title_text'] = "JOB TITLE TEXT"

        try:
            data_dict['company_name'] = dt.find('div', {'class': 'comp-name-text'}).text.strip()
        except Exception as ex:
            data_dict['company_name'] = "COMPANY NAME"
        try:
            data_dict['deadline'] = dt.find('div', {'class': 'dead-text-d'}).text.strip()
        except Exception as ex:
            data_dict['deadline'] = "DEADLINE"

# done
        try:
            data_dict['education'] = dt.find('div', {'class': 'edu-text-d'}).text.strip()
        except Exception as ex:
            data_dict['education'] = "EDUCATION"

        try:
            data_dict['experience'] = dt.find('div', {'class': 'exp-text-d'}).text.strip()
        except Exception as ex:
            data_dict['experience'] = "EXPERIENCE"

        try:

            resp_detail = requests.post(data_dict['job_link'])

            html_detail = BeautifulSoup(resp_detail.content, 'html.parser')
            # published_date = html_detail.find('div', class_='panel-body').h4
            # date = published_date.text.replace(u'\xa0', u'').replace(u'\n',u'').replace(u'\r', u'')
            # for e in date:
            #     print(date[e].replace('  ', ''))

            data_detail = html_detail.find('div', {'class': 'job-preview'})
            print(data_detail)
            data_dict_detail = {};

            try:
                data_dict['published_date'] = data_detail.find('div', {'class': 'panel-body'}).findNext('h4').text.strip().replace(u'\xa0',u'').replace(u'Published on:',u'')
                published_date = data_detail.find('div', {'class': 'panel-body'}).findNext('h4').text.strip().replace(u'\xa0',u'').replace(u'Published on:',u'')
            except Exception as ex:
                data_dict['published_date'] = "Error"

            try:
                data_dict['vacancy'] = data_detail.find(text="Vacancy").findNext('p').text.strip()
            except Exception as ex:
                data_dict['no_of_vacancy'] = "Error"
            try:
                # data_dict['employment_status'] = data_detail.find(text="Employment Status").findNext('p').text.strip()
                data_dict['employment_status'] = data_detail.find('div', {'class': 'job_nat'}).findNext('p').text.strip()
            except Exception as ex:
                data_dict['employment_status'] = "Error"

            try:
                data_dict['job_location'] = data_detail.find(text="Job Location").findNext('p').text.strip()
            except Exception as ex:
                data_dict['job_location'] = "Error"

            try:
                data_dict['salary'] = data_detail.find(text="Salary").findNext('ul').text.strip()
            except Exception as ex:
                data_dict['salary'] = "Error"

            try:
                data_dict['job_responsibilities'] = [x.text for x in data_detail.find('div', {'class': 'job_des'}).find_all('li')]
                # data_dict['job_responsibilities'] = data_detail.find(text="Job Responsibilities").findNext('ul').text.strip()
                # data_dict['job_responsibilities'] = data_detail.find('div', {'class': 'job_des'}), 'p'.text.strip()
            except Exception as ex:
                data_dict['job_responsibilities'] = "Error"


            try:
                data_dict['educational_requirements'] = [x.text for x in data_detail.find('div', {'class': 'edu_req'}).find_all('li')]
                # data_detail.find('div',{'class': 'edu_req'}).text.strip()
            except Exception as ex:
                data_dict['educational_requirements'] = "Error"

            try:
                data_dict['job_requirements'] = [x.text for x in data_detail.find('div', {'class': 'job_req'}).find_all('li')]
                # data_detail.find('div', {'class': 'job_req'}).text.strip()
            except Exception as ex:
                data_dict['job_requirements'] = "Error"



            try:
                data_dict['other_benefit'] = [x.text for x in data_detail.find('div', {'class': 'oth_ben'}).find_all('li')]
                    # data_detail.find('div', {'class': 'oth_ben '}).text.strip()
            except Exception as ex:
                data_dict['other_benefit'] = "Error"

        except Exception as ex:
            print("Detail Data error")
        # Calling the write_csv_file function
        write_csv_file(data_dict)

        # Increment of total_jobs
        total_jobs += 1

        JOB_LIST_API = 'http://127.0.0.1/api/job_create/'
        JOB_LIST_API_KEY = '96d56aceeb9049debeab628ac760aa11'
        HEADER = {'api-key': JOB_LIST_API_KEY}

        response = requests.post(JOB_LIST_API,json=data_dict, headers=HEADER)

        print(response)

        break
    # Increment page no.
    page_no += 1
    break

job_list_file_obj.close()

print('Successfully completed!')

# Total jobs
print('Total Job : {0}'.format(total_jobs))

