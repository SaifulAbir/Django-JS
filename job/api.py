from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.status import HTTP_200_OK
from rest_framework.utils import json
from .models import Company, Job,Industry,JobType,Experience,Qualification,Gender
from .serializers import *
from rest_framework.response import Response
from rest_framework import generics

class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class JobList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializerAllField

class JobObject(generics.ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):

        queryset = Job.objects.all()
        job = self.kwargs['pk']
        if job is not None:
            queryset = queryset.filter(job_id=job)
        return queryset

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

