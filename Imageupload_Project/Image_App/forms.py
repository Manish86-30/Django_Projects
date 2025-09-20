from django import forms
from .models import ImageFields


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageFields
        fields = '__all__'
        