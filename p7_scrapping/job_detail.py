from requests import get
from bs4 import BeautifulSoup
job_detail_url = 'https://jobs.bdjobs.com/jobdetails.asp?id=904199&fcatId=8&ln=1'
job_detail_text = get(job_detail_url).text
job_detail_html = BeautifulSoup(job_detail_text, 'html.parser')
# result = job_detail_html.find_all('h4', class_='job-title')
# print(result)
#
# job_detail_dict = {};
# job_detail_dict['job-title'] = job_detail_html.find('h4' , class_ = 'job-title').text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\r', u'')
# job_detail_dict['company_name'] = job_detail_html.find('h2', class_= 'company-name').text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\r', u'')
# job_detail_dict['vacancy'] = job_detail_html.find('div', class_ = 'vac').text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'Vacancy', u'')
# job_detail_dict['job_context'] = job_detail_html.find('div', class_= 'job_des').text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\r', u'')
# job_detail_dict['employment_etatus'] = job_detail_html.find('div', class_= 'job_nat').text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\r', u'')
# job_detail_dict['educational_requirments'] = job_detail_html.find('div', class_= 'edu_req').text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\r', u'')
# job_detail_dict['additional_requirments'] = job_detail_html.find('div', class_= 'job_req').text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\r', u'')
# job_detail_dict['job_location'] = job_detail_html.find('div', class_= 'job_loc').text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\r', u'')
# job_detail_dict['salary'] = job_detail_html.find('div', class_= 'salary_range').text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\r', u'')
# job_detail_dict['other_benefits'] = job_detail_html.find('div', class_= 'oth_ben').text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\r', u'')
# job_detail_dict['application_deadline'] = str(job_detail_html.find('div', class_= 'date'))
# job_detail_dict['company_information'] = str(job_detail_html.find('div', class_= 'information'))
# job_detail_dict['job_category'] = str(job_detail_html.find('div', class_= 'category'))
import time, datetime
now = datetime.datetime.now()

published_date = job_detail_html.find('div', {'class': 'panel-body'}).findNext('h4').text.strip().replace(u'\xa0',u'').replace(u'Published on:',u'')
current_date = now.strftime("%b %-1d, %Y")

print(repr(published_date))
print(repr(current_date))

if published_date == current_date:
    print('Date Matched')
else:
    print('Date Not Matched')


# .replace(u'\xa0', u'').replace(u'\n', u'')
# published_date = job_detail_html.find('div', class_ = 'panel-body').h4
# for e in published_date.find_all():
#     e.decompose()
# published_date = published_date.text.replace(u'\xa0', u'').replace(u'\n', u'').replace(u'\r', u'')
#
# published_date = published_date.lstrip('\'')
# print(published_date)
# import time, datetime
# now = datetime.datetime.now()
# # import time, datetime
# conv=time.strptime(published_date,"%b %d %Y")
# #
#
# current_date = now.strftime("%b %-1d, %Y")
# current_date2 = conv.strftime("%b %-1d, %Y")
# published_date = list(published_date.split(' '))
# current_date = list(current_date.split(' '))
# if published_date == current_date:
#     print('Date Matched')
# else:
#     print('Date Not Matched')
#
# print(str(current_date) == str(current_date2))


# job_detail_dict['job_right_rummery'] = job_detail_html.select('.right.job-summary').text



