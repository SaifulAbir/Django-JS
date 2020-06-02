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

@api_view(["GET"])
def job_alert_notification(request):
    data = {}
    if request.user.is_authenticated:
        try:
            user = Professional.objects.get(user = request.user)
        except Professional.DoesNotExist:
            user = None

        if user.job_alert_status == True:
            data = {
                'status': SUBSCRIBED_TXT,
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "email": user.email,
                    }
                }
            }
        else:
            data = {
                'status': NOT_SUBSCRIBED_TXT,
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "email": user.email,
                    }
                }
            }

    else:
        data = {
            'status': NOT_USER_TXT,
            'code': HTTP_401_UNAUTHORIZED,
            "result": {
            }
        }
    return Response(data)



@api_view(["POST"])
def job_alert(request):
    user_email = json.loads(request.body)
    data = {}
    if user_email['email'] and not request.user.is_authenticated:
        try:
            sub_user = Professional.objects.get(email = user_email['email'], job_alert_status = True)
        except Professional.DoesNotExist:
            sub_user = None
        try:
            not_sub_user = Professional.objects.get(email = user_email['email'])
        except Professional.DoesNotExist:
            not_sub_user = None
        if sub_user:
            data = {
                'status': SUBSCRIBED_TXT,
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "email": user_email['email'],
                        "job_alert": sub_user.job_alert_status
                    }
                }
            }
        elif not_sub_user:
            data = {
                'status': NOT_SUBSCRIBED_TXT,
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "email": user_email['email'],
                    }
                }
            }
        else:
            data = {
                'status': NOT_USER_TXT,
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "email": user_email['email'],
                    }
                }
            }
    if request.user.is_authenticated:
        job_alert_save(user_email['email'])
        try:
            sub_user = Professional.objects.get(email = user_email['email'], job_alert_status = True)
        except Professional.DoesNotExist:
            sub_user = None

        if sub_user:
            data = {
                'status': NOT_SUBSCRIBED_USER_TXT,
                'code': HTTP_200_OK,
                "result": {
                    "user": {
                        "email": user_email['email'],
                        "job_alert": sub_user.job_alert_status
                    }
                }
            }
    return Response(data)


@api_view(["POST"])
def professional_education_save(request):
    data = json.loads(request.body)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    data.update({'created_by_id': request.user.id, 'created_at': str(ip)})
    key_obj = ProfessionalEducation(**data)
    key_obj.save()
    if 'institution_id' in data and data['institution_id'] is not None:
        data['institution_obj'] = InstituteNameSerializer(Institute.objects.get(pk=data['institution_id'])).data
    if 'major_id' in data and data['major_id'] is not None:
        data['major_obj'] = MajorSerializer(Major.objects.get(pk=data['major_id'])).data
    data['id'] = key_obj.id
    data['degree'] = data["degree_id"]
    del data["degree_id"]
    return Response(data)

@api_view(["POST"])
def professional_skill_save(request):

    data = json.loads(request.body)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    data.update({'created_by_id': request.user.id,'created_at': str(ip)})
    key_obj = ProfessionalSkill(**data)
    key_obj.save()
    data['skill_obj']= SkillSerializer(Skill.objects.get(pk=data['skill_name_id'])).data
    data['id'] = key_obj.id
    return Response(data)

@api_view(["POST"])
def professional_workexperience_save(request):
    data = json.loads(request.body)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    data.update({'created_by_id': request.user.id, 'created_at': str(ip)})
    key_obj = WorkExperience(**data)
    key_obj.save()
    data['id'] = key_obj.id
    return Response(data)

@api_view(["POST"])
def professional_portfolio_save(request):
    data = json.loads(request.body)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    data.update({'created_by_id': request.user.id, 'created_at': str(ip)})
    if 'image' in data:
        img_base64 = data['image']
        if img_base64:
            format, imgstr = img_base64.split(';base64,')
            ext = format.split('/')[-1]
            filename = str(uuid.uuid4()) + '-professional.' + ext
            image_data = ContentFile(base64.b64decode(imgstr), name=filename)
            fs = FileSystemStorage()
            filename = fs.save(filename, image_data)
            uploaded_file_url = fs.url(filename)
            data['image'] = uploaded_file_url
    key_obj = Portfolio(**data)
    key_obj.save()
    data['id'] = key_obj.id
    return Response(data)

@api_view(["POST"])
def professional_membership_save(request):
    data = json.loads(request.body)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    data.update({'created_by_id': request.user.id, 'created_at': str(ip)})
    key_obj = Membership(**data)
    key_obj.save()
    data['id'] = key_obj.id
    return Response(data)

@api_view(["POST"])
def professional_certification_save(request):
    data = json.loads(request.body)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    data.update({'created_by_id': request.user.id, 'created_at': str(ip)})
    key_obj = Certification(**data)
    key_obj.save()
    data['id'] = key_obj.id
    return Response(data)

@api_view(["POST"])
def professional_reference_save(request):
    data = json.loads(request.body)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    data.update({'created_by_id': request.user.id, 'created_at': str(ip)})
    key_obj = Reference(**data)
    key_obj.save()
    data['id'] = key_obj.id
    return Response(data)

class EducationUpdateDelete(GenericAPIView, UpdateModelMixin):
    queryset = ProfessionalEducation.objects.all()
    serializer_class = ProfessionalEducationSerializer

    def put(self, request,pk, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.data.update(
            {'modified_by_id': request.user.id, 'modified_at': str(ip), 'modified_date': timezone.now()})
        if "degree_id" in request.data:
            request.data["degree"] = request.data["degree_id"]
            del request.data["degree_id"]
        if "institution_id" in request.data:
            request.data["institution"] = request.data["institution_id"]
            del request.data["institution_id"]
        if "major_id" in request.data:
            request.data["major"] = request.data["major_id"]
            del request.data["major_id"]
        if 'is_ongoing' in request.data and request.data['is_ongoing'] == True:
            request.data['graduation_date'] = None
        self.partial_update(request, *args, **kwargs)
        prof_obj = ProfessionalEducationSerializer(ProfessionalEducation.objects.get(pk=pk)).data
        if 'institution' in request.data and request.data['institution'] is not None:
            prof_obj['institution_obj'] = InstituteNameSerializer(
                Institute.objects.get(pk=request.data['institution'])).data
        else:
            if prof_obj['institution']:
                prof_obj['institution_obj'] = InstituteNameSerializer(
                    Institute.objects.get(pk=prof_obj['institution'])).data
        if 'major_id' in request.data and request.data['major_id'] is not None:
            prof_obj['major_obj'] = MajorSerializer(Major.objects.get(pk=request.data['major_id'])).data
        else:
            if prof_obj['major']:
                prof_obj['major_obj'] = MajorSerializer(Major.objects.get(pk=prof_obj['major'])).data

        return Response(prof_obj)

class SkillUpdateDelete(GenericAPIView, UpdateModelMixin):
    queryset = ProfessionalSkill.objects.all()
    serializer_class = ProfessionalSkillSerializer

    def put(self, request,pk, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.data.update({'modified_by_id': request.user.id, 'modified_at': str(ip),'modified_date':timezone.now()})
        self.partial_update(request, *args, **kwargs)
        prof_obj = ProfessionalSkillSerializer(ProfessionalSkill.objects.get(pk=pk)).data
        prof_obj['rating'] = Decimal(prof_obj['rating'])
        if 'skill_name_id' in request.data:
            prof_obj['skill_obj'] = SkillSerializer(Skill.objects.get(pk=request.data['skill_name_id'])).data
        else:
            prof_obj['skill_obj'] = SkillSerializer(Skill.objects.get(pk=prof_obj['skill_name'])).data
        return Response(prof_obj)

class WorkExperienceUpdateDelete(GenericAPIView, UpdateModelMixin):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer

    def put(self, request,pk, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.data.update(
            {'modified_by_id': request.user.id, 'modified_at': str(ip), 'modified_date': timezone.now()})
        if "company_id" in request.data:
            request.data["company"] = request.data["company_id"]
            del request.data["company_id"]
        self.partial_update(request, *args, **kwargs)
        prof_obj = WorkExperienceSerializer(WorkExperience.objects.get(pk=pk)).data

        return Response(prof_obj)

class PortfolioUpdateDelete(GenericAPIView, UpdateModelMixin):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def put(self, request,pk, *args, **kwargs):
        if 'image' in request.data:
            img_base64 = request.data['image']
            if img_base64:

                format, imgstr = img_base64.split(';base64,')
                ext = format.split('/')[-1]
                filename = str(uuid.uuid4()) + '-professional.' + ext
                data = ContentFile(base64.b64decode(imgstr), name=filename)
                fs = FileSystemStorage()
                filename = fs.save(filename, data)
                uploaded_file_url = fs.url(filename)
                request.data['image'] = uploaded_file_url
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.data.update(
            {'modified_by_id': request.user.id, 'modified_at': str(ip), 'modified_date': timezone.now()})
        self.partial_update(request, *args, **kwargs)
        prof_obj = PortfolioSerializer(Portfolio.objects.get(pk=pk)).data
        return Response(prof_obj)

class MembershipUpdateDelete(GenericAPIView, UpdateModelMixin):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    def put(self, request,pk, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.data.update(
            {'modified_by_id': request.user.id, 'modified_at': str(ip), 'modified_date': timezone.now()})
        self.partial_update(request, *args, **kwargs)
        prof_obj = MembershipSerializer(Membership.objects.get(pk=pk)).data
        return Response(prof_obj)

class CertificationUpdateDelete(GenericAPIView, UpdateModelMixin):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer

    def put(self, request,pk, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.data.update(
            {'modified_by_id': request.user.id, 'modified_at': str(ip), 'modified_date': timezone.now()})
        self.partial_update(request, *args, **kwargs)
        prof_obj = CertificationSerializer(Certification.objects.get(pk=pk)).data
        return Response(prof_obj)

class ReferenceUpdateDelete(GenericAPIView, UpdateModelMixin):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer

    def put(self, request,pk, *args, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.data.update(
            {'modified_by_id': request.user.id, 'modified_at': str(ip), 'modified_date': timezone.now()})
        self.partial_update(request, *args, **kwargs)
        prof_obj = ReferenceSerializer(Reference.objects.get(pk=pk)).data
        return Response(prof_obj)


class EducationObject(APIView):
    permission_classes = (IsAppAuthenticated,)
    def get(self, request, pk):
        education = ProfessionalEducationSerializer(get_object_or_404(ProfessionalEducation, pk=pk)).data
        edu_data = {
            'edu_info': education,
        }
        return Response(edu_data)


class ReligionList(generics.ListCreateAPIView):
    queryset = Religion.objects.all()
    serializer_class = ReligionSerializer

class NationalityList(generics.ListCreateAPIView):
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer

class InstituteList(generics.ListCreateAPIView):
    queryset = Institute.objects.all()
    serializer_class = InstituteNameSerializer

class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationNameSerializer

class MajorList(generics.ListCreateAPIView):
    queryset = Major.objects.all()
    serializer_class = MajorSerializer

class CertificateNameList(generics.ListCreateAPIView):
    queryset = CertificateName.objects.all()
    serializer_class = CertificateNameSerializer



class SkillObject(APIView):
    def get(self, request, pk):
        skill = ProfessionalSkillSerializer(get_object_or_404(ProfessionalSkill, pk=pk)).data
        skill_data = {
            'skill_info': skill,
        }
        return Response(skill_data)




def StaticUrl(self):
    data = {
        '1': "http://facebook.com/",
        '2': "http://twitter.com/",
        '3': "http://linkedin.com/",

    }
    return HttpResponse(json.dumps(data), content_type='application/json')


api_view('GET')
def institute_search(request):
    names = list(Institute.objects.values_list('name',flat=True))
    return HttpResponse(json.dumps(names),'application/json')
