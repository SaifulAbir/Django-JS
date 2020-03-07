from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)

from question.utils import getRandomQuestionnaire
from questionnaire_template.models import Template, TemplateDetails
from resources.strings import *
from exams.models import ExamQuestionnaireDetails, Exam
from questionnaire.models import Questionnaire, QuestionnaireDetail
from registration.models import Registration
from .models import Subject
from .models import Topics
from .models import Difficulties
from .models import Qtype
from .models import Question
from answer.models import Answer
from rest_framework.views import APIView
from .serializers import QuestionSerializer
from rest_framework.response import Response
from question import utils
from sub_topics.models import SubTopics
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
from django.contrib.auth.decorators import login_required, permission_required


class QuestionListWithAnsFromQuestionnaire(APIView):
    def get(self, request,exam_id):

        exmobj = Exam.objects.get(id=exam_id)
        if not exmobj:
            data = {
                'status': FAILED,
                'code': HTTP_404_NOT_FOUND,
                'msg': DATA_NOT_FOUND,
                "data": {
                    "questionListWithAns": [],
                }
            }
            return Response(data, HTTP_404_NOT_FOUND)

        questionnaire=getRandomQuestionnaire(exam_id)
        if not questionnaire:
            data = {
                'status': FAILED,
                'code': HTTP_404_NOT_FOUND,
                'msg': DATA_NOT_FOUND,
                "data": {
                    "questionListWithAns": [],
                }
            }
            return Response(data, HTTP_404_NOT_FOUND)
        else:
            question_list= list(QuestionnaireDetail.objects.filter(questionnaire_id_id=questionnaire.questionnaire_id).values_list('question_id_id', flat=True))
            question = utils.getQuestionListFromDbBasedOnQuestionnareFilter(question_list)
            serializer = QuestionSerializer(question, many=True)
            return Response({"questionListWithAns": serializer.data})
