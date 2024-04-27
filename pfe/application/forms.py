from django import forms
from django.contrib.auth.models import User
from .models import Utilisateur

class LoginForm(forms.Form):
    username = forms.CharField(label='Utilisateur', max_length=255)
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)

class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ('nom', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }

