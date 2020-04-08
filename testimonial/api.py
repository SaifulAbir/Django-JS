import json

from django.http import HttpResponse
from rest_framework.decorators import api_view

from .models import Testimonial
from .serializers import TestimonialSerializer
# from .serializers import DistrictSerializer
from rest_framework.response import Response
from rest_framework import generics

@api_view(["GET"])
def testimonial_list(request):
    queryset = Testimonial.objects.all()[:6]
    for testimonials in queryset:
        if not testimonials.profile_picture:
            testimonials.profile_picture = "testimonials/alternate.png"

    data=[{
        'client_name': str(testimonial.client_name),
        'comment' : str(testimonial.comment),
        'profile_picture': 'media/'+str(testimonial.profile_picture),
    } for testimonial in queryset
    ]
    return HttpResponse(json.dumps(data), content_type='application/json')
