from django.contrib import admin

# Register your models here.
from job.models import Qualification
from pro.models import Professional, ProfessionalEducation, Institute, Major

admin.site.register(Professional)
admin.site.register(ProfessionalEducation)
admin.site.register(Institute)
admin.site.register(Major)