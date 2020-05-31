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

from testimonial.urls import *
from pro.api import TokenObtainPairCustomView
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('api/app-dashboard/<int:user_id>', dashboard),
    path('api/profile-info/<int:user_id>', professional_info),
    path('', include('job.urls')),
    path('api/', include('job.urls_api')),
    path('api/', include('pro.urls_api')),
    path('api/', include('registration.urls')),
    path('api/', include('exam.urls')),
    path('api/', include('testimonial.urls')),
    path('api/', include('location.urls')),
    path('api/', include('settings.urls')),
    path('api/', include('question.urls')),
    path('api/', include('exam_paper.urls')),
    path('api/', include('career_advice.urls')),
    path('api/professional/', include('pro.urls')),
    path('professional/', include('pro.urls')),
    path('log/', isLoggedIn),
    path('api/send_email_to_admin_contact_us/', send_email_to_admin_contact_us),
    path('api/sign_in/', TokenObtainPairCustomView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # path('', views.home, name='home'),

    path('career-advice/', TemplateView.as_view(template_name='career_advice.html'), name='career_advice'),
    path('skill-check/', TemplateView.as_view(template_name='skill_check.html'), name='skill_check'),
    path('about-us/', TemplateView.as_view(template_name='about_us.html'), name='about_us'),
    path('contact-us/', TemplateView.as_view(template_name='contact_us.html'), name='contact_us'),
    path('privacy-policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),
    path('terms-and-conditions/', TemplateView.as_view(template_name='terms-and-condition.html'), name='terms-and-condition'),
    path('FAQ/', TemplateView.as_view(template_name='FAQ.html'), name='FAQ'),
    path('my_job_search/', TemplateView.as_view(template_name='my_job_search.html'), name='my_job_search'),
    path('company-dashboard/', TemplateView.as_view(template_name='company_dashboard.html'), name='company_dashboard'),
    path('company-manage-jobs/', TemplateView.as_view(template_name='company_manage_jobs.html'), name='company_manage_jobs'),
    path('company-manage-candidates/', TemplateView.as_view(template_name='company_manage_candidate.html'),name='company_manage_candidates'),
    path('company-shortlisted-candidates/', TemplateView.as_view(template_name='company_shortlisted_candidates.html'),name='company_shortlisted_candidates'),
    path('about-us-app/', TemplateView.as_view(template_name='about_us_app.html')),
    path('contact-us-app/', TemplateView.as_view(template_name='contact_us_app.html')),
    path('career-advice-app/', TemplateView.as_view(template_name='career_advice_app.html')),
    path('FAQ-app/', TemplateView.as_view(template_name='FAQ_app.html')),
    path('company-details/<str:name>/', TemplateView.as_view(template_name='company_details.html'),name='company_details'),
    path('career-advice/details/<int:id>/', TemplateView.as_view(template_name='career_advice_details.html'), name='career_advice_details')

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)