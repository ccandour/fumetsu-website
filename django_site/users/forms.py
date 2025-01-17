import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django_password_eye.fields import PasswordEye
from django_password_eye.widgets import PasswordEyeWidget

from .models import Profile


class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=24,
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg focus-ring focus-ring-primary",
            'placeholder': 'Nick'
        })
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg focus-ring focus-ring-primary",
            'placeholder': 'admin@core.pl'
        })
    )

    password1 = PasswordEye(
        required=True, label='Hasło',
        widget=PasswordEyeWidget(
            attrs={
                "class": "form-control form-control-lg focus-ring focus-ring-primary",
                "placeholder": "********",
                "data-bs-toggle": "password"
            }
        )
    )

    password2 = PasswordEye(
        required=True, label='Powtórz hasło',
        widget=PasswordEyeWidget(
            attrs={
                "class": "form-control form-control-lg focus-ring focus-ring-primary",
                "placeholder": "********",
            }
        )
    )

    usable_password = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
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

    password = PasswordEye(
        required=True, label='Hasło',
        widget=PasswordEyeWidget(
            attrs={
                "class": "form-control form-control-lg focus-ring focus-ring-primary",
                "placeholder": "********",
                "data-bs-toggle": "password"
            }
        )
    )

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
        label="E-mail (aby zmienić skontaktuj się z administratorem)",
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'admin@core.pl',
                "class": "form-control form-control-lg focus-ring focus-ring-primary",
                'disabled': 'true'
            }
        )
    )

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        label='Zdjęcie profilowe (max 10MB)',
        error_messages={'invalid': 'Tylko zdj'},
        widget=forms.FileInput(
            attrs={
                "class": "form-control form-control-lg focus-ring focus-ring-primary"
            }
        ),
    )
    color = forms.CharField(
        required=False,
        max_length=7,
        label=mark_safe('Kolor (dostępny dla <a href="https://www.patronite.pl/example" target="_blank">Patronów</a>)'),
        widget=forms.TextInput(
            attrs={
                'placeholder': '#000000',
                "class": "form-control form-control-lg focus-ring focus-ring-primary"
            }
        ),
    )
    description = forms.CharField(
        required=False,
        max_length=1024,
        label=mark_safe('Opis (obsługuje <a href="https://www.markdownguide.org/basic-syntax/" target="_blank">Markdown</a>)'),
        widget=forms.Textarea(
            attrs={
                "placeholder": "Napisz coś o sobie <3",
                "class": "form-control form-control-lg focus-ring focus-ring-primary"
            }
        )
    )

    class Meta:
        model = Profile
        fields = ['image', 'color', 'description']

    def __init__(self, staff=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not staff:
            self.fields['color'].widget.attrs['disabled'] = 'true'


class CustomPasswordChangeForm(PasswordChangeForm):
    error_css_class = 'danger'
    old_password = PasswordEye(
        required=True, label='Stare hasło',
        widget=PasswordEyeWidget(

        )
    )
    new_password1 = PasswordEye(
        required=True, label='Nowe hasło',
        widget=PasswordEyeWidget(
            attrs={
                "class": "form-control form-control-lg focus-ring focus-ring-primary",
                "placeholder": "********",
                "data-bs-toggle": "new-password-1"
            }
        )
    )
    new_password2 = PasswordEye(
        required=True, label='Powtórz nowe hasło',
        widget=PasswordEyeWidget(
            attrs={
                "class": "form-control form-control-lg focus-ring focus-ring-primary",
                "placeholder": "********",
                "autocomplete": "off",
                "data-bs-toggle": "new-password-2"
            }
        )
    )


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="E-mail",
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'admin@core.pl',
                "class": "form-control form-control-lg focus-ring focus-ring-primary"
            }
        )
    )


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = PasswordEye(
        required=True, label='Nowe hasło',
        widget=PasswordEyeWidget(
            attrs={
                "class": "form-control form-control-lg focus-ring focus-ring-primary",
                "placeholder": "********",
                "data-bs-toggle": "new-password-1"
            }
        )
    )
    new_password2 = PasswordEye(
        required=True, label='Powtórz nowe hasło',
        widget=PasswordEyeWidget(
            attrs={
                "class": "form-control form-control-lg focus-ring focus-ring-primary",
                "placeholder": "********",
                "autocomplete": "off",
                "data-bs-toggle": "new-password-2"
            }
        )
    )


class BanForm(forms.ModelForm):
    ban = forms.DateTimeField(initial=datetime.datetime.today)

    class Meta:
        model = Profile
        fields = ['ban']
