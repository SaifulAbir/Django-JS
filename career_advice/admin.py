from career_advice.models import Career_Advice
from django.contrib import admin

# Register your models here.



class Career_AdviceAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'author', 'created_date']
    search_fields = ['title', 'description', 'author', 'created_date']


admin.site.register(Career_Advice, Career_AdviceAdmin)