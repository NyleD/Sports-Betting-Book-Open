from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# Modelform works with databases
class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['image', 'verified']

    def __init__(self, *args, **kwargs): 
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)                       
        self.fields['verified'].disabled = True

# class GamesUpdateForm(forms.ModelForm):
# Need to add in fiields Probably the Amount of Money Being Used
# Current Bets {Money -> Current Odds -> Game Date/Timings/Score}  
