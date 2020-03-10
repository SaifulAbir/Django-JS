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
from django.conf import settings
from registration.models import Registration
from resources.strings import *
from resources.strings_registration import *


def checkDuplicateRegistration(professional_id,exam_id):
    reg= Registration.objects.filter(professional=professional_id, exam_id=exam_id, status=REGISTRATION_STATUS_ZERO)

    if reg:
        ERROR_MESSAGE = DUPLICATE_ENTRY_NOT_ALLOWED
        status = False
    else:
        ERROR_MESSAGE = ''
        status = True
    return status
