from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK
)

from question.models import Question

def getQuestionListFromDb():
    questionList = Question.objects.all()
    return questionList

def getQuestionListFromDbBasedOnQuestionnareFilter(question_list):
    questionList= Question.objects.all().filter(pk__in=question_list).order_by('-id')
    return questionList

def getRandomQuestionnaire(exam_id):
    questionnaire = ExamQuestionnaireDetails.objects.filter(exam_id=exam_id).order_by("?").first()
    return questionnaire




