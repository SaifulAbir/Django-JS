from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json

from job.models import Company
from .models import Settings
from .serializers import SettingsSerializer
# from .serializers import DistrictSerializer
from rest_framework.response import Response
from rest_framework import generics

class SettingsList(generics.ListAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
