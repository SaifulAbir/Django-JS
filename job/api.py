from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from .models import Company, Job,Industry,JobType,Experience,Qualification,Gender
from .serializers import CompanySerializer, IndustrySerializer, JobTypeSerializer, QualificationSerializer, \
    ExperienceSerializer, GenderSerializer, JobSerializer
from rest_framework.response import Response
from rest_framework import generics


# @api_view(["POST"])
# def joblist(request):
#     received_json_data = json.loads(request.body)
#     email = received_json_data["email"]
#
#     data = {
#         'status': 1,
#         'code': 200,
#         "message": 'ok',
#         "result": {
#             "user": {
#                 "email": email
#             }
#         }
#     }
#
#     return Response(data)


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class IndustryList(generics.ListCreateAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class JobTypeList(generics.ListCreateAPIView):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

class ExperienceList(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class QualificationList(generics.ListCreateAPIView):
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer

class GenderList(generics.ListCreateAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer

@api_view(["POST"])
def job_create(request):
    job_data = json.loads(request.body)
    job_obj = Job(**job_data)
    job_obj.save()
    return Response(HTTP_200_OK)

class JobUpdateView(GenericAPIView, UpdateModelMixin):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

