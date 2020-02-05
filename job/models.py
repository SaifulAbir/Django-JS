from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)



divisions = [
    'Dhaka',
    'Chittagong',
]

district = {
    'Dhaka' : ['Dhaka', ],
    'Chittagong': []
}
