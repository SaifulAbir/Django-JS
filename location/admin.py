from django.contrib import admin

# Register your models here.
from location.models import Division, District

admin.site.register(Division)
admin.site.register(District)