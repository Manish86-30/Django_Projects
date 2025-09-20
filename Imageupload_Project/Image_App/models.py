from django.db import models


class ImageFields(models.Model):
    Image = models.ImageField(upload_to="myimage")
    Date = models.DateTimeField(auto_now_add=True)

