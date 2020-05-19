from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from rest_framework.views import APIView

from job.models import Job, FavouriteJob, ApplyOnline, Skill
from job.serializers import JobSerializerAllField, JobSerializer
from p7.models import populate_user_info


class JobAPI(APIView):
    def get(self, request, slug):
        job = get_object_or_404(Job, slug=slug)
        job.is_favourite = get_favourite_status(job, request.user)
        job.is_applied = get_applied_status(job, request.user)
        job.profile_picture = get_company_logo(job)
        job.latitude, job.longitude = get_company_latlng(job)

        data = JobSerializerAllField(job).data

        data['skill']=[]
        for skill in job.job_skills.all():
            data['skill'].append(skill.name)

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