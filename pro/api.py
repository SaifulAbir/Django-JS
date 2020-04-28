import base64
import uuid
import datetime
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
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

from job.serializers import SkillSerializer
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


@api_view(["POST"])
def profile_create_with_user_create(request):
    profile_data = json.loads(request.body)
    try:
        user_obj = User.objects.get(email=profile_data['email'])
    except User.DoesNotExist:
        user_obj = None
    data = {}
    if 'email' not in profile_data:
        data = {
            'status': FAILED_TXT,
            'code': 500,
            "message": EMAIL_BLANK_ERROR_MSG,
            "result": {
                "user": {

                }
            }
        }
    elif 'password' not in profile_data:
        data = {
            'status': FAILED_TXT,
            'code': 500,
            "message": PASSWORD_BLANK_ERROR_MSG,
            "result": {
                "user": {

                }
            }
        }
    elif 'phone' not in profile_data:
        data = {
            'status': FAILED_TXT,
            'code': 500,
            "message": MOBILE_BLANK_ERROR_MSG,
            "result": {
                "user": {

                }
            }
        }
    elif User.objects.filter(email=profile_data['email']).count()>0 and user_obj.is_active == 1 :
        data = {
            'status': FAILED_TXT,
            'code': 500,
            "message": EMAIL_EXIST_ERROR_MSG,
            "result": {
                "user": {
                    'email': profile_data['email']
                }
            }
        }
    elif profile_data['email'] and profile_data['password']:
        try:
            user_obj = User.objects.get(email=profile_data['email'])
        except User.DoesNotExist:
            user_obj = None
        if User.objects.filter(email=profile_data['email']).count()>0 and user_obj.is_active != 1:
            hash_password = make_password(profile_data['password'])
            user = User.objects.get(email=profile_data['email'])
            user.email = profile_data['email']
            user.password = hash_password
            user.username = profile_data['email']
            user.is_active = 0
            user.save()
            if profile_data['terms_and_condition_status'] == ON_TXT:
                profile_data['terms_and_condition_status']=1
            elif profile_data['terms_and_condition_status'] == OFF_TXT:
                profile_data['terms_and_condition_status'] = 0
            del profile_data['confirm_password']
            profile_data['password'] = hash_password
            Professional.objects.filter(email=profile_data['email']).update(**profile_data)
            profile_obj = Professional.objects.get(email=profile_data['email'])
            sendSignupEmail(profile_data['email'],profile_obj.id, datetime.date.today)
            data = {
                'status': 'success',
                'code': HTTP_200_OK,
                "message": 'success message here',  ## will change it later
                "result": {
                    "user": {
                        "email": profile_data['password'],
                        "professional": profile_obj.id
                    }
                }
            }
        else:
            hash_password = make_password(profile_data['password'])
            user = User(email=profile_data['email'], password=hash_password, username=profile_data['email'], is_active=0)
            user.save()
            if profile_data['terms_and_condition_status'] == ON_TXT:
                profile_data['terms_and_condition_status']=1
            elif profile_data['terms_and_condition_status'] == OFF_TXT:
                profile_data['terms_and_condition_status'] = 0
            del profile_data['confirm_password']
            try:
                if profile_data['alert']:
                    alert = profile_data['alert']
                    del profile_data['alert']
            except KeyError:
                alert = None
            profile_obj = Professional(**profile_data)
            profile_obj.password = hash_password
            profile_obj.user_id=user.id
            profile_obj.save()
            if alert == 'on':
                job_alert_save(profile_data['email'])
            sendSignupEmail(profile_data['email'],profile_obj.id, datetime.date.today)
            data = {
                'status': 'success',
                'code': HTTP_200_OK,
                "message": 'success message here', ## will change it later
                "result": {
                    "user": {
                        "email": profile_data['password'],
                        "professional": profile_obj.id
                    }
                }
            }
    return Response(data)

@api_view(["POST"])
def profile_create(request):
    profile_data = json.loads(request.body)
    profile_data['password'] = make_password(profile_data['password'])
    profile_obj = Professional(**profile_data)
    profile_obj.save()
    return Response(HTTP_200_OK)

@api_view(["POST"])
def login(request):
    login_data = json.loads(request.body)
    if login_data["email"] is None or login_data["password"] is None:
        return Response({'error': LOGIN_CREDENTIAL_BLANK_ERROR},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=login_data["email"], password=login_data["password"])
    if not user:
        return Response({'error': LOGIN_CREDENTIAL_ERROR_MSG},
                        status=HTTP_404_NOT_FOUND)
    if login_data['alert'] == 'on':
        job_alert_save(login_data['email'])
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=HTTP_200_OK)

class ProfessionalDetail(APIView):
    permission_classes = (IsAppAuthenticated,)
    def get(self, request, pk):
        profile = get_object_or_404(Professional, pk=pk)
        education = ProfessionalEducation.objects.filter(professional=pk ,is_archived=False)
        skills = ProfessionalSkill.objects.filter(professional=pk, is_archived=False)
        experience = WorkExperience.objects.filter(professional=pk, is_archived=False)
        portfolio = Portfolio.objects.filter(professional=pk, is_archived=False)
        membership = Membership.objects.filter(professional_id=pk, is_archived=False)
        certification = Certification.objects.filter(professional=pk, is_archived=False)
        reference = Reference.objects.filter(professional=pk, is_archived=False)

        info_data = ProfessionalSerializer(profile).data
        info_data['religion_obj'] = ReligionSerializer(profile.religion).data
        info_data['nationality_obj'] = NationalitySerializer(profile.nationality).data
        edu_data = [{
            'id': edu.id,
            'degree': edu.degree_id,
            'institution_obj': InstituteNameSerializer(edu.institution).data,
            'institution_text': edu.institution_text,
            'cgpa': edu.cgpa,
            'major':MajorSerializer(edu.major).data,
            'major_text':edu.major_text,
            'enrolled_date': edu.enrolled_date,
            'graduation_date': edu.graduation_date,
        } for edu in education
        ]

        skill_data = [{
            'id':skill.id,
            'skill_obj': SkillSerializer(skill.skill_name).data,
            'rating': skill.rating,
            'verified_by_skillcheck': skill.verified_by_skillcheck,
        } for skill in skills
        ]
        experience_data = [{
            'id': exp.id,
            'company_text':exp.company_text,
            'company': exp.company_id,
            'designation': exp.designation,
            'start_date': exp.start_date,
            'end_date': exp.end_date,
        } for exp in experience
        ]

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
            'experience_info': experience_data,
            'portfolio_info': portfolio_data,
            'membership_info': membership_data,
            'certification_info': certification_data,
            'reference_data': reference_data

        }
        return Response(prof_data)


# @api_view(["POST"])
# def professional_education_save(request):
#     data = json.loads(request.body)
#
#     key_obj = ProfessionalEducation(**data)
#     key_obj.save()
#
#     return Response(HTTP_200_OK)


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
    if 'institution_id' in data:
        data['institution_obj'] = InstituteNameSerializer(Institute.objects.get(pk=data['institution_id'])).data
    if 'major_id' in data:
        data['major_obj'] = MajorSerializer(Major.objects.get(pk=data['major_id'])).data
    data['id'] = key_obj.id
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



class ProfessionalUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Professional.objects.get(pk=pk)
        except Professional.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        # image uploading code start here
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
        # end of image uploading code

        serializer = ProfessionalSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomPasswordResetView:
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
        """
          Handles password reset tokens
          When a token is created, an e-mail needs to be sent to the user
        """
        # send an e-mail to the user
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            'reset_password_url': "{}/professional/password-reset/{}".format(SITE_URL, reset_password_token.key),
            'site_name': site_shortcut_name,
            'site_domain': SITE_URL
        }

        # render email text
        email_html_message = render_to_string('user_reset_password.html', context)
        email_plaintext_message = render_to_string('user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset for {}".format(site_shortcut_name),
            # message:
            email_plaintext_message,
            # from:
            # "ishraak.office@{}".format(site_url),
            "ishraak.office@gmail.com",
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()



class CustomPasswordTokenVerificationView(APIView):
    """
      An Api View which provides a method to verifiy that a given pw-reset token is valid before actually confirming the
      reset.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = CustomTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        # get token validation time
        password_reset_token_validation_time = get_password_reset_token_expiry_time()

        # find token
        reset_password_token = ResetPasswordToken.objects.filter(key=token).first()

        if reset_password_token is None:
            return Response({'status': 'invalid'}, status=status.HTTP_404_NOT_FOUND)

        # check expiry date
        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            # delete expired token
            reset_password_token.delete()
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)

        # check if user has password to change
        if not reset_password_token.user.has_usable_password():
            return Response({'status': 'irrelevant'})

        return Response({'status': 'OK'})


@api_view(["GET"])
@permission_classes(())
def professional_signup_email_verification(request,token):
    # received_json_data = json.loads(request.body)
    email_start_marker = 'email='
    email_end_marker = '&token='
    email = token[token.find(email_start_marker)+len(email_start_marker):token.find(email_end_marker)]

    token_start_marker = 'token='
    token = token[token.find(token_start_marker)+len(token_start_marker):]
    print(email)
    print(token)

    try:
        professional=Professional.objects.get(email=email, signup_verification_code=token)
        professional.signup_verification_code= ''
        professional.save()
        user = User.objects.get(id=professional.user.id)
        user.is_active = 'True'
        user.save()
        status=HTTP_200_OK
    except Professional.DoesNotExist:
        status=HTTP_404_NOT_FOUND

    if status == HTTP_200_OK:
        message = PROFILE_VERIFICATION_SUCCESS_MESSAGE
    else:
        message = PROFILE_VERIFICATION_FAILED_MESSAGE

    return HttpResponseRedirect("/professional/sign-in/?{}".format(message))

class TokenViewBase(generics.GenericAPIView):
    permission_classes = (IsAppAuthenticated,)
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        try:
            if request.data['alert']:
                alert = request.data['alert']
        except KeyError:
            alert = None

        if alert == 'on':
            job_alert_save(request.data['email'])
        response = Response(serializer.validated_data, status=status.HTTP_200_OK)
        response.set_cookie('access', serializer.validated_data["access"])
        response.set_cookie('refresh', serializer.validated_data["refresh"])
        response.set_cookie('user', serializer.validated_data["user_id"])
        return response

class TokenObtainPairCustomView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainCustomPairSerializer

def logout(request):
    response = HttpResponseRedirect('/professional/sign-in')
    response.delete_cookie('access')
    response.delete_cookie('refresh')
    response.delete_cookie('user')
    return response

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

class ProfessionalUpdatePartial(GenericAPIView, UpdateModelMixin):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

    def put(self,request,pk, *args, **kwargs,):
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
        prof_obj = ProfessionalSerializer(Professional.objects.get(pk=pk)).data
        prof_obj['religion_obj'] = ReligionSerializer(Religion.objects.get(pk = prof_obj['religion'])).data
        prof_obj['nationality_obj'] = NationalitySerializer(Nationality.objects.get(pk = prof_obj['nationality'])).data
        # if 'religion_obj' in request.data:
        #     prof_obj['religion_obj'] = ReligionSerializer(
        #         Religion.objects.get(pk=request.data['religion'])).data
        # if 'nationality_obj' in request.data:
        #     prof_obj['nationality_obj'] = NationalitySerializer(Nationality.objects.get(pk=request.data['nationality'])).data
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
        self.partial_update(request, *args, **kwargs)
        prof_obj = ProfessionalEducationSerializer(ProfessionalEducation.objects.get(pk=pk)).data
        if 'institution_id' in request.data:
            prof_obj['institution_obj'] = InstituteNameSerializer(
                Institute.objects.get(pk=request.data['institution_id'])).data
        else:
            if prof_obj['institution']:
                prof_obj['institution_obj'] = InstituteNameSerializer(
                    Institute.objects.get(pk=prof_obj['institution'])).data
        if 'major_id' in request.data:
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


# @api_view(["GET"])
# def professional_info(request,pk):
#     basic_info = Professional.objects.get(pk=pk)
#     education = ProfessionalEducation.objects.filter(professional=pk)
#     skills = ProfessionalSkill.objects.filter(professional=pk)
#     experience = WorkExperience.objects.filter(professional=pk)
#     portfolio = Portfolio.objects.filter(professional=pk)
#     membership = Membership.objects.filter(professional=pk)
#     certification = Certification.objects.filter(professional=pk)
#     reference = Reference.objects.filter(professional=pk)
#
#     info_data = [ProfessionalSerializer(basic_info).data]
#     edu_data = [{
#         'qualification': str(edu.qualification_id),
#         'institution': str(edu.institution_id),
#         'cgpa': str(edu.cgpa),
#         'major': str(edu.major_id),
#         'enrolled_date': str(edu.enrolled_date),
#         'graduation_date': str(edu.graduation_date),
#     } for edu in education
#     ]
#
#     skill_data = [{
#         'skill': str(skill.name_id),
#         'rating': str(skill.rating),
#         'verified_by_skillcheck': str(skill.verified_by_skillcheck),
#     } for skill in skills
#     ]
#     experience_data = [{
#         'company': str(exp.company_id),
#         'designation': str(exp.designation),
#         'Started_date': str(exp.Started_date),
#         'end_date': str(exp.end_date),
#     } for exp in experience
#     ]
#
#     portfolio_data = [{
#         'name': str(pf.name),
#         'image': str(pf.image),
#         'description': str(pf.description),
#     } for pf in portfolio
#     ]
#
#     membership_data = [{
#         'org_name': str(ms.org_name_id),
#         'position_held': str(ms.position_held),
#         'membership_ongoing': str(ms.membership_ongoing),
#         'Start_date': str(ms.Start_date),
#         'end_date': str(ms.end_date),
#         'desceription': str(ms.desceription),
#     } for ms in membership
#     ]
#
#     certification_data = [{
#         'certification_name': str(cert.certification_name_id),
#         'organization_name': str(cert.organization_name_id),
#         'has_expiry_period': str(cert.has_expiry_period),
#         'issue_date': str(cert.issue_date),
#         'expiry_date': str(cert.expiry_date),
#         'credential_id': str(cert.credential_id),
#         'credential_url': str(cert.credential_url),
#     } for cert in certification
#     ]
#
#     reference_data = [{
#         'name': str(ref.name),
#         'current_position': str(ref.current_position),
#         'email': str(ref.email),
#         'mobile': str(ref.mobile),
#     } for ref in reference
#     ]
#
#
#
#     prof_data={
#         'personal_info':info_data,
#         'edu_info': edu_data,
#         'skill_info': skill_data,
#         'experiecnce_info': experience_data,
#         'portfolio_info': portfolio_data,
#         'membership_info': membership_data,
#         'certification_info': certification_data,
#         'reference_data': reference_data
#
#     }
#
#
#     return HttpResponse(json.dumps(prof_data), content_type='application/json')