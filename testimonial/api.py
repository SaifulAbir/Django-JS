import json

from django.http import HttpResponse

from .models import Testimonial
from .serializers import TestimonialSerializer
# from .serializers import DistrictSerializer
from rest_framework.response import Response
from rest_framework import generics


def testimonial_list(request):
    queryset = Testimonial.objects.all()[:5]
    for testimonials in queryset:
        if not testimonials.profile_picture:
            testimonials.profile_picture = "a"

    data=[{
        'client_name': str(testimonial.client_name),
        'comment' : str(testimonial.comment),
        'profile_pic': str(testimonial.profile_picture),
    } for testimonial in queryset
    ]
    return HttpResponse(json.dumps(data), content_type='application/json')
