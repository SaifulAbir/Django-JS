from rest_framework import serializers
from questionnaire_submit.models import Exampaper
#
class QuestionSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exampaper
        fields = ['registration_id','question_id', 'question_text','answers_id','submitted_ans_id']

