from rest_framework import serializers
from .models import TrendingKeywords
from rest_framework.validators import *


class TrendingKeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendingKeywords
        fields = ['keyword']
