from datetime import datetime, timedelta
from pprint import pprint

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.db.models import Q, Count
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from job.models import Job
from job.serializers import JobSerializer
from pro.utils import similar  # TODO: Why from pro


@api_view(["GET"])
def job_list(request):
    # TODO: recent jobs should be logged here
    try:
        query = request.GET.get('q')
        current_url = request.GET.get('current_url')
        sorting = request.GET.get('sort')
        category = request.GET.get('category')
        company = request.GET.get('company')
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

        if request.user.is_authenticated:
            current_user_id = request.user.id
            queryset = Job.objects.filter(
                Q(application_deadline__gte=datetime.now()) | Q(application_deadline=None),
                Q(fav_jobs__isnull=True) | Q(fav_jobs__user=current_user_id),
                Q(applied_jobs__isnull=True) | Q(applied_jobs__created_by=current_user_id),
                is_archived=False,
                status='Published',
            ).select_related('company'
                             ).annotate(is_favourite=Count('fav_jobs')
            ).annotate(is_applied=Count('applied_jobs'))

        else:
            queryset = Job.objects.filter(
                Q(application_deadline__gte=datetime.now()) | Q(application_deadline=None),
                is_archived=False,
                status='Published',
            ).select_related('company')



        if sorting == 'most-applied':
            queryset = queryset.order_by('-applied_count')
        elif sorting == 'top-rated':
            queryset = queryset.order_by('-favorite_count')
        else: # 'most-recent'
            queryset = queryset.order_by('-post_date')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
            )

        if category:
            queryset = queryset.filter(job_category=category)

        if datePosted:
            if datePosted == 'Last hour':
                queryset = queryset.filter(post_date__gt=datetime.now() - timedelta(hours=1))
            elif datePosted == 'Last 24 hour':
                queryset = queryset.filter(post_date__gt=datetime.now() - timedelta(hours=24))
            elif datePosted == 'Last 7 days':
                queryset = queryset.filter(post_date__gt=datetime.now() - timedelta(days=7))
            elif datePosted == 'Last 14 days':
                queryset = queryset.filter(post_date__gt=datetime.now() - timedelta(days=14))
            elif datePosted == 'Last 30 days':
                queryset = queryset.filter(post_date__gt=datetime.now() - timedelta(days=30))

        if gender and gender != 'Any':
            queryset = queryset.filter(job_gender=gender)

        if job_type:
            queryset = queryset.filter(job_type=job_type)

        if company:
            queryset = queryset.filter(company=company)

        if qualification:
            queryset = queryset.filter(qualification_id=qualification)

        if skill:
            queryset = queryset.filter(job_skills__in = [skill])

        if topSkill:
            queryset = queryset.filter(job_skills__in=[topSkill])

        if salaryMin and salaryMax:
            queryset = queryset.filter(salary_min__gte=salaryMin) & queryset.filter(salary_min__lte = salaryMax)

        if experienceMin and  experienceMax:
            queryset = queryset.filter(experience__gte=experienceMin) & queryset.filter(experience__lte = experienceMax)

        if job_city:
            queryset = queryset.filter(job_city__icontains=job_city)

        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 20)

        default_number_of_row = 20
        paginator = Paginator(queryset, page_size)

        try:
            queryset = paginator.page(page)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = paginator.page(1)

        for job in queryset:
            if not request.user.is_authenticated:
                job.is_favourite = False
                job.is_applied = False

        number_of_row_total = paginator.count
        number_of_pages = paginator.num_pages
        check_next_available_or_not = paginator.page(page).has_next()
        queryset = JobSerializer(queryset, many=True)

    except Job.DoesNotExist:
        queryset = [] # TODO:Does this work with .data?


    data = {
        'status': 'success',
        'count': number_of_row_total,
        'number_of_pages': number_of_pages,
        'next_pages': check_next_available_or_not,
        'code': HTTP_200_OK,
        'current_url': current_url,
        "results":  queryset.data,
    }

    return Response(data, HTTP_200_OK)


@api_view(["GET"])
def similar_jobs(request, identifier, limit = 5):
    try:
        selected_job = Job.objects.get(job_id=identifier)
    except Job.DoesNotExist:
        return JsonResponse(Job.DoesNotExist)

    if request.user.is_authenticated:
        current_user_id = request.user.id
        queryset = Job.objects.filter(
            ~Q(job_id=identifier),
            Q(application_deadline__gte=datetime.now()) | Q(application_deadline=None),
            Q(fav_jobs__isnull=True) | Q(fav_jobs__user=current_user_id),
            Q(applied_jobs__isnull=True) | Q(applied_jobs__created_by=current_user_id),
            is_archived=False,
            status='Published',
        ).select_related('company'
                         ).annotate(is_favourite=Count('fav_jobs')
        ).annotate(is_applied=Count('applied_jobs')
        ).order_by('-post_date')

    else:
        queryset = Job.objects.filter(
            ~Q(job_id=identifier),
            Q(application_deadline__gte=datetime.now()) | Q(application_deadline=None),
            is_archived=False,
            status='Published',
        ).order_by("-post_date")

    data = []
    for job in queryset:
        if(similar(selected_job.title, job.title) > 0.8 ): # TODO: Read from settings)
            if not request.user.is_authenticated:
                job.is_favourite = False
                job.is_applied = False
            data.append(job)
        if len(data) >= limit:
            break

    data = JobSerializer(data, many=True).data
    return Response(data)

@api_view(["GET"])
def recent_jobs(request, limit:int = 6):
    if request.user.is_authenticated:
        current_user_id = request.user.id
        queryset = Job.objects.filter(
            Q(application_deadline__gte=datetime.now()) | Q(application_deadline=None),
            Q(fav_jobs__isnull=True) | Q(fav_jobs__user=current_user_id),
            Q(applied_jobs__isnull=True) | Q(applied_jobs__created_by=current_user_id),
            is_archived=False,
            status='Published',
        ).select_related('company'
                         ).annotate(is_favourite=Count('fav_jobs')
        ).annotate(is_applied=Count('applied_jobs')
        ).order_by('-post_date')[:limit]

    else:
        queryset = Job.objects.filter(
            Q(application_deadline__gte=datetime.now()) | Q(application_deadline=None),
            is_archived=False,
            status='Published',
        ).select_related('company'
                         ).order_by('-post_date')[:limit]

    for job in queryset:
        if not request.user.is_authenticated:
            job.is_favourite = False
            job.is_applied = False

    data = JobSerializer(queryset, many=True).data
    return Response(data)


@api_view(["GET"])
def favourite_jobs(request):
    current_user_id = request.user.id
    queryset = Job.objects.filter(
        Q(applied_jobs__isnull=True) | Q(applied_jobs__created_by=current_user_id),
        fav_jobs__user=current_user_id,
    ).select_related('company'
                     ).annotate(is_applied=Count('applied_jobs')
    ).order_by('-post_date')

    for job in queryset:
        job.is_favourite = True

    data = JobSerializer(queryset, many=True).data
    return Response(data)


@api_view(["GET"])
def applied_jobs(request):
    current_user_id = request.user.id
    queryset = Job.objects.filter(
        Q(fav_jobs__isnull=True) | Q(fav_jobs__user=current_user_id),
        applied_jobs__created_by=current_user_id,
    ).select_related('company'
                     ).annotate(is_favourite=Count('fav_jobs')
    ).order_by('-post_date')

    for job in queryset:
        job.is_applied = True

    data = JobSerializer(queryset, many=True).data
    return Response(data)



