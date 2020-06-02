from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.status import HTTP_200_OK
from career_advice.models import *
from career_advice.serializers import CareerAdviceSerializer
from rest_framework.response import Response

class CareerAdviseShow(generics.ListCreateAPIView):
    queryset = CareerAdvice.objects.filter().order_by('-created_date')[:3]
    serializer_class = CareerAdviceSerializer

@api_view(["GET"])
def career_advise(request):
    queryset = CareerAdvice.objects.filter().order_by('-created_date')[:40]

    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 2)
    paginator = Paginator(queryset, page_size)
    current_url = request.GET.get('current_url')
    paginator = Paginator(queryset, page_size)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(1)

    number_of_row_total = paginator.count
    number_of_pages = paginator.num_pages
    start_index = paginator.page(page).start_index()
    end_index = paginator.page(page).end_index()
    check_previous_available_or_not = paginator.page(page).has_previous()
    check_next_available_or_not = paginator.page(page).has_next()
    if check_previous_available_or_not:
        previous_page_number = paginator.page(page).previous_page_number()
    else:
        previous_page_number = 0

    if check_next_available_or_not:
        next_page_number = paginator.page(page).next_page_number()
    else:
        next_page_number = 0
    check_next_available_or_not = paginator.page(page).has_next()


    queryset = CareerAdviceSerializer(queryset, many=True)

    data = {
        'status': 'success',
        'count': number_of_row_total,
        'start_index': start_index,
        'end_index': end_index,
        'number_of_pages': number_of_pages,
        'next_pages': check_next_available_or_not,
        'previous_pages': check_previous_available_or_not,
        'previous_page_number': previous_page_number,
        'next_page_number': next_page_number,
        'code': HTTP_200_OK,
        'current_url': current_url,
        "results": queryset.data,
    }

    return Response(data, HTTP_200_OK)



