from django.contrib import admin

# Register your models here.
from registration.models import Registration
class RegistrationAdmin(admin.ModelAdmin):
     list_per_page = 10

admin.site.register(Registration, RegistrationAdmin)