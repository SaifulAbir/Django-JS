from django.utils import timezone
from django.db import models

class P7Model(models.Model):
    created_by = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(null=True)
    created_from = models.CharField(max_length=255, null=True)
    modified_by = models.CharField(max_length=255, null=True)
    modified_at = models.DateTimeField(auto_now=True)
    modified_from = models.CharField(max_length=255, null=True)
    is_archived = models.BooleanField(default=False)
    archived_by = models.CharField(max_length=255, null=True)
    archived_at = models.DateTimeField(null=True)
    archived_from = models.CharField(max_length=255, null=True)

    class Meta:
        abstract = True

def populate_time_info(sender, instance, *args, **kwargs):
    if instance._state.adding:
        instance.created_at = timezone.now()
    else:
        instance.modified_at = timezone.now()
        if instance.is_archived and not instance.archived_at:
            instance.archived_at = timezone.now()


def populate_user_info(request, instance, is_changed, is_archived):
    if is_changed:
        instance.modified_by = request.user.username
        if is_archived:
            instance.archived_by = request.user.username
    else:
        instance.created_by = request.user.username
