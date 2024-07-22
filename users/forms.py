from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from django_recaptcha.fields import ReCaptchaField, ReCaptchaV2Checkbox
import datetime


class SignupForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'email',
    })
    )

    username = forms.CharField(
        max_length=24,
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Login',
        })
    )

    password1 = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Hasło'})
    )

    password2 = forms.CharField(
        label="Powtórz hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Powtórz hasło'})
    )

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={
    #        'data-theme': 'dark',
    #    })) 

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=24,
        label="Nazwa użytkownika",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Nazwa użytkownika"
            }
        )
    )

    password = forms.CharField(widget=forms.PasswordInput())

    #captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={
    #        'data-theme': 'dark',
    #    }))

    class Meta:
        fields = ['username', 'password']


class UsernameUpdateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=24,
        label="Nazwa użytkownika",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nick',
                "class": "form-control form-control-lg focus-ring focus-ring-primary"
            }
        )
    )

    class Meta:
        model = User
        fields = ['username']


class MailUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=100,
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'admin@fumetsu.pl',
                "class": "form-control form-control-lg focus-ring focus-ring-primary"
            }
        )
    )

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(
        label='Zdjęcie profilowe', required=False,
        error_messages={'invalid': 'Tylko zdj'},
        widget=forms.FileInput(
            attrs={
                "class": "form-control form-control-lg focus-ring focus-ring-primary"
            }
        )
    )
    description = forms.CharField(
        max_length=1024,
        label="Opis",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Napisz coś o sobie <3",
                "class": "form-control form-control-lg focus-ring focus-ring-primary"
            }
        )
    )

    class Meta:
        model = Profile
        fields = ['image', 'description']


class BanForm(forms.ModelForm):
    ban = forms.DateTimeField(initial=datetime.datetime.today)

    class Meta:
        model = Profile
        fields = ['ban']
