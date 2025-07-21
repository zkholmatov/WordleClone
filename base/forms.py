from django.forms import ModelForm
from .models import Guess, User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']


class GuessForm(ModelForm):
    class Meta:
        model = Guess
        fields = [
            'word',
        ]

    def clean_word(self):
        word = self.cleaned_data.get('word')

        if len(word) != 5:
            raise forms.ValidationError("Not enough letters")

        with open('allowed-guesses.txt') as f:
            valid_words = set(word.strip().upper() for word in f)

        if word.upper() not in valid_words:
            raise forms.ValidationError("Not in word list")

        return word.upper()