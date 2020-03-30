"""p7 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from p7.api import *


from pro.api import TokenObtainPairCustomView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('api/app-dashboard/<int:user_id>', dashboard),
    path('api/profile-info/<int:user_id>', professional_info),
    path('', include('job.urls')),
    path('api/', include('job.urls')),
    path('api/', include('registration.urls')),
    path('api/', include('exam.urls')),
    path('api/', include('location.urls')),
    path('api/', include('question.urls')),
    path('api/', include('exam_paper.urls')),
    path('api/', include('career_advice.urls')),
    path('api/professional/', include('pro.urls')),
    path('professional/', include('pro.urls')),
    path('api/sign_in/', TokenObtainPairCustomView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('career_advise/', TemplateView.as_view(template_name='career_advise.html'), name='career_advise'),
    path('skill_check', TemplateView.as_view(template_name='skill_check.html'), name='skill_check'),
    path('about_us', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
    path('test/', TemplateView.as_view(template_name='home_test.html'), name='home_test'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)