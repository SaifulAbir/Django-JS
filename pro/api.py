from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from rest_framework.response import Response
from pro.models import Professional


@api_view(["POST"])
def profile_create(request):
    profile_data = json.loads(request.body)
    profile_data['password'] = make_password(profile_data['password'])
    profile_obj = Professional(**profile_data)
    profile_obj.save()
    return Response(HTTP_200_OK)