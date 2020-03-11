from django.conf import settings
from registration.models import Registration

def checkSubmittedAnsRightOrWrong(actualAns, submittedAns):
    if actualAns == submittedAns:
        return settings.STATIC_TRUE
    else:
        return settings.STATIC_FALSE

def getRegistrationCandidateName(registrationId):
    regObj = Registration.objects.filter(id=registrationId['question_id_id']).order_by('id')
    return regObj.candidate_name
