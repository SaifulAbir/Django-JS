from django.contrib import admin

# Register your models here.
from job.models import Company, JobType, Experience, Qualification, Gender, Industry, Job


class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'industry', 'employment_status', 'job_location', 'experience', 'qualification', 'gender', 'company_name',
                    'division', 'district']
    search_fields = ['title__icontains', 'industry__name__icontains', 'employment_status__name__icontains', 'job_location__icontains',
                     'experience__name__icontains', 'qualification__name__icontains', 'gender__name__icontains',
                     'company_name__name__icontains', 'division__name__icontains', 'district__name__icontains', 'zipcode__iexact']


admin.site.register(Company)
admin.site.register(JobType)
admin.site.register(Experience)
admin.site.register(Qualification)
admin.site.register(Gender)
admin.site.register(Industry)
admin.site.register(Job, JobAdmin)