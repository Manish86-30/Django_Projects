from django.db import models
from django.contrib.auth.models import User


class Recipe(models.Model):
    User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    Day = models.CharField(max_length=20, null=True, blank=True)
    Name = models.CharField(max_length=100, default='something')
    Description = models.CharField(max_length=100, default='something')
    