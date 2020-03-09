import json

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Topics, SubTopics
from rest_framework.views import APIView
from .serializers import TopicsPopulateSerializer, SubTopicsPopulateSerializer
from rest_framework.response import Response

# class TopicstPopulate(generics.ListAPIView):
#     serializer_class = TopicsPopulateSerializer
#
#     def get_queryset(self):
#
#         queryset = Topics.objects.all()
#         subject = self.kwargs['subject']
#         if subject is not None:
#             queryset = queryset.filter(subject_id=subject)
#             print('hi')
#             print(queryset)
#         return queryset


def topics_populate(reques,subject):
    topic = Topics.objects.get(subject_id = subject)
    data = [{
        'id': str(topic.id) ,
        'name':str(topic.name)
    }]
    print(data)
    return HttpResponse(json.dumps(data), content_type='application/json')

def sub_topics_populate(reques,topic):
    sub_topic = SubTopics.objects.get(topics = topic)
    data = [{
        'id': str(sub_topic.id) ,
        'name':str(sub_topic.name)
    }]
    print(data)
    return HttpResponse(json.dumps(data), content_type='application/json')




# class SubTopicstPopulate(generics.ListAPIView):
#     serializer_class = SubTopicsPopulateSerializer
#
#     def get_queryset(self):
#
#         queryset = SubTopics.objects.all()
#         topic = self.kwargs['topic']
#         if topic is not None:
#             queryset = queryset.filter(topics=topic)
#             print(queryset)
#         return queryset