from rest_framework import serializers

from question.models import Topics, SubTopics


class TopicsPopulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['name']

class SubTopicsPopulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTopics
        fields = ['name']


