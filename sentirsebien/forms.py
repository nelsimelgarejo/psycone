from django.forms import fields
from sentirsebien.models import Perfil, FichaSociodemografica
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2',)

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['universidad', 'tipo_usuario', 'dni']

class FichaSociodemograficaForm(forms.ModelForm):
    class Meta:
        model = FichaSociodemografica
        fields = '__all__'
        exclude = ['id', 'perfil']