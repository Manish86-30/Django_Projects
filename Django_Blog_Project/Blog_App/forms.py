from django import forms
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['Title', 'Author', 'Body']

        widgets = {
            'Title' : forms.TextInput(attrs={'class': 'form-control'}),
            'Author' : forms.Select(attrs={'class': 'form-control'}),
            'Body' : forms.Textarea(attrs={'class': 'form-control'}),
        }



class UserEditForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}


class UserAdminForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}