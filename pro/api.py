import base64
import uuid
import datetime
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

from p7.permissions import IsAppAuthenticated
from pro.models import Professional, ProfessionalEducation, ProfessionalSkill, WorkExperience, Portfolio, Membership, \
    Certification, Reference
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from pro.serializers import CustomTokenSerializer, TokenObtainCustomPairSerializer, ProfessionalEducationSerializer
from pro.serializers import ProfessionalSerializer
from resources.strings_pro import *
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from pro.utils import sendSignupEmail
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
            profile_obj = Professional(**profile_data)
            profile_obj.password = hash_password
            profile_obj.user_id=user.id
            profile_obj.save()
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
        membership = Membership.objects.filter(professional=pk, is_archived=False)
        certification = Certification.objects.filter(professional=pk, is_archived=False)
        reference = Reference.objects.filter(professional=pk, is_archived=False)

        info_data = ProfessionalSerializer(profile).data
        edu_data = [{
            'qualification': str(edu.qualification_id),
            'institution': str(edu.institution_id),
            'cgpa': str(edu.cgpa),
            'major': str(edu.major_id),
            'enrolled_date': str(edu.enrolled_date),
            'graduation_date': str(edu.graduation_date),
        } for edu in education
        ]

        skill_data = [{
            'skill': str(skill.name_id),
            'rating': str(skill.rating),
            'verified_by_skillcheck': str(skill.verified_by_skillcheck),
        } for skill in skills
        ]
        experience_data = [{
            'company': str(exp.company_id),
            'designation': str(exp.designation),
            'Started_date': str(exp.Started_date),
            'end_date': str(exp.end_date),
        } for exp in experience
        ]

        portfolio_data = [{
            'name': str(pf.name),
            'image': str(pf.image),
            'description': str(pf.description),
        } for pf in portfolio
        ]

        membership_data = [{
            'org_name': str(ms.org_name_id),
            'position_held': str(ms.position_held),
            'membership_ongoing': str(ms.membership_ongoing),
            'Start_date': str(ms.Start_date),
            'end_date': str(ms.end_date),
            'desceription': str(ms.desceription),
        } for ms in membership
        ]

        certification_data = [{
            'certification_name': str(cert.certification_name_id),
            'organization_name': str(cert.organization_name_id),
            'has_expiry_period': str(cert.has_expiry_period),
            'issue_date': str(cert.issue_date),
            'expiry_date': str(cert.expiry_date),
            'credential_id': str(cert.credential_id),
            'credential_url': str(cert.credential_url),
        } for cert in certification
        ]

        reference_data = [{
            'name': str(ref.name),
            'current_position': str(ref.current_position),
            'email': str(ref.email),
            'mobile': str(ref.mobile),
        } for ref in reference
        ]

        prof_data = {
            'personal_info': info_data,
            'edu_info': edu_data,
            'skill_info': skill_data,
            'experiecnce_info': experience_data,
            'portfolio_info': portfolio_data,
            'membership_info': membership_data,
            'certification_info': certification_data,
            'reference_data': reference_data

        }
        return Response(prof_data)


@api_view(["POST"])
def professional_education_save(request):
    data = json.loads(request.body)

    key_obj = ProfessionalEducation(**data)
    key_obj.save()

    return Response(HTTP_200_OK)

@api_view(["POST"])
def professional_skill_save(request):
    data = json.loads(request.body)

    key_obj = ProfessionalSkill(**data)
    key_obj.save()

    return Response(HTTP_200_OK)

@api_view(["POST"])
def professional_workexperience_save(request):
    data = json.loads(request.body)

    key_obj = WorkExperience(**data)
    key_obj.save()

    return Response(HTTP_200_OK)

@api_view(["POST"])
def professional_portfolio_save(request):
    data = json.loads(request.body)

    key_obj = Portfolio(**data)
    key_obj.save()

    return Response(HTTP_200_OK)

@api_view(["POST"])
def professional_membership_save(request):
    data = json.loads(request.body)

    key_obj = Membership(**data)
    key_obj.save()

    return Response(HTTP_200_OK)

@api_view(["POST"])
def professional_certification_save(request):
    data = json.loads(request.body)

    key_obj = Certification(**data)
    key_obj.save()

    return Response(HTTP_200_OK)

@api_view(["POST"])
def professional_reference_save(request):
    data = json.loads(request.body)

    key_obj = Reference(**data)
    key_obj.save()

    return Response(HTTP_200_OK)



class ProfessionalUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Professional.objects.get(pk=pk)
        except Professional.DoesNotExist:
            raise Http404
    def put(self, request, pk, format=None):
        profile = self.get_object(pk)

        # image uploading code start here
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
            'reset_password_url': "{}/professional/password-reset/{}".format(strings.site_url, reset_password_token.key),
            'site_name': site_shortcut_name,
            'site_domain': site_url
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


class ProfessionalUpdatePartial(GenericAPIView, UpdateModelMixin):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

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