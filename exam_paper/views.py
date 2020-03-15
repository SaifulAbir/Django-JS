from django.db.models import Count, Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.utils import json
from rest_framework.status import (
    HTTP_200_OK
)
from django.utils import timezone
from rest_framework.response import Response

from exam.models import Exam
from registration.models import Registration
from resources.strings import *
from .models import *
from .utils import checkSubmittedAnsRightOrWrong
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView
)

def index(request):
    result = []
    partial_result = Exampaper.objects.values('registration_id').annotate(number_of_correct = Count('correct', filter=Q(correct__gt=0), distinct=True)).annotate(number_of_question_id=Count('question_id'))
    for full_result in partial_result:
        full_result['registration_obj'] = Registration.objects.get(pk = full_result['registration_id'])
        result.append(full_result)
    context = {
        'reg': '',
        'title': 'Latest Posts',
        'result': result,
    }
    return render(request, 'exam_paper/index.html', context)

class ResultListView(ListView):
    template_name = 'exam_paper/result-list.html'
    queryset = Exampaper.objects.all()