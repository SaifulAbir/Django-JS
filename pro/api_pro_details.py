import base64

from decimal import Decimal
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import serializers
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework import parsers, renderers, status, generics
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from rest_framework.utils import json
from rest_framework.response import Response
from rest_framework.views import APIView
from django_rest_passwordreset.views import get_password_reset_token_expiry_time

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from job.models import FavouriteJob, ApplyOnline, Job
from job.serializers import SkillSerializer, JobSerializer
from p7.permissions import IsAppAuthenticated
from p7.settings_dev import SITE_URL
from pro.models import Professional, Religion, Nationality
from pro.models import Professional, ProfessionalEducation, ProfessionalSkill, WorkExperience, Portfolio, Membership, \
    Certification, Reference
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from pro.serializers import *
from pro.serializers import ProfessionalSerializer
from resources.strings_pro import *
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from pro.utils import sendSignupEmail, job_alert_save
from resources.strings_pro import *


class ProfessionalDetail(generics.ListAPIView):
    permission_classes = (IsAppAuthenticated,)
    def get(self, request, pk):

        profile = get_object_or_404(Professional, pk=pk)
        education = ProfessionalEducation.objects.filter(professional=pk ,is_archived=False).order_by('-enrolled_date')
        skills = ProfessionalSkill.objects.filter(professional=pk, is_archived=False)
        experience = WorkExperience.objects.filter(professional=pk, is_archived=False).order_by("-start_date")
        portfolio = Portfolio.objects.filter(professional=pk, is_archived=False)
        membership = Membership.objects.filter(professional_id=pk, is_archived=False)
        certification = Certification.objects.filter(professional=pk, is_archived=False).order_by("-issue_date")
        reference = Reference.objects.filter(professional=pk, is_archived=False)
        info_data = ProfessionalSerializer(profile).data
        info_data['religion_obj'] = ReligionSerializer(profile.religion).data
        info_data['nationality_obj'] = NationalitySerializer(profile.nationality).data
        work_experience_data = WorkExperienceDetailSerializer(experience, many=True).data


        edu_data = [{
            'id': edu.id,
            'degree': edu.degree_id,
            'institution_obj': InstituteNameSerializer(edu.institution).data,
            'institution_text': edu.institution_text,
            'cgpa': edu.cgpa,
            'major_obj':MajorSerializer(edu.major).data,
            'major_text':edu.major_text,
            'enrolled_date': edu.enrolled_date,
            'graduation_date': edu.graduation_date,
            'description': edu.description,
            'is_ongoing' :edu.is_ongoing
        } for edu in education
        ]

        skill_data = [{
            'id':skill.id,
            'skill_obj': SkillSerializer(skill.skill_name).data,
            'rating': skill.rating,
            'verified_by_skillcheck': skill.verified_by_skillcheck,
        } for skill in skills
        ],


        portfolio_data = [{
            'id': pf.id,
            'name': pf.name,
            'image': pf.image,
            'description': pf.description,
        } for pf in portfolio
        ]

        membership_data = [{
            'id':ms.id,
            'organization': ms.organization,
            'position_held': ms.position_held,
            'membership_ongoing': ms.membership_ongoing,
            'start_date': ms.start_date,
            'end_date': ms.end_date,
            'description': ms.description,
        } for ms in membership
        ]

        certification_data = [{
            'id': cert.id,
            'certificate_name': cert.certificate_name,
            'organization': cert.organization,
            'has_expiry_period': cert.has_expiry_period,
            'issue_date': cert.issue_date,
            'expiry_date': cert.expiry_date,
            'credential_id': cert.credential_id,
            'credential_url': cert.credential_url,
        } for cert in certification
        ]

        reference_data = [{
            'id':ref.id,
            'description':ref.description
        } for ref in reference
        ]

        prof_data = {
            'personal_info': info_data,
            'edu_info': edu_data,
            'skill_info': skill_data,
            'experience_info': work_experience_data,
            'portfolio_info': portfolio_data,
            'membership_info': membership_data,
            'certification_info': certification_data,
            'reference_data': reference_data

        }
        return Response(prof_data)
