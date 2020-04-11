from requests import get
url = 'https://jobs.bdjobs.com/jobdetails.asp?id=904146&fcatId=8&ln=1'

job_text = get(url).text

# print(job_text)
print('---------------------------------------------')
from bs4 import BeautifulSoup




# print(type(dir(result)))
# job_detail = job_html.select('div.container.job-details1 .row.jdfx')

job_html = BeautifulSoup(job_text, 'html.parser')

# result = job_html.find_all('div.container.job-details1',id='job-preview')
# result = job_html.find_all('h4', attrs={"class": "job-title"})
# result = job_html.find_all('h4', {"class": "job-title"})
# result = job_html.find_all('h4', class_='job-title')
# result = job_html.select('.job-title')

result = job_html.find_all('h4', class_='job-title').get_text()
print(result)


# soup.find_all("a", attrs={"class": "sister"})
# job_detail_dict = {};
# job_detail_dict['Job_Title'] = job_html.find_all('.job-title').get_text()

# print(job_detail_dict)
# print(dir(job_detail_dict['Job_Title'])).contents[0]

# job_detail_dict['job-title'] = job_html.select('div.container.job-details1 .job-title').get_text()
# job_detail_dict['Company_Name'] = job_html.select('.company-name').get_text()
# job_detail_dict['Vacancy'] = job_html.select('.vac').get_text()
# job_detail_dict['Job_Context'] = job_html.select('.job_des').get_text()
# job_detail_dict['Employment_Status'] = job_html.select('.job_nat').get_text()
# job_detail_dict['Educational_Requirments'] = job_html.select('.edu_req').get_text()
# job_detail_dict['Additional_Requirments'] = job_html.select('.job_req').get_text()
# job_detail_dict['Salary'] = job_html.select('.salary_range').get_text()
# job_detail_dict['Other_Benefits'] = job_html.select('.oth_ben').get_text()
# job_detail_dict['Application_Deadline'] = job_html.select('.date').get_text()
# job_detail_dict['Company_Information'] = job_html.select('.information').get_text()
# job_detail_dict['Job_Right_Summery'] = job_html.select('.right.job-summary').get_text()

# print(job_detail_dict)

