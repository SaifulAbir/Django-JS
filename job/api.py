from rest_framework.decorators import api_view
from rest_framework.utils import json
from .models import Company, Job
from .serializers import JobSerializer
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


# class CompanyList(generics.ListCreateAPIView):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer

class JobList(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer



