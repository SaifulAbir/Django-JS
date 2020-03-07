
from rest_framework import generics
from .models import Topics
from rest_framework.views import APIView
from .serializers import TopicsPopulateSerializer
from rest_framework.response import Response

class TopicstPopulate(generics.ListAPIView):
    serializer_class = TopicsPopulateSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Topics.objects.all()
        subject = self.kwargs['subject']
        if subject is not None:
            queryset = queryset.filter(subject_id=subject)
            print(queryset)
        return queryset