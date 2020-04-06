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
from pro.models import Professional
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from pro.serializers import CustomTokenSerializer, TokenObtainCustomPairSerializer
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
        data = ProfessionalSerializer(profile).data
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


