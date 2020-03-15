from django.conf import settings
from registration.models import Registration
from resources.config import *


def checkSubmittedAnsRightOrWrong(actualAns, submittedAns):
    if actualAns == submittedAns:
        return STATIC_TRUE
    else:
        return STATIC_FALSE
