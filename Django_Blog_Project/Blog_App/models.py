from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    Title = models.CharField(max_length=255)
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Body = models.TextField()
    Post_Date = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return self.Title + ' | ' + str(self.Author)
    
    
    def get_absolute_url(self):
        #return reverse("details", args=(str(self.id)))
        return reverse('home')