from django import forms
from django.forms import ModelForm

from .models import *

class BetForm(ModelForm):
    class Meta:
        model = Bet
        fields = ['bet_amt', 'bet_team']