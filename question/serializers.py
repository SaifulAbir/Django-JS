from rest_framework import serializers

from question.models import Topics


class TopicsPopulateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['name']
