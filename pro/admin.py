from django.contrib import admin

# Register your models here.
from pro.models import Professional, ProfessionalEducation, ProfessionalSkill, WorkExperience, Portfolio

admin.site.register(Professional)
admin.site.register(ProfessionalEducation)
admin.site.register(ProfessionalSkill)
admin.site.register(WorkExperience)
admin.site.register(Portfolio)
