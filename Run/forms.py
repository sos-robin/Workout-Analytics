from django import forms
from django.db import models
from .models import Profile ,Achievement
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'gender','profile_photo']


class AchievementForm(forms.ModelForm):


    class Meta:
        model = Achievement
        fields = [
            'distance_covered', 'time_hours', 'time_minutes', 'time_seconds', 
            'calories_burned', 'average_speed', 'achievement_date', 'achievement_photo'
        ]
        widgets = {
            'distance_covered': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Distance', 'min': '0', 'step': '0.01'}),
            'time_hours': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Hours', 'min': '0', 'step': '1'}),
            'time_minutes': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Minutes', 'min': '0', 'max': '59', 'step': '1'}),
            'time_seconds': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Seconds', 'min': '0', 'max': '59', 'step': '1'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Calories Burned', 'min': '0'}),
            'average_speed': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Average Speed', 'min': '0', 'step': '0.01'}),
            'achievement_date': forms.DateInput(attrs={'class': 'form-control form-control-sm','type': 'date'}),
            'achievement_photo': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
        }

class AchievementSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100, required=False)