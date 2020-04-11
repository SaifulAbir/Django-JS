import requests
from bs4 import BeautifulSoup
import csv
def write_csv_file(data):
    try:
        csv_writer.writerow(
            {'Job Title': data['job_title_text'], 'Company Name': data['company_name'], 'Education': data['education'],
             'Experience': data['experience'], 'Deadline': data['deadline'], 'Vacancy': data_dict['no_of_vacancy'],
             'Job Responsibilities': data_dict['job_responsibilities'],
             'Employment Status': data_dict['employment_status'],
             'Educational Requirment': data_dict['educational_requirements'],
             'Job Requirment': data_dict['job_requirements'],
             'Job Location': data_dict['job_location'], 'Salary': data_dict['salary'],
             'Other Benefit': data_dict['other_benefit'], 'Job Link': data['job_link']})
    except:
        print('Exception occurred! No problem. Keep going.')

job_list_file_obj = open('bdjobs_detail_list.csv', 'w', newline='')

main_site = 'http://jobs.bdjobs.com/'

url = 'http://jobs.bdjobs.com/jobsearch.asp?fcatId=8'

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
column_names = ['Job Title', 'Company Name', 'Education', 'Experience', 'Deadline', 'Vacancy', 'Job Responsibilities', 'Employment Status', 'Educational Requirment', 'Job Requirment', 'Job Location', 'Salary', 'Other Benefit', 'Job Link']

csv_writer = csv.DictWriter(job_list_file_obj, fieldnames=column_names)

csv_writer.writeheader()

csv_writer.writerow({'Job Title': '', 'Company Name': '', 'Education': '', 'Experience': '', 'Deadline': '', 'Vacancy': '', 'Job Responsibilities': '', 'Employment Status': '', 'Educational Requirment': '', 'Job Requirment': '', 'Job Location': '', 'Salary': '', 'Other Benefit': '', 'Job Link': ''})

page_no = 1
max_page_no = 18

total_jobs = 0

while page_no <= max_page_no:
    print('Page No : {0}'.format(page_no))

    post_data['pg'] = page_no

    resp = requests.post(url, data=post_data)

    html = BeautifulSoup(resp.content, 'html.parser')

    data = html.find_all('div', {'class': 'norm-jobs-wrapper'})

    if page_no == 1:
        max_page_no = html.find('div', {'id': 'topPagging'}).find_all('li')[-1].text.strip().replace('.', '')
        max_page_no = int(max_page_no)

    for dt in data:
        data_dict = {};
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
        try:
            data_dict['company_name'] = dt.find('div', {'class': 'comp-name-text'}).text.strip()
        except Exception as ex:
            data_dict['company_name'] = "COMPANY NAME"
        try:
            data_dict['deadline'] = dt.find('div', {'class': 'dead-text-d'}).text.strip()
        except Exception as ex:
            data_dict['deadline'] = "DEADLINE"
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
            data_detail = html_detail.find('div', {'class': 'col-md-8'})
            data_dict_detail = {};
            try:
                data_dict['no_of_vacancy'] = data_detail.find(text="Vacancy").findNext('p').text.strip()
            except Exception as ex:
                data_dict['no_of_vacancy'] = "Error"
            try:
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
            except Exception as ex:
                data_dict['job_responsibilities'] = "Error"
            try:
                data_dict['educational_requirements'] = [x.text for x in data_detail.find('div', {'class': 'edu_req'}).find_all('li')]
            except Exception as ex:
                data_dict['educational_requirements'] = "Error"
            try:
                data_dict['job_requirements'] = [x.text for x in data_detail.find('div', {'class': 'job_req'}).find_all('li')]
            except Exception as ex:
                data_dict['job_requirements'] = "Error"
            try:
                data_dict['other_benefit'] = [x.text for x in data_detail.find('div', {'class': 'oth_ben'}).find_all('li')]
            except Exception as ex:
                data_dict['other_benefit'] = "Error"
        except Exception as ex:
            print("Detail Data error")
        write_csv_file(data_dict)
        total_jobs += 1
    page_no += 1
job_list_file_obj.close()
print('Successfully completed!')
print('Total Job : {0}'.format(total_jobs))

