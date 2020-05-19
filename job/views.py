from django.shortcuts import render
from rest_framework.views import APIView
from .models import Company
from rest_framework.response import Response
from rest_framework import generics

def jobs(request):
    context = {
        'keyword': '',
        'top_categories':'',
        'top_skill':''
    }

    keyword = request.POST.get('keyword')
    top_category = request.POST.get('top-category')
    top_skill = request.POST.get('top-skill')
    if not keyword :
        keyword=''
    elif not top_category:
        top_category=''
    elif not top_skill:
        top_skill=''


    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        context['keyword'] = keyword
        context['top_categories'] = top_category
        context['top_skill'] = top_skill

    return render(request, 'job-list.html', context)
