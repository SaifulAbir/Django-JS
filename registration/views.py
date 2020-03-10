from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Registration
from .serializers import RegistrationSerializer
from registration import utils

class RegistrationView(APIView):
    def get(self, request,examinee_id):
        candidateList = utils.getCadidateListFromDb(examinee_id)
        candidateList = RegistrationSerializer(candidateList, many=True)
        return Response({"registration": candidateList.data})


class RegistrationViewSingle(APIView):
    def get(self, request,id):
        singleCadidateDetails = utils.getSingleCadidateDetailsFromDb(id)
        serializer = RegistrationSerializer(singleCadidateDetails, many=True)
        return Response({"registration": serializer.data})