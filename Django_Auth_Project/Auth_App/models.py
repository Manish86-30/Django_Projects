from django.db import models

class Employee_Data(models.Model):
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Mobile = models.IntegerField(default=+91)
    Address = models.CharField(max_length=100, null=True)
    City = models.CharField(max_length=100, null=True)
    State = models.CharField(max_length=100, null=True)
    Pincode = models.CharField(max_length=100, null=True)
    Password = models.CharField(max_length=100)