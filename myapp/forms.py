from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import App

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name', 'apk_file', 'first_screen_screenshot', 
                  'second_screen_screenshot', 'video_recording', 
                  'ui_hierarchy', 'screen_changed']


class AppUpdateForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name', 'apk_file', 'first_screen_screenshot', 
                  'second_screen_screenshot', 'video_recording', 
                  'ui_hierarchy', 'screen_changed']