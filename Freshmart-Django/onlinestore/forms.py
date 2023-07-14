from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    phone_number = forms.CharField(max_length=11, help_text='Required. Enter a valid phone number.')

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2',]


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'Middle_name', 'last_name', 'gender',)
