from django.db.models import Count
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.utils import json

from .test_serializers import TrendingKeywordsSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from .models import TrendingKeywords


class TrendingKeywordsPopulator(generics.ListCreateAPIView):
    queryset = TrendingKeywords.objects.values('keyword').annotate(key_count=Count('keyword')).order_by('-key_count')
    serializer_class = TrendingKeywordsSerializer


@api_view(["POST"])
def save_trending_keys(request):
    search_data = json.loads(request.body)
    key_obj = TrendingKeywords(**search_data)
    key_obj.save()
    print('HHAHAHAHHAHAHAHAHh')
    return Response(HTTP_200_OK)