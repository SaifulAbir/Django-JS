from rest_framework import serializers

from question.models import *


class TopicsPopulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['name']

class SubTopicsPopulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopics
        fields = ['name']


class QtypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ['name']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id','name', 'correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    qtype = QtypeSerializer(many=False)

    class Meta:
        model = Question
        fields = ['id','question','qtype', 'answers']