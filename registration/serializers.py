from rest_framework import serializers

from exam.serializers import ExamSerializer
from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    # candidate_id = serializers.CharField(max_length=250)
    # candidate_name = serializers.CharField(max_length=250)
    # exam_id = serializers.CharField(max_length=250)
    # exam_name = serializers.CharField(max_length=250)
    # duration_in_minutes = serializers.CharField(max_length=250)
    # status = serializers.CharField(max_length=250)
    # created_date = serializers.DateTimeField()
   # exam = serializers.RelatedField(source='exam_registration', read_only=True)

    #This source data comes from choice field
    result_status = serializers.CharField(source='get_result_status_display')
    exam = ExamSerializer(many=False)
    class Meta:
        model = Registration
        fields = ['id','exam','result_status','percentage_of_correct','exam_submitted_date']