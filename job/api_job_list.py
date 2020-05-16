from datetime import datetime, timedelta

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from job.serializers import JobSerializer
from pro.utils import similar
from job.models import Job, FavouriteJob, ApplyOnline, JobType, Company


@api_view(["GET"])
def job_list(request):
    try:
        query = request.GET.get('q')
        current_url = request.GET.get('current_url')
        print(current_url)
        sorting = request.GET.get('sort')
        category = request.GET.get('category')
        district = request.GET.get('location')
        skill = request.GET.get('skill')
        location_from_homepage = request.GET.get('location_from_homepage')
        keyword_from_homepage = request.GET.get('keyword_from_homepage')
        salaryMin = request.GET.get('salaryMin')
        salaryMax = request.GET.get('salaryMax')
        experienceMin = request.GET.get('experienceMin')
        experienceMax = request.GET.get('experienceMax')
        datePosted = request.GET.get('datePosted')
        gender = request.GET.get('gender')
        job_type = request.GET.get('job_type')
        qualification = request.GET.get('qualification')
        topSkill = request.GET.get('top-skill')

        if sorting == 'most-applied':
            job_list = Job.objects.all().order_by('-applied_count')
        elif sorting == 'top-rated':
            job_list = Job.objects.all().order_by('-favorite_count')
        else: # 'most-recent'
            job_list = Job.objects.all().order_by('-post_date')

        if query:
            job_list = job_list.filter(
                Q(title__icontains=query)
            )

        if category:
            job_list = job_list.filter(
                job_category=category)

        if datePosted:
            if datePosted == 'Last hour':
                job_list = job_list.filter(post_date__gt=datetime.now() - timedelta(hours=1))

            if datePosted == 'Last 24 hour':
                job_list = job_list.filter(post_date__gt=datetime.now() - timedelta(hours=24))

            if datePosted == 'Last 7 days':
                job_list = job_list.filter(post_date__gt=datetime.now() - timedelta(days=7))

            if datePosted == 'Last 14 days':
                job_list = job_list.filter(post_date__gt=datetime.now() - timedelta(days=14))

            if datePosted == 'Last 30 days':
                job_list = job_list.filter(post_date__gt=datetime.now() - timedelta(days=30))

        if gender and gender != 'Any':
            job_list = job_list.filter(
                gender_id=gender
            )

        if job_type:
            job_list = job_list.filter(
                employment_status=job_type
            )

        if qualification:
            job_list = job_list.filter(
                qualification_id=qualification
            )

        if skill:
            job_list = job_list.filter(job_skills__in = [skill])
            print(skill)


        if topSkill:
            job_list = job_list.filter(job_skills__in=[topSkill])
            print(topSkill)

        if salaryMin and salaryMax:
            job_list = (job_list.filter(salary_min__gte=salaryMin) & job_list.filter(salary_min__lte = salaryMax))


        if experienceMin and  experienceMax:
            job_list = (job_list.filter(experience__gte=experienceMin) & job_list.filter(experience__lte = experienceMax))

        if location_from_homepage:
            job_list = job_list.filter(
                Q(district__name__icontains=location_from_homepage)
            )

        if keyword_from_homepage:
            job_list = job_list.filter(
                Q(title__icontains=keyword_from_homepage)
            )


        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 2)

        default_number_of_row = 2
        paginator = Paginator(job_list, page_size)

        try:
            job_list = paginator.page(page)
        except PageNotAnInteger:
            job_list = paginator.page(1)
        except EmptyPage:
            job_list = paginator.page(1)

        for job in job_list:
            job = populate_favourite_status(job, request.user)
            job = populate_applied_status(job, request.user)
            job = populate_company_logo(job)

        number_of_row_total = paginator.count
        number_of_pages = paginator.num_pages
        check_next_available_or_not = paginator.page(page).has_next()
        job_list = JobSerializer(job_list, many=True)

    except Job.DoesNotExist:
        job_list = []


    data = {
        'status': 'success',
        'count': number_of_row_total,
        'number_of_pages': number_of_pages,
        'next_pages': check_next_available_or_not,
        'code': HTTP_200_OK,
        'current_url': current_url,
        "results":  job_list.data,
    }


    return Response(data, HTTP_200_OK)



@api_view(["GET"])
def similar_jobs(request, identifier, limit = 5):
    try:
        selected_job = Job.objects.get(job_id=identifier)
    except Job.DoesNotExist:
        return JsonResponse(Job.DoesNotExist)

    queryset = Job.objects.filter(is_archived=False,
                                  status='Published',
                                  application_deadline__lte=datetime.now())
    data = []
    for job in queryset:
        if job.job_id != selected_job.job_id and similar(selected_job.title, job.title) > 0.80: # TODO: Read from settings
            job = populate_favourite_status(job, request.user)
            job = populate_applied_status(job, request.user)
            job = populate_company_logo(job)
            data.append(make_job_list_response(job))
        if len(data) >= limit:
            break

    return JsonResponse(list(data), safe=False)


@api_view(["GET"])
def recent_jobs(request, limit:int = 6):
    queryset = Job.objects.all().order_by('-post_date')[:limit]
    data = []
    for job in queryset:
        job = populate_favourite_status(job, request.user)
        job = populate_applied_status(job, request.user)
        job = populate_company_logo(job)
        data.append(make_job_list_response(job))

    return JsonResponse(list(data), safe=False)


@api_view(["GET"])
def favourite_jobs(request):
    current_user_id = request.user.id
    queryset = FavouriteJob.objects.filter(user=current_user_id)
    data = []
    for fav_job in queryset:
        job = Job.objects.get(job_id=fav_job.job_id)
        job = populate_applied_status(job, request.user)
        job = populate_company_logo(job)
        data.append(make_job_list_response(job))

    return JsonResponse(list(data), safe=False)


@api_view(["GET"])
def applied_jobs(request):
    current_user_id = request.user.id
    queryset = ApplyOnline.objects.filter(created_by=current_user_id)
    data = []
    for app_job in queryset:
        job = Job.objects.filter(job_id=app_job.job_id)
        job = populate_favourite_status(job, request.user)
        job = populate_company_logo(job)
        data.append(make_job_list_response(job))

    return JsonResponse(list(data), safe=False)


def populate_company_logo(job):
    # TODO: read from string file/ settings
    if job.company_name:
        if job.company_name.profile_picture:
            job.profile_picture = '/media/' + str(job.company_name.profile_picture)
        else:
            job.profile_picture = '/static/images/job/company-logo-2.png'
    else:
        job.profile_picture = '/static/images/job/company-logo-2.png'

    return job

def populate_favourite_status(job : Job, user):
    if user.is_authenticated:
        try:
            favourite_job = FavouriteJob.objects.get(job=job, user=user)
        except FavouriteJob.DoesNotExist:
            favourite_job = False
    else:
        favourite_job = False

    job.favourite_job = favourite_job
    return job

def populate_applied_status(job : Job, user):
    if user.is_authenticated:
        try:
            applied_job = ApplyOnline.objects.get(job=job, created_by=user)
        except ApplyOnline.DoesNotExist:
            applied_job = None
    else:
        applied_job = False

    job.applied_job = applied_job

    return job

def make_job_list_response(job : Job):
    return {
        'job_id': job.job_id,
        'slug': job.slug,
        'title': job.title,
        'job_city': job.city,
        'job_country': job.country,
        'job_nature': job.job_nature,
        'job_site': job.job_site,
        'job_type': job.job_type,
        'company_name': str(job.company_name),
        'profile_picture': job.profile_picture,
        'is_favourite' : job.is_favourite,
        'is_applied' : job.is_applied,
        'post_date': job.post_date,
        'created_at': job.created_at,
        'application_deadline':job.application_deadline,
    }