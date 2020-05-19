from django.contrib import admin

from p7.models import populate_user_info


class P7Admin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        is_archived = 'is_archived' in form.changed_data and obj.archived_by
        populate_user_info(request, obj, change, is_archived)
        obj.save()