from career_advice.models import CareerAdvice
from django.contrib import admin

# Register your models here.



class CareerAdviceAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'author', 'created_date']
    search_fields = ['title', 'description', 'author', 'created_date']


admin.site.register(CareerAdvice, CareerAdviceAdmin)