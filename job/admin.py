from django.conf import settings
from django.contrib import admin

# Register your models here.
from job.models import Company, JobType, Experience, Qualification, Gender, Industry, Job, Currency, TrendingKeywords, \
    ApplyOnline
from job.models import Company, JobType, Experience, Qualification, Gender, Industry, Job, Currency , Skill
from django_admin_listfilter_dropdown.filters import DropdownFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

class JobAdmin(admin.ModelAdmin):
    filter_horizontal = ('job_skills',)
    list_display = ['title', 'industry', 'employment_status', 'job_location', 'experience', 'qualification', 'application_deadline',  'company_name', 'entry_date' ]
    search_fields = ['title__icontains', 'industry__name__icontains', 'employment_status__name__icontains', 'job_location__icontains',
                     'experience__name__icontains', 'qualification__name__icontains', 'gender__name__icontains',
                     'company_name__name__icontains', 'division__name__icontains', 'district__name__icontains', 'zipcode__iexact','entry_date']
    date_hierarchy = 'entry_date'
    list_per_page = 15
    list_filter = (('entry_date', DateTimeRangeFilter),)
    readonly_fields = ["slug",]
# class CompanyAdmin(admin.ModelAdmin):
#     list_display = ['name', 'address', 'basis_membership_no', 'email', 'web_address', 'organization_head','year_of_eastablishment',
#                     'division', 'district']
#     search_fields = ['name__icontains', 'basis_membership_no__icontains', 'email__icontains', 'web_address__icontains',
#                      'organization_head__icontains', 'organization_head_number__icontains']



@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'basis_membership_no', 'email', 'web_address', 'organization_head','year_of_eastablishment',
                    'division', 'district']
    search_fields = ['name__icontains', 'basis_membership_no__icontains', 'email__icontains', 'web_address__icontains',
                     'organization_head__icontains', 'organization_head_number__icontains']

    # fieldsets = (
    #     (None, {
    #         'fields': ( 'name', 'profile_picture', 'latitude', 'longitude','created_date')
    #     }),
    # )

    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?&libraries=places&key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )
# admin.site.register(Company, CompanyAdmin)
class TrendingKeywordsAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'location', 'device', 'browser', 'operating_system', 'created_date']
    search_fields = ['keyword', 'location', 'device', 'browser', 'operating_system', 'created_date']
# admin.site.register(Company, CompanyAdmin)



# admin.site.register(ApplyOnline, ApplyOnlineAdmin)
class ApplyOnlineAdmin(admin.ModelAdmin):
    list_display = ['job', 'created_by', 'created_at', 'created_from', 'modified_by', 'modified_at', 'modified_from']
    search_fields = ['job', 'created_by', 'created_at', 'created_from', 'modified_by', 'modified_at', 'modified_from']


# admin.site.register(ApplyOnline, ApplyOnlineAdmin)

admin.site.register(JobType)
admin.site.register(Experience)
admin.site.register(Qualification)
admin.site.register(Gender)
admin.site.register(Industry)
admin.site.register(Currency)
admin.site.register(Job, JobAdmin)
admin.site.register(Skill)
admin.site.register(TrendingKeywords, TrendingKeywordsAdmin)
admin.site.register(ApplyOnline,ApplyOnlineAdmin)
