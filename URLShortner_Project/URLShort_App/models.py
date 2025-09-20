from django.db import models

class UrlData(models.Model):
    url = models.CharField(max_length=100)
    slug = models.CharField(max_length=20)

    def __str__(self):
        return f"Short URL for: {self.url} is {self.slug}"
    