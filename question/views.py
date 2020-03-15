from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
# Create your views here.
from question.models import *
from resources.strings import YES_TEXT
from resources.strings_question import *


def generate_result_csv(df:pd.DataFrame, row_results, row_msgs):
    df['result'] = row_results
    df['msg'] = row_msgs
    return df.to_csv()


def excelimport(request):
    msg = ''
    row_msgs = []
    row_results=[]
    if request.method == 'POST' and request.FILES['excelfile']:


        myfile = request.FILES['excelfile']
        file_type = request.FILES['excelfile'].content_type
        file_type = str(file_type)


        # if file_type != EXCEL_CONTENT_TYPE_XLSX or file_type != EXCEL_CONTENT_TYPE_XLX:
        #     return render(request, 'question/excelimport.html', {
        #         'msg': INVALID_EXCEL_FILE_FORMAT_MSG
        #     })

        exceldata = pd.read_excel(myfile)
        excel_column_list = list(exceldata.columns)
        standard_column_name_with_serial = ['Subject', 'Topic', 'Subtopic', 'Difficulties', 'Type', 'Status',
       'Question', 'Option One', 'Option One Correct', 'Option Two',
       'Option Two Correct', 'Option Three', 'Option Three Correct',
       'Option Four', 'Option Four Correct', 'Option Five',
       'Option Five Correct']

        if standard_column_name_with_serial != excel_column_list:
            return render(request, 'question/excelimport.html', {
                'msg': QUESTION_IMPORT_INVALID_COLUMN_ERROR_MSG
            })
        elif exceldata.empty :
            return render(request, 'question/excelimport.html', {
                'msg': EMPTY_EXCEL_FILE_FORMAT_MSG
            })

        for i in exceldata.index:
            ## Get the subject ID
            try:
                subject_name = exceldata[EXCEL_COLUMN_SUBJECT][i]
                subject=Subject.objects.get(name=subject_name)
            except Exception as ex:
                row_results.append("ERROR")
                row_msgs.append('This subject ' + exceldata[EXCEL_COLUMN_SUBJECT ][i] + ' not found' + str(ex))
                continue

            ## Get the subject ID
            try:
                topic_name = exceldata[EXCEL_COLUMN_TOPIC][i]
                topic=Topics.objects.get(name=topic_name)
            except Topics.DoesNotExist:
                row_results.append("ERROR")
                row_msgs.append('This topic ' + exceldata[EXCEL_COLUMN_TOPIC][i] + ' not found')
                continue

            ## Get the Subtopic ID
            try:
                subtopic_name = exceldata[EXCEL_COLUMN_SUBTOPIC][i]
                sub_topic = SubTopics.objects.get(name=subtopic_name)
            except SubTopics.DoesNotExist:
                row_results.append("ERROR")
                row_msgs.append('This subtopic ' + exceldata[EXCEL_COLUMN_SUBTOPIC][i] + ' not found')
                continue

            ## Get the difficulties ID
            try:
                difficulties = exceldata[EXCEL_COLUMN_DIFFICULTIES][i]
                difficulties = Difficulty.objects.get(name=difficulties)
            except Difficulty.DoesNotExist:
                row_results.append("ERROR")
                row_msgs.append('This difficulty' + exceldata[EXCEL_COLUMN_DIFFICULTIES][i] + ' not found')
                continue

            ## Get the qtype ID
            try:
                type = exceldata[EXCEL_COLUMN_QTYPE][i]
                qtype=QuestionType.objects.get(name=type)
            except QuestionType.DoesNotExist:
                row_results.append("ERROR")
                row_msgs.append('This type' + exceldata[EXCEL_COLUMN_QTYPE][i] + ' not found')
                continue

            # Insert Question && Transaction start from here
            question_text = exceldata[EXCEL_COLUMN_QUESTION][i]

            option_one = exceldata[EXCEL_COLUMN_OPTION_ONE][i]
            option_one_correct = exceldata[EXCEL_COLUMN_OPTION_ONE_CORRECT][i]

            option_two = exceldata[EXCEL_COLUMN_OPTION_TWO][i]
            option_two_correct = exceldata[EXCEL_COLUMN_OPTION_TWO_CORRECT][i]

            option_three = exceldata[EXCEL_COLUMN_OPTION_THREE][i]
            option_three_correct = exceldata[EXCEL_COLUMN_OPTION_THREE_CORRECT][i]

            option_four = exceldata[EXCEL_COLUMN_OPTION_FOUR][i]
            option_four_correct = exceldata[EXCEL_COLUMN_OPTION_FOUR_CORRECT][i]



            question_obj=Question.objects.create(question=question_text, subject=subject, topic=topic, sub_topic=sub_topic, qtype=qtype,
                                    difficulties=difficulties, status=QUESTION_STATUS_PUBLISHED)

            if option_one:
                if option_one_correct == YES_TEXT:
                    option_one_correct = True
                else:
                    option_one_correct = False
                Answer.objects.create(name=option_two, correct=option_one_correct, question=question_obj)

            if option_two:
                if option_two_correct == YES_TEXT:
                    option_two_correct = True
                else:
                    option_two_correct = False
                Answer.objects.create(name=option_one, correct=option_two_correct, question=question_obj)

            if option_three:
                if option_three_correct == YES_TEXT:
                    option_three_correct = True
                else:
                    option_three_correct = False
                Answer.objects.create(name=option_three, correct=option_three_correct, question=question_obj)

            if option_four:
                if option_four_correct == YES_TEXT:
                    option_four_correct = True
                else:
                    option_four_correct = False
                Answer.objects.create(name=option_four, correct=option_four_correct, question=question_obj)

            if exceldata[EXCEL_COLUMN_OPTION_FIVE][i]:
                option_five = exceldata[EXCEL_COLUMN_OPTION_FIVE][i]
                option_five_correct = exceldata[EXCEL_COLUMN_OPTION_FIVE_CORRECT][i]
                if option_five_correct == YES_TEXT:
                    option_five_correct = True
                else:
                    option_five_correct = False
                Answer.objects.create(name=option_five, correct=option_five_correct, question=question_obj)
            ## Transaction End here
            row_results.append("OK")
            row_msgs.append("")

        output_file = generate_result_csv(exceldata, row_results, row_msgs)
        response = HttpResponse(output_file, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="result.xls"'
        return response
    return render(request, 'question/excelimport.html', {
        'msg': msg
    })