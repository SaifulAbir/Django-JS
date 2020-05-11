# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import check_password
#
# def checkValidEmailPassword(email, password):
#     user_obj = User.objects.get(username=email)
#     status = check_password(password, user_obj.password)
#     return status
import random
import socket
from urllib.parse import urlparse
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
from resources.strings_pro import *
from difflib import SequenceMatcher


def sendContactUsEmail(name, email, subject, phone, message):

    html_message = loader.render_to_string(
        'contact_us_email_content.html',
        {
            'name': name,
            'email': email,
            'subject': subject,
            'phone': phone,
            'message': message
        }
    )
    subject_text = loader.render_to_string('contact_us_email_subject.txt')

    message = ' it  means a world to us '
    email_from = EMAIL_HOST_USER
    recipient_list = ['rashedhsn16@gmail.com']
    return send_mail(subject_text, message, email_from, recipient_list,html_message=html_message)
