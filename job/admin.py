from django.conf import settings
from django.contrib import admin

# Register your models here.
from job.models import Company, JobType, Experience, Qualification, Gender, Industry, Job, Currency, TrendingKeywords, \
    ApplyOnline
from job.models import Company, JobType, Experience, Qualification, Gender, Industry, Job, Currency , Skill, JobSource, JobCategory, JobGender
from django_admin_listfilter_dropdown.filters import DropdownFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

class JobAdmin(admin.ModelAdmin):
    filter_horizontal = ('job_skills',) # Many to many field
    list_display = ['title', 'company_name', 'job_location', 'created_date',  'entry_date', 'application_deadline' ]
    search_fields = ['title__icontains', 'industry__name__icontains', 'employment_status__name__icontains', 'job_location__icontains',
                     'experience__name__icontains', 'qualification__name__icontains', 'gender__name__icontains',
                     'company_name__name__icontains', 'division__name__icontains', 'district__name__icontains', 'zipcode__iexact','entry_date']
    date_hierarchy = 'entry_date' # Top filter
    list_per_page = 15
    list_filter = (('created_date', DateRangeFilter), ('entry_date', DateRangeFilter))
    fields = ['title','company_name',('job_location','job_category','application_deadline'),
        ('job_gender','vacancy','experience'),
        ('salary','salary_min','salary_max','currency'),
        'descriptions','responsibilities','education','qualification',
        'additional_requirements','other_benefits',
        ('job_area','job_city','job_country'),'company_profile',
        ('company_area','company_city','company_country'),
        ('job_site','job_nature','job_type'),'job_skills',
        ('job_source_1','job_url_1'),
        ('job_source_2','job_url_2'),
        ('job_source_3','job_url_3'),
        ('created_by','created_at','modified_by','modified_at'),
        ('post_date','review_date','approve_date','publish_date'),
        'raw_content','status',
        ('slug', 'applied_count', 'favorite_count')]
    readonly_fields = ["slug", "applied_count", "favorite_count", 'created_by','created_at','modified_by','modified_at']
    # exclude = ["terms_and_condition",] <- use this when 'fields' is not used

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
            if not obj.is_archived and form.is_archived:
                obj.archived_by = request.user
        else:
            obj.created_by = request.user
        obj.save()

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

# Added by Munir (02-03).05.2020  >>>
admin.site.register(JobSource)
admin.site.register(JobCategory)
admin.site.register(JobGender)
# <<<
