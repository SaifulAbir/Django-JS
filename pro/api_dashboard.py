from django.db.models.functions import TruncMonth
from rest_framework.decorators import api_view
from rest_framework.response import Response

from job.models import Job
from pro.models import ProfessionalSkill


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