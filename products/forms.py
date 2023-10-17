from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Role

class LoginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    role = forms.ChoiceField(
        label='Rola',
        choices=[('Klient', 'Klient'), ('Sprzedawca', 'Sprzedawca')],
        required=False,
    )
