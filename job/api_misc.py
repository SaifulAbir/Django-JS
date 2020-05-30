from datetime import date

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.utils import json

from pro.models import Professional
from .models import FavouriteJob, ApplyOnline
from .serializers import *
from .utils import favourite_job_counter, applied_job_counter


@api_view(["GET"])
def get_vital_stats(self):
    companies = Company.objects.all().count()
    professional = Professional.objects.all().count()
    with_deadline = Job.objects.filter(application_deadline__gte=date.today()).count()
    without_deadline = Job.objects.filter(application_deadline__isnull=True).count()
    open_job = with_deadline + without_deadline
    data ={
        'professional_count': str(professional),
        'open_job' : str(open_job),
        'resume': str(0),
        'company_count': str(companies),
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

@api_view(["POST"])
def toggle_favourite(request):
    data = {}
    job_data = json.loads(request.body)

    if job_data:
        try:
            job = Job.objects.get(job_id = job_data['job_id'])
        except Job.DoesNotExist:
            job = None
        try:
            favourite_jobs = FavouriteJob.objects.filter(user = request.user.id,job = job_data['job_id'])
        except FavouriteJob.DoesNotExist:
            favourite_jobs = None
        if not favourite_jobs:
            favourite_job = FavouriteJob(job_id = job_data['job_id'], user = request.user )
            favourite_job.save()
            favourite_job_counter(job)
            data = {
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "job": job_data['job_id'],
                        "status": 'Saved'
                    }
                }
            }
        elif favourite_jobs:
            favourite_jobs.delete()
            favourite_job_counter(job)
            data = {
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "job": job_data['job_id'],
                        "status": 'Removed'
                    }
                }
            }
    return Response(data)


@api_view(["POST"])
def apply_online(request):
    data = {}
    job_data = json.loads(request.body)


    user = User.objects.get(id = request.user.id)
    j_id = job_data['job_id']

    job = Job.objects.get(job_id=j_id)

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    data.update({'job': job, 'created_by': user,
                 'created_from': str(ip), 'modified_by': user,
                 'modified_from': str(ip)})
    # apply_online_job = ApplyOnline(**data)
    # print('apply_online_job', apply_online_job)
    # apply_online_job.save()
    if job_data:
        try:
            job = Job.objects.get(job_id = job_data['job_id'])
        except Job.DoesNotExist:
            job = None
        try:
            apply_online_job = ApplyOnline.objects.filter(created_by = user, job = job)
        except ApplyOnline.DoesNotExist:
            apply_online_job = None
        if not apply_online_job:
            apply_online_job = ApplyOnline(**data)

            apply_online_job.save()
            applied_job_counter(job)
            data = {
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "job": job_data['job_id'],
                        "status": 'Saved'
                    }
                }
            }

    return Response(data)

@api_view(["POST"])
def save_trending_keywords(request):
    search_data = json.loads(request.body)

    if request.user_agent.is_mobile is True:
        device_name = 'Mobile'
    elif request.user_agent.is_tablet is True:
        device_name = 'Tablet'
    elif request.user_agent.is_pc is True:
        device_name = 'Computer'
    browser_name = request.user_agent.browser.family
    os_name = request.user_agent.os.family

    search_data.update([('device', device_name), ('browser', browser_name), ('operating_system', os_name)])

    if search_data['keyword']:
        key_obj = TrendingKeywords(**search_data)
        key_obj.save()
        return Response(HTTP_200_OK)

