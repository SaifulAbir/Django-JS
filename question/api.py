import json

from django.http import HttpResponse

from questionnaire.models import QuestionnaireDetail
from resources.strings import *
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from exam.models import Exam, ExamQuestionnaireDetails
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)


def topics_populate(reques,subject):
    topic = Topics.objects.get(subject_id = subject)
    data = [{
        'id': str(topic.id) ,
        'name':str(topic.name)
    }]
    print(data)
    return HttpResponse(json.dumps(data), content_type='application/json')

def sub_topics_populate(reques,topic):
    sub_topic = SubTopics.objects.get(topics = topic)
    data = [{
        'id': str(sub_topic.id) ,
        'name':str(sub_topic.name)
    }]
    print(data)
    return HttpResponse(json.dumps(data), content_type='application/json')

class QuestionListWithAns(APIView):
    def get(self, request):
        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response({"questionListWithAns": serializer.data})

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

        questionnaire = ExamQuestionnaireDetails.objects.filter(exam_id=exam_id).order_by("?").first()
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
            question = Question.objects.all().filter(pk__in=question_list).order_by('-id')
            serializer = QuestionSerializer(question, many=True)
            return Response({"questionListWithAns": serializer.data})
