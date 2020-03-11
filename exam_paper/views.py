from django.db.models import Count, Q

from answer.models import Answer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.utils import json
from rest_framework.status import (
    HTTP_200_OK
)
from django.utils import timezone
from assessment import messages_en, settings_dev
from rest_framework.response import Response

from exams.models import Exam
from questionnaire_submit.models import Exampaper
from registration.models import Registration
from resources.strings import *
from .utils import checkSubmittedAnsRightOrWrong
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView
)


@api_view(["POST"])
def exam_submit(request):
    received_json_data = json.loads(request.body)
    examinee_id = received_json_data['examinee_id']
    exam_id = received_json_data['exam_id']

    try:
        reg_obj = Registration.objects.get(candidate_id=examinee_id, exam_id=exam_id, status=REGISTRATION_STATUS_ZERO)
        exam_obj= Exam.objects.get(id=exam_id)
    except Registration.DoesNotExist:
        enrolled_exam_list = []
        data = {
            'status': FAILED,
            'code': HTTP_200_OK,
            "message": DATA_NOT_FOUND,
            "result": []
        }
        return Response(data)

    question_ans_list = received_json_data['question_ans_list']

   # number_of_question = len(question_ans_list)
    for single_question_ans in question_ans_list:
        quesion_ans_model = Exampaper()
        quesion_ans_model.examinee_id = examinee_id
        quesion_ans_model.exam_id = exam_id
        quesion_ans_model.exam_id = exam_id
        quesion_ans_model.registration_id = reg_obj.id
        quesion_ans_model.question_text = single_question_ans['question_text']
        answers =Answer.objects.filter(question_id = single_question_ans['question_id_id'], correct = 1).values_list('id', flat=True).order_by('id')
        answers_list = list(answers)
        answers_list = ','.join(map(str, answers_list))

        quesion_ans_model.answers_id = answers_list
        quesion_ans_model.question_id_id = single_question_ans['question_id_id']
        quesion_ans_model.submitted_ans_id = single_question_ans['submitted_ans_id']
        quesion_ans_model.correct = checkSubmittedAnsRightOrWrong(quesion_ans_model.answers_id,quesion_ans_model.submitted_ans_id)
        quesion_ans_model.created_date = timezone.now()
        quesion_ans_model.save()

    result = Exampaper.objects.filter(registration_id=reg_obj.id, correct= ANS_CORRECT).count()
    number_of_question = Exampaper.objects.filter(registration_id=reg_obj.id).count()
    percentageOfRightAns = (100*result)/number_of_question

    reg_obj.status = REGISTRATION_STATUS_ONE
    reg_obj.percentage_of_correct = percentageOfRightAns

    if int(exam_obj.pass_mark) <= int(percentageOfRightAns):
        reg_obj.result_status = RESULT_STATUS_PASSED
    else:
        reg_obj.result_status = RESULT_STATUS_FAILED

    reg_obj.exam_submitted_date = timezone.now()
    reg_obj.save()

    data = {
            'status': SUCCESS,
            'code': HTTP_200_OK,
            "message": messages_en.SUCCESS,
            "result":{
                'number_of_question' : number_of_question,
                'correct_ans' : result,
                'percentage_of_right_ans' : percentageOfRightAns
            }
        }
    return Response(data)

@api_view(["GET"])
def result(request, registration_id):
    result = Exampaper.objects.filter(registration_id=registration_id, correct = 1).count()
    number_of_question = Exampaper.objects.filter(registration_id=registration_id).count()

    percentageOfRightAns = (100*result)/number_of_question
    data = {
            'status': "ok",
            'code': HTTP_200_OK,
            "message": messages_en.SUCCESS,
            "result":{
                'number_of_question' : number_of_question,
                'correct_ans' : result,
                'percentage_of_right_ans' : percentageOfRightAns
            }
        }
    return Response(data)
