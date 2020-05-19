from datetime import datetime, timedelta
from pprint import pprint

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.db.models import Q, F
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from job.serializers import JobSerializer
from job.api_job_core import get_favourite_status, get_company_logo, get_applied_status
from pro.utils import similar # TODO: Why from pro
from job.models import Job, FavouriteJob, ApplyOnline


@api_view(["GET"])
def job_list(request):
    # TODO: recent jobs should be logged here
    try:
        query = request.GET.get('q')
        current_url = request.GET.get('current_url')
        sorting = request.GET.get('sort')
        category = request.GET.get('category')
        district = request.GET.get('location')
        skill = request.GET.get('skill')
        job_city = request.GET.get('job_city')
        salaryMin = request.GET.get('salaryMin')
        salaryMax = request.GET.get('salaryMax')
        experienceMin = request.GET.get('experienceMin')
        experienceMax = request.GET.get('experienceMax')
        datePosted = request.GET.get('datePosted')
        gender = request.GET.get('gender')
        job_type = request.GET.get('job_type')
        qualification = request.GET.get('qualification')
        topSkill = request.GET.get('top-skill')

        job_list = Job.objects.filter(
            is_archived=False,
            status='Published',
            application_deadline__gte=datetime.now()
        )

        if sorting == 'most-applied':
            job_list = job_list.order_by('-applied_count')
        elif sorting == 'top-rated':
            job_list = job_list.order_by('-favorite_count')
        else: # 'most-recent'
            job_list = job_list.order_by('-post_date')

        if query:
            job_list = job_list.filter(
                Q(title__icontains=query)
            )

        if category:
            job_list = job_list.filter(job_category=category)

        if datePosted:
            if datePosted == 'Last hour':
                job_list = job_list.filter(post_date__gt=datetime.now() - timedelta(hours=1))
            elif datePosted == 'Last 24 hour':
                job_list = job_list.filter(post_date__gt=datetime.now() - timedelta(hours=24))
            elif datePosted == 'Last 7 days':
                job_list = job_list.filter(post_date__gt=datetime.now() - timedelta(days=7))
            elif datePosted == 'Last 14 days':
                job_list = job_list.filter(post_date__gt=datetime.now() - timedelta(days=14))
            elif datePosted == 'Last 30 days':
                job_list = job_list.filter(post_date__gt=datetime.now() - timedelta(days=30))

        if gender and gender != 'Any':
            job_list = job_list.filter(job_gender=gender)

        if job_type:
            job_list = job_list.filter(job_type=job_type)

        if qualification:
            job_list = job_list.filter(qualification_id=qualification)

        if skill:
            job_list = job_list.filter(job_skills__in = [skill])

        if topSkill:
            job_list = job_list.filter(job_skills__in=[topSkill])

        if salaryMin and salaryMax:
            job_list = job_list.filter(salary_min__gte=salaryMin) & job_list.filter(salary_min__lte = salaryMax)

        if experienceMin and  experienceMax:
            job_list = job_list.filter(experience__gte=experienceMin) & job_list.filter(experience__lte = experienceMax)

        if job_city:
            job_list = job_list.filter(job_city__icontains=job_city)

        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)

        default_number_of_row = 20
        paginator = Paginator(job_list, page_size)

        try:
            job_list = paginator.page(page)
        except PageNotAnInteger:
            job_list = paginator.page(1)
        except EmptyPage:
            job_list = paginator.page(1)

        for job in job_list:
            job.is_favourite = get_favourite_status(job, request.user)
            job.is_applied = get_applied_status(job, request.user)
            job.profile_picture = get_company_logo(job)

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

    queryset = Job.objects.filter(
        ~Q(job_id=identifier),
        is_archived=False,
        status='Published',
        application_deadline__gte=datetime.now(),
    ).order_by(
        "-post_date"
    )

    data = []
    for job in queryset:
        if(similar(selected_job.title, job.title) > 0.8 ): # TODO: Read from settings)
            job.is_favourite = get_favourite_status(job, request.user)
            job.is_applied = get_applied_status(job, request.user)
            job.profile_picture = get_company_logo(job)
            data.append(job)
        if len(data) >= limit:
            break

    data = JobSerializer(data, many=True).data
    return Response(data)

@api_view(["GET"])
def recent_jobs(request, limit:int = 6):
    queryset = Job.objects.filter(
        is_archived=False,
        status='Published',
        application_deadline__gte=datetime.now()
    ).order_by('-post_date')[:limit]

    for job in queryset:
        job.is_favourite = get_favourite_status(job, request.user)
        job.is_applied = get_applied_status(job, request.user)
        job.profile_picture = get_company_logo(job)
    data = JobSerializer(queryset, many=True).data
    return Response(data)


@api_view(["GET"])
def favourite_jobs(request):
    current_user_id = request.user.id
    queryset = FavouriteJob.objects.filter(user=current_user_id).order_by('-created_date')
    jobs = []
    for fav_job in queryset:
        job = Job.objects.get(job_id=fav_job.job_id)
        job.is_favourite = True
        job.is_applied = get_applied_status(job, request.user)
        job.profile_picture = get_company_logo(job)
        jobs.append(job)

    pprint(connection.queries)
    data = JobSerializer(jobs, many=True).data
    return Response(data)


@api_view(["GET"])
def applied_jobs(request):
    current_user_id = request.user.id
    queryset = ApplyOnline.objects.filter(created_by=current_user_id).order_by('-created_at')
    jobs = []
    for app_job in queryset:
        job = Job.objects.get(job_id=app_job.job_id)
        job.is_favourite = get_favourite_status(job, request.user)
        job.is_applied = True
        job.profile_picture = get_company_logo(job)
        jobs.append(job)
    data = JobSerializer(jobs, many=True).data
    return Response(data)



