from django.conf.urls import url
from django.contrib import admin
from django.contrib.admin import ModelAdmin, AdminSite
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from question.models import Answer
from questionnaire.models import Questionnaire
from registration.models import Registration
from .models import Exampaper, AssignQuestionnaire

# Register your models here.

