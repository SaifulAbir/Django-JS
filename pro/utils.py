import random
from django.http import Http404, HttpResponse
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)
from django.db.models import Q
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.template import loader
from p7.settings_dev import *


from pro.models import Professional


def sendSignupEmail(email):
    unique_id = random.randint(100000, 999999)
    updateExamineeVerficationCode(email, unique_id)

    data = ''
    html_message = loader.render_to_string(
        'account_activation_email.html',
        {
            'activation_token': unique_id,
            'subject': 'Thank you from' + data,
        }
    )
    subject_text = loader.render_to_string(
        'account_activation_email_subject.txt',
        {
            'user_name': email,
            'subject': 'Thank you from' + data,
        }
    )

    message = ' it  means a world to us '
    email_from = EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject_text, message, email_from, recipient_list,html_message=html_message)

def updateExamineeVerficationCode(email, unique_id):
    professional = Professional.objects.get(email=email)
    professional.signup_verification_code = unique_id
    professional.save()
