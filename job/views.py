from django.shortcuts import render
from rest_framework.views import APIView
from .models import Company
from rest_framework.response import Response
from rest_framework import generics

def jobs(request):
    context = {
        'keyword': ''
    }

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        context['keyword'] = request.POST.get('keyword')

    return render(request, 'job-list.html', context)
