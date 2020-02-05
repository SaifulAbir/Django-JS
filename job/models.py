from django.db import models

# Create your models here.
class Job(models.Model):
    option_text = models.CharField(max_length=1000)



    def __str__(self):
        return '%d: %s' % (self.id, self.option_text)

    class Meta:
        verbose_name_plural = "Questions Options"