from django.contrib import admin
from .models import ImageFields



@admin.register(ImageFields)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'Image', 'Date')