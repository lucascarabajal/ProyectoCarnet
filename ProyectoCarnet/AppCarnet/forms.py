from .models import Direcciones
from user.models import Usuario
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError



class cargarDireccion(forms.ModelForm):
    class Meta:
        model = Direcciones
        fields = ('nombre', 'numero', 'piso', 'altura')


class cargarPersona(forms.ModelForm):

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'dni', 'nacimiento')
    
class CustomUserCreationForm(forms.Form):     
    

    username = forms.CharField(label='', min_length=4, max_length=35, widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario'}))
    email = forms.EmailField(label='',widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs= {'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs= {'placeholder': 'Confirmar Contraseña'}))
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Usuario.objects.filter(username=username)
        if r.count():
            raise  ValidationError(f"{username} ya existe.Pruebe otro nombre de usuario")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Usuario.objects.filter(email=email)
        if r.count():
            raise  ValidationError(f"{email} ya esta registrado. Pruebe con otro email.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Contraseñas no coinciden")

        return password2

    def save(self, commit=True):
        user = Usuario.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user






"""class CreateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email',error_messages={'exists': 'This already exists!'})
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']"""
