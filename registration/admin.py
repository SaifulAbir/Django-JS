from django.contrib import admin

# Register your models here.
from registration.models import Registration
class RegistrationAdmin(admin.ModelAdmin):
     list_per_page = 10
     save_as = True

admin.site.register(Registration, RegistrationAdmin)