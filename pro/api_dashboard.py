from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

from job.models import Job, FavouriteJob, ApplyOnline
from pro.models import ProfessionalSkill, ProRecentActivity


@api_view(["GET"])
def skill_job_chart(request):
    user = request.user
    skills = ProfessionalSkill.objects.filter(created_by=user)
    all_query = Job.objects.none()
    for skill in skills:
        jobs = Job.objects.filter(job_skills=skill.skill_name)
        all_query = all_query|jobs
    # count = all_query.filter(created_date__year='2020').values_list('created_date__month').distinct().annotate(total=Count('title'))
    count = all_query.annotate(month=TruncMonth('publish_date')).values('month').order_by('month').annotate(total=Count('title'))
    return Response(count)


@api_view(["GET"])
def pro_recent_activity(request):
    user = request.user
    activity = ProRecentActivity.objects.filter(user = user).order_by('time')
    for obj in activity:
        if (timezone.now() - obj.time).days >=1:
            obj.activity_time = '{} days ago'.format((timezone.now() - obj.time).days)
        elif (((timezone.now() - obj.time).seconds)//3600) >=1:
            obj.activity_time = '{} hour ago'.format(((timezone.now() - obj.time).seconds) //3600)
        elif (((timezone.now() - obj.time).seconds)//60) >=1:
            obj.activity_time = '{} min ago'.format(((timezone.now() - obj.time).seconds) //60)
        else:
            obj.activity_time = '{} sec ago'.format(((timezone.now() - obj.time).seconds))
    activity_list =[{
        'description': act.description,
        'time': act.activity_time,
        'type': act.type
    }for act in activity]
    return Response(activity_list)


@api_view(["GET"])
def info_box_api(request):
    user = request.user
    favourite_job = FavouriteJob.objects.filter(user = user).count()
    applied_job = ApplyOnline.objects.filter(created_by = user).count()
    skills_count = ProfessionalSkill.objects.filter(created_by=user).count()
    data ={'favourite_job_count':favourite_job,
           'applied_job_count':applied_job,
           'skills_count':skills_count
           }

    return Response(data)