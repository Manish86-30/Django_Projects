from django.db import models


class Employee(models.Model):
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Mobile = models.IntegerField(default=+91)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Pincode = models.IntegerField(default=0)