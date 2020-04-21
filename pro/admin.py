from django.contrib import admin

# Register your models here.
from pro.models import Professional,Religion,Nationality

admin.site.register(Professional)
admin.site.register(Religion)
admin.site.register(Nationality)
