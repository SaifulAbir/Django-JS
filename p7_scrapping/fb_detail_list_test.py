# -*- coding: utf-8 -*-

"""
Crawl  jobs from facebook.com
"""

import time, datetime
from selenium import webdriver

main_site = 'http://127.0.0.1:8000/'
main_site = 'http://dev.ishraak.com/'
facebook_url = 'https://m.facebook.com/groups/119479435370179/?ref=br_rs&_rdc=1&_rdr'
# Job search url
# url = f'{bdjobs}/jobsearch.asp?fcatId=8'

COMPANY_LIST_API = main_site + 'api/company/list'
JOB_LIST_API = main_site + 'api/job/create/'
JOB_LIST_API_KEY = '96d56aceeb9049debeab628ac760aa11'
API_HEADER = {'api-key': JOB_LIST_API_KEY}


def main():
    driver = webdriver.Chrome('driver/chromedriver')  # Optional argument, if not specified will search path.
    driver.get(facebook_url)
    driver.maximize_window()

    page = True

    # for dt in data:
    #     # A dictionary to pass data to function
    #     data_dict = {}



    while page == True:
        elems = driver.find_elements_by_xpath('//*[@id="u_0_8"]/div/header/div[2]/div/div/div[1]/div/a').getattr('href')
        print(elems)
        print('hello')
        for elem in elems:
            print(elem.get_attribute("href"))

#         data = driver.find_all('div', {'class': ['', 'norm-jobs-wrapper']})
#
#         try:
#             driver.find_element_by_xpath('//*[@id="m_more_item"]/a/div/div/div/strong/text()').click()
#         except:
#             page = False
#
#         for dt in data:
#             # A dictionary to pass data to function
#             data_dict = {}
#
#             # Fetching desired content using its tag and class
#             try:
#                 title = dt.find('div', {'class': 'job-title-text'})
#             except Exception as ex:
#                 title = "JOB TITLE"
#
#             try:
#                 data_dict['job_url_1'] = bdjobs + title.find('a', {'href': True})['href']
#             except Exception as ex:
#                 data_dict['job_url_1'] = "JOB LINK"
#
#             try:
#                 data_dict['title'] = title.text.strip()
#             except Exception as ex:
#                 data_dict['title'] = "JOB TITLE TEXT"
#
#             try:
#                 data_dict['company_name_id'] = dt.find('div', {'class': 'comp-name-text'}).text.strip()
#
#                 # TODO: Move outside loop
#                 print('Retrieving company data..')
#                 response = requests.get(COMPANY_LIST_API, json=data_dict, headers=API_HEADER)
#                 print('done.')
#                 josnResponse = response.json()
#
#                 companyName = unknown_company
#                 for company in josnResponse:
#                     if company['name'] == data_dict['company_name_id']:
#                         companyName = companyName['name']
#                 data_dict['company_name_id'] = companyName
#
#             except Exception as ex:
#                 data_dict['company'] = unknown_company
#
#             try:
#                 data_dict['application_deadline'] = dt.find('div', {'class': 'dead-text-d'}).text.strip()
#                 datetimeobject = datetime.datetime.strptime(data_dict['application_deadline'], "%b %d, %Y")
#                 data_dict['application_deadline'] = datetimeobject.strftime('%Y-%m-%d')
#             except Exception as ex:
#                 data_dict['deadline'] = "DEADLINE"
#
#             try:
#                 data_dict['education'] = dt.find('div', {'class': 'edu-text-d'}).text.strip()
#             except Exception as ex:
#                 data_dict['education'] = "EDUCATION"
#
#             # try:
#             #     data_dict['experience'] = dt.find('div', {'class': 'exp-text-d'}).text.strip()
#             # except Exception as ex:
#             #     data_dict['experience'] = "EXPERIENCE"
#
#             try:
#                 resp_detail = s.post(bdjobs + title.find('a', {'href': True})['href'])
#                 html_detail = BeautifulSoup(resp_detail.content, 'html.parser')
#                 data_detail = html_detail.find('div', {'class': 'job-preview'})
#                 try:
#                     data_dict['raw_content'] = data_detail.text
#                 except Exception as ex:
#                     data_dict['raw_content'] = ""
#
#                 try:
#                     published_date = data_detail.find('div', {'class': 'panel-body'}).findNext(
#                         'h4').text.strip().replace(u'\xa0', u'').replace(u'Published on:', u'')
#                     datetimeobject = datetime.datetime.strptime(published_date, "%b %d, %Y")
#                     data_dict['post_date'] = datetimeobject.strftime('%Y-%m-%d') + " 00:00:00.000000"
#                 except Exception as ex:
#                     data_dict['post_date'] = "Error"
#
#                 try:
#                     data_dict['vacancy'] = data_detail.find(text="Vacancy").findNext('p').text.strip()
#
#                     if data_dict['vacancy'] == 'Not specific':
#                         data_dict['vacancy'] = UNKNOWN_VACANCY
#                 except Exception as ex:
#                     data_dict['no_of_vacancy'] = "Error"
#
#                 # try:
#                 #     data_dict['employment_status'] = data_detail.find('div', {'class': 'job_nat'}).findNext('p').text.strip()
#                 # except Exception as ex:
#                 #     data_dict['employment_status'] = "Error"
#
#                 try:
#                     data_dict['address'] = data_detail.find(text="Job Location").findNext('p').text.strip()
#                 except Exception as ex:
#                     data_dict['address'] = "Error"
#
#                 # try:
#                 #     data_dict['salary'] = data_detail.find(text="Salary").findNext('ul').text.strip()
#                 # except Exception as ex:
#                 #     data_dict['salary'] = "Error"
#
#                 try:
#                     data_dict['responsibilities'] = data_detail.find('div', {'class': 'job_des'}).text
#                 except Exception as ex:
#                     data_dict['responsibilities'] = "Error"
#
#                 # try:
#                 #     data_dict['educational_requirements'] = [x.text for x in data_detail.find('div', {'class': 'edu_req'}).find_all('li')]
#                 #     # data_detail.find('div',{'class': 'edu_req'}).text.strip()
#                 # except Exception as ex:
#                 #     data_dict['educational_requirements'] = "Error"
#
#                 # try:
#                 #     data_dict['job_requirements'] = [x.text for x in data_detail.find('div', {'class': 'job_req'}).find_all('li')]
#                 #     # data_detail.find('div', {'class': 'job_req'}).text.strip()
#                 # except Exception as ex:
#                 #     data_dict['job_requirements'] = "Error"
#
#                 try:
#                     data_dict['other_benefits'] = [x.text for x in
#                                                    data_detail.find('div', {'class': 'oth_ben'}).find_all('li')]
#                 except Exception as ex:
#                     data_dict['other_benefits'] = "Error"
#
#             except Exception as ex:
#                 print("Detail Data error")
#
#             if data_dict['post_date'] < last_scrapping_date:
#                 scrapping_status = False
#                 break
#
#             if data_dict['job_url_1'] in job_links:
#                 continue
#
#             job_links.append(data_dict['job_url_1'])
#             response = requests.post(JOB_LIST_API, json=data_dict, headers=API_HEADER)
#
#             if response.status_code == 200:
#                 saved_jobs += 1
#             else:
#                 print("Trying with minimum")
#                 min_data = {
#                     'title': 'Error BdJobs Scraping',
#                     'company_name_id': unknown_company,
#                     'job_url_1': data_dict['job_url_1'],
#                     'raw_content': data_dict['raw_content']
#                 }
#                 response = requests.post(JOB_LIST_API, json=min_data, headers=API_HEADER)
#                 if response.status_code == 200:
#                     print('Saved with minimum')
#                     saved_jobs += 1
#             # Increment of total_jobs
#             total_jobs += 1
#
#             print(f"{total_jobs}: {data_dict['title']}")
#             print(response.status_code)
#
#         # Increment page no.
#         page_no += 1
#         if scrapping_status == False:
#             break
#
#     print('Successfully completed!')
#
#     try:
#         fl = open("last_scrap_time.txt", "w+")
#         fl.write(current_date)
#     except:
#         print('Writing last scrap time failed')
#     finally:
#         if fl != None and not fl.closed:
#             fl.close()
#
#     # Total jobs
#     print('Total Job : {0}'.format(total_jobs))
#     print('Saved Job : {0}'.format(saved_jobs))
#
#
if __name__ == "__main__":
    main()