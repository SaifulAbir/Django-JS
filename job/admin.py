from django.contrib import admin

# Register your models here.
from job.models import Company,JobType,Experience,Qualification,Gender,Industry

admin.site.register(Company)
admin.site.register(JobType)
admin.site.register(Experience)
admin.site.register(Qualification)
admin.site.register(Gender)
admin.site.register(Industry)