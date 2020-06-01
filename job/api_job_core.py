from datetime import datetime, timedelta
from pprint import pprint

from django.db import connection
from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from rest_framework.views import APIView
from django.db.models import Q, Count
from job.models import Job, FavouriteJob, ApplyOnline, Skill
from job.serializers import JobSerializerAllField, JobSerializer
from p7.models import populate_user_info

# TODO Handle try catch
class JobAPI(APIView):
    def get(self, request, slug):
        if request.user.is_authenticated:
            current_user_id = request.user.id
            queryset = Job.objects.filter(
                Q(fav_jobs__isnull=True) | Q(fav_jobs__user=current_user_id),
                Q(applied_jobs__isnull=True) | Q(applied_jobs__created_by=current_user_id),
                is_archived=False,
                status='Published',
                slug=slug,
            ).select_related('company'
           # ).prefetch_related('job_skills'
            ).annotate(is_favourite=Count('fav_jobs')
            ).annotate(is_applied=Count('applied_jobs')
            ).order_by('-post_date'
            ).first()

        else:
            queryset = Job.objects.filter(
                is_archived=False,
                status='Published',
                slug=slug,
            ).select_related('company'
            #).prefetch_related('job_skills'
            ).order_by('-post_date'
            ).first()

            queryset.is_favourite = False
            queryset.is_applied = False

        data = JobSerializerAllField(queryset).data
        data['job_skills'] = []
        for skill in queryset.job_skills.all():
            data['job_skills'].append(skill.name)
        # pprint(connection.queries)
        return Response(data)



@api_view(["POST"])
def create_job(request):
    job_data = json.loads(request.body)
    try:
        skills = job_data['skills']
        del job_data['skills']
    except KeyError:
        skills = None

    job_obj = Job(**job_data)
    populate_user_info(request, job_obj, False, False)
    job_obj.save()
    if skills:
        skill_list = skills.split(',')
        for skill in skill_list:
            try:
                skill_obj = Skill.objects.get(name=skill)
            except Skill.DoesNotExist:
                skill_obj = None
            if skill_obj:
                job_obj.job_skills.add(skill_obj)

    return Response(HTTP_200_OK)


class JobUpdateView(GenericAPIView, UpdateModelMixin):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

def get_company_latlng(job):
    if type(job) is QuerySet:
        job = job[0]
    if job.company_name:
        latitude = job.company_name.latitude
        longitude = job.company_name.longitude
    return latitude, longitude

def get_company_logo(job):
    # TODO: read from string file/ settings
    if type(job) is QuerySet:
        job = job[0]
    if job.company_name:
        if job.company_name.profile_picture:
            profile_picture = '/media/' + str(job.company_name.profile_picture)
        else:
            profile_picture = '/static/images/job/company-logo-2.png'
    else:
        profile_picture = '/static/images/job/company-logo-2.png'

    return profile_picture

def get_favourite_status(job : Job, user):
    if type(job) is QuerySet:
        job = job[0]
    if user.is_authenticated:
        try:
            favourite_job = FavouriteJob.objects.get(job=job, user=user)
        except FavouriteJob.DoesNotExist:
            favourite_job = None
    else:
        favourite_job = None

    return favourite_job != None

def get_applied_status(job : Job, user):
    if type(job) is QuerySet:
        job = job[0]
    if user.is_authenticated:
        try:
            applied_job = ApplyOnline.objects.get(job=job, created_by=user)
        except ApplyOnline.DoesNotExist:
            applied_job = None
    else:
        applied_job = None

    return applied_job != None