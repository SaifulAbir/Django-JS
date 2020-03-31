from django.contrib import admin

# Register your models here.
from job.models import Company, JobType, Experience, Qualification, Gender, Industry, Job, Currency, TrendingKeywords
from job.models import Company, JobType, Experience, Qualification, Gender, Industry, Job, Currency , Skill


class JobAdmin(admin.ModelAdmin):
    filter_horizontal = ('job_skills',)
    list_display = ['title', 'industry', 'employment_status', 'job_location', 'experience', 'qualification', 'application_deadline', 'gender', 'company_name',
                    'division', 'district']
    search_fields = ['title__icontains', 'industry__name__icontains', 'employment_status__name__icontains', 'job_location__icontains',
                     'experience__name__icontains', 'qualification__name__icontains', 'gender__name__icontains',
                     'company_name__name__icontains', 'division__name__icontains', 'district__name__icontains', 'zipcode__iexact']

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'basis_membership_no', 'email', 'web_address', 'organization_head','year_of_eastablishment',
                    'division', 'district']
    search_fields = ['name__icontains', 'basis_membership_no__icontains', 'email__icontains', 'web_address__icontains',
                     'organization_head__icontains', 'organization_head_number__icontains']



admin.site.register(Company, CompanyAdmin)
admin.site.register(JobType)
admin.site.register(Experience)
admin.site.register(Qualification)
admin.site.register(Gender)
admin.site.register(Industry)
admin.site.register(Currency)
admin.site.register(Job, JobAdmin)
admin.site.register(Skill)
admin.site.register(TrendingKeywords)
