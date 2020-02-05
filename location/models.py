from django.db import models

# Create your models here.

class Division(models.Model):
    name = models.CharField(max_length=30, primary_key=True)

class District(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
