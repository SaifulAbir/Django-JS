# -*- coding: utf-8 -*-

"""
Crawl IT jobs from bdjobs.com
"""

# Load necessary modules
import requests
from bs4 import BeautifulSoup
import csv


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
        csv_writer.writerow({'job_title': data['job_title_text'], 'job_link': data['job_link']})
    except:
        print('Exception occurred! No problem. Keep going.')


# Function ends here

# Open a csv file with 'write' mode
job_list_file_obj = open('bdjobs_links.csv', 'w', newline='')

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

column_names = ['job_title', 'job_link']

# Creating csv writer
csv_writer = csv.DictWriter(job_list_file_obj, fieldnames=column_names)

# Write column name
csv_writer.writeheader()

csv_writer.writerow({'job_title': '', 'job_link': ''})

# At least 1 page should be available
page_no = 1
max_page_no = 4

# Total jobs counting
total_jobs = 0

while page_no <= max_page_no:
    print('Page No : {0}'.format(page_no))

    # Assign new page no.
    post_data['pg'] = page_no

    resp = requests.post(url, data=post_data)

    html = BeautifulSoup(resp.content, 'html.parser')

    data = html.find_all('div', {'class': 'norm-jobs-wrapper'})

    if page_no == 1:
        max_page_no = html.find('div', {'id': 'topPagging'}).find_all('li')[-1].text.strip().replace('.', '')
        max_page_no = int(max_page_no)

    for dt in data:
        # A dictionary to pass data to function
        data_dict = {};

        # Fetching desired content using its tag and class
        try:
            job_title = dt.find('div', {'class': 'job-title-text'})
        except Exception as ex:
            job_title = "JOB TITLE"

        try:
            data_dict['job_link'] = main_site + job_title.find('a', {'href': True})['href']
        except Exception as ex:
            data_dict['job_link'] = "JOB LINK"

        try:
            data_dict['job_title_text'] = job_title.text.strip()
        except Exception as ex:
            data_dict['job_title_text'] = "JOB TITLE TEXT"

        # Calling the write_csv_file function
        write_csv_file(data_dict)

        # Increment of total_jobs
        total_jobs += 1

    # Increment page no.
    page_no += 1

job_list_file_obj.close()

print('Successfully completed!')

# Total jobs
print('Total Job : {0}'.format(total_jobs))

