from django import forms
from .models import TrackerModel, profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TrackerForm(forms.ModelForm):
    
    class Meta:
        model = TrackerModel
        fields = ['date', 'category', 'amount', 'description']
        

class CustomUserCreation(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateFrom(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['img']

class FilterForm(forms.Form):
    choice = {
        'last': 'Last->First',
        'first': 'First->Last'
    }
    sort_by = forms.ChoiceField(choices=choice)
    from_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))