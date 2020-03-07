
from rest_framework import generics
from .models import Topics, SubTopics
from rest_framework.views import APIView
from .serializers import TopicsPopulateSerializer, SubTopicsPopulateSerializer
from rest_framework.response import Response

class TopicstPopulate(generics.ListAPIView):
    serializer_class = TopicsPopulateSerializer

    def get_queryset(self):

        queryset = Topics.objects.all()
        subject = self.kwargs['subject']
        if subject is not None:
            queryset = queryset.filter(subject_id=subject)
        return queryset

class SubTopicstPopulate(generics.ListAPIView):
    serializer_class = SubTopicsPopulateSerializer

    def get_queryset(self):

        queryset = SubTopics.objects.all()
        topic = self.kwargs['topic']
        if topic is not None:
            queryset = queryset.filter(topics=topic)
        return queryset