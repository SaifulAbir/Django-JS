from django.conf import settings
from django.contrib import admin
from django.db import models
from django import forms

# Register your models here.
from job.models import Company, JobType, Experience, Qualification, Gender, Industry, Job, Currency, TrendingKeywords, \
    ApplyOnline
from job.models import Company, JobType, Experience, Qualification, Gender, Industry, Job, Currency , Skill, JobSource, JobCategory, JobGender
from django_admin_listfilter_dropdown.filters import DropdownFilter
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter

class JobAdmin(admin.ModelAdmin):
    filter_horizontal = ('job_skills',) # Many to many field
    list_display = ['title', 'company_name', 'created_at',  'post_date', 'created_by', 'status' ]
    search_fields = ['title__icontains', 'company_name__name__icontains']
    date_hierarchy = 'created_at' # Top filter
    list_per_page = 15
    list_filter = (('created_at', DateRangeFilter),
                   ('post_date', DateRangeFilter),
                   ('status', DropdownFilter),
                   ('created_by', DropdownFilter))
    fields = [('title','status'),'company_name',('address','job_category','application_deadline'),
        ('job_gender','vacancy','experience'),
        ('salary','salary_min','salary_max','currency'),
        'description','responsibilities','education','qualification',
        'additional_requirements','other_benefits',
        ('job_area','job_city','job_country'),'company_profile',
        ('company_area','company_city','company_country'),
        ('job_site','job_nature','job_type'),'job_skills',
        ('job_source_1','job_url_1'),
        ('job_source_2','job_url_2'),
        ('job_source_3','job_url_3'),
        ('created_by','created_at','modified_by','modified_at'),
        ('post_date','review_date','approve_date','publish_date'),
        'raw_content',
        ('slug', 'applied_count', 'favorite_count')]
    readonly_fields = ['slug', 'applied_count', 'favorite_count', 
        'created_by', 'created_at', 'modified_by',
        'modified_at', 'review_date', 'approve_date', 'publish_date']
    # exclude = ["terms_and_condition",] <- use this when 'fields' is not used
    # formfield_overrides = {
    #     models.CharField: {'widget': forms.TextInput(attrs={'size': '40'})}
    # }

    def save_model(self, request, obj, form, change):
        save_model_with_user(self, request, obj, form, change)


def save_model_with_user(self, request, obj, form, change):
    if change:
        obj.modified_by = request.user.username
        if 'is_archived' in form.changed_data and obj.archived_by:
            obj.archived_by = request.user.username
    else:
        obj.created_by = request.user.username
    obj.save()


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'basis_membership_no', 'email', 'web_address', 'organization_head','year_of_eastablishment',
                    'division', 'district']
    search_fields = ['name__icontains', 'basis_membership_no__icontains', 'email__icontains', 'web_address__icontains',
                     'organization_head__icontains', 'organization_head_number__icontains']


    class Media:
        if hasattr(settings, 'GOOGLE_MAPS_API_KEY') and settings.GOOGLE_MAPS_API_KEY:
            css = {
                'all': ('css/admin/location_picker.css',),
            }
            js = (
                'https://maps.googleapis.com/maps/api/js?&libraries=places&key={}'.format(settings.GOOGLE_MAPS_API_KEY),
                'js/admin/location_picker.js',
            )


class TrendingKeywordsAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'location', 'device', 'browser', 'operating_system', 'created_date']
    search_fields = ['keyword', 'location', 'device', 'browser', 'operating_system', 'created_date']
# admin.site.register(Company, CompanyAdmin)



# admin.site.register(ApplyOnline, ApplyOnlineAdmin)
class ApplyOnlineAdmin(admin.ModelAdmin):
    list_display = ['job', 'created_by', 'created_at', 'created_from', 'modified_by', 'modified_at', 'modified_from']
    search_fields = ['job', 'created_by', 'created_at', 'created_from', 'modified_by', 'modified_at', 'modified_from']



@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    fields = ['name', 'created_by', 'created_at', 'modified_by', 'modified_at']
    readonly_fields = ['created_by', 'created_at', 'modified_by', 'modified_at']

    def save_model(self, request, obj, form, change):
        save_model_with_user(self, request, obj, form, change)

@admin.register(JobGender)
class JobGenderAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'created_at']
    fields = ['name', 'created_by', 'created_at', 'modified_by', 'modified_at']
    readonly_fields = ['created_by', 'created_at', 'modified_by', 'modified_at']

    def save_model(self, request, obj, form, change):
        save_model_with_user(self, request, obj, form, change)


@admin.register(JobSource)
class JobSourceAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'url', 'created_by', 'created_at']
    fields = ['name', 'description', 'url', 'created_by', 'created_at', 'modified_by', 'modified_at']
    readonly_fields = ['created_by', 'created_at', 'modified_by', 'modified_at']

    def save_model(self, request, obj, form, change):
        save_model_with_user(self, request, obj, form, change)

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
