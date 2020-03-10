from rest_framework import serializers
from .models import Exam

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['exam_code','exam_name','duration','image','exam_fee','discount_price','discount_percent','instruction']


class FeaturedExamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exam
        fields = '__all__'



class EnrolleedExamSerializer(serializers.ModelSerializer):
    class Meta:

        model = Exam
        fields = ['id','exam_code','exam_name','duration','image','exam_fee','discount_price','discount_percent','instruction']
