from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.contrib import messages

import os

from fumetsu.forms import CreateComment
from fumetsu.models import StaffCredit, SeriesComment
from django.views.generic.base import TemplateView
from .forms import *
from datetime import datetime, timezone
from fumetsu.models import EpisodeComment
from django.db.models import Q

from django.contrib.auth import authenticate, login, update_session_auth_hash

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from fumetsu.ban import get_color
from django.contrib.auth import logout

import re
import unidecode


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.cleaned_data['username'] = unidecode.unidecode(form.cleaned_data.get('username'))
            user = form.save(commit=False)
            if User.objects.filter(email=form.cleaned_data.get('email')).first() or User.objects.filter(
                    username=form.cleaned_data['username']).first():
                messages.error(request, f'Ten email lub nick już istnieje.')
                return render(request, 'signup.html', {'form': form})
            else:
                user.is_active = False
                user.username = form.cleaned_data['username']
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('signup_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'protocol': request.scheme,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Aktywacja konta na Fumetsu'
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                messages.success(request, f'Na podany adres e-mail został wysłany link aktywacyjny.')
                return redirect('fumetsu-home')
        else:
            messages.error(request, f'Nieprawidłowe dane.')
            return render(request, 'signup.html', {'form': form})
    else:
        return render(request, 'signup.html', {'form': SignupForm()})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Dziękujemy za potwierdzenie e-maila. Możesz się teraz zalogować.')
        return redirect('login')
    else:
        messages.error(request, f'Nieprawidłowy link!')
        return redirect('fumetsu-home')


def login_cas(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')

            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('fumetsu-home')
            except:
                messages.success(request, f"Nie ma takiego konta.")
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Twoje hasło zostało pomyślnie zmienione!')
            return redirect('profile', request.user.username)
        else:
            messages.error(request, 'Zmiana hasła nie powiodła się.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'password_change.html', {
        'form': form
    })


def reset_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data.get('email')
            user = User.objects.filter(email=mail).first()
            if user:
                current_site = get_current_site(request)
                reset_token = default_token_generator.make_token(user)
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'protocol': request.scheme,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': reset_token,
                })
                mail_subject = 'Resetowanie hasła na Fumetsu'
                to_email = mail
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

            messages.success(request, 'Na podany adres e-mail został wysłany link do resetowania hasła.')
            return redirect('fumetsu-home')
    else:
        return render(request, 'password_reset.html', {'form': CustomPasswordResetForm()})


def reset_password_confirm(request, uidb64, token, token_generator=default_token_generator):
    if request.method == 'POST':
        user = User.objects.get(id=urlsafe_base64_decode(uidb64))
        form = CustomSetPasswordForm(request.user, request.POST)

        if form.is_valid() and token_generator.check_token(user, token):
            new_password = form.cleaned_data['new_password2']
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Twoje hasło zostało zmienione.')
            return redirect('fumetsu-home')
        else:
            print(f'User: {user.username} - Token: {token} - Valid: {token_generator.check_token(user, token)}')
            messages.error(request, 'Nie udało się zmienić hasła.')
            return redirect('fumetsu-home')
    else:
        user = User.objects.get(pk=urlsafe_base64_decode(uidb64))
        form = CustomSetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, f'Pomyślnie wylogowano')
    return redirect('fumetsu-home')


class EditProfile(TemplateView):
    template_name = 'edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_staff = True if self.request.user.profile.id in StaffCredit.objects.values_list('user_id', flat=True) or self.request.user.is_superuser else False

        context['username_form'] = UsernameUpdateForm(instance=self.request.user)
        context['mail_form'] = MailUpdateForm(instance=self.request.user)
        context['p_form'] = ProfileUpdateForm(instance=self.request.user.profile, staff=is_staff)
        context['users'] = self.request.user
        context['r_valid'] = ["<hr>", "<br>", "<a>", "<center>"]

        return context

    def post(self, request, *args, **kwargs):

        username_form = UsernameUpdateForm(request.POST, initial={'username': request.user.username})
        profile_form = ProfileUpdateForm(request.POST, request.FILES, initial={'image': request.user.profile.image,
                                                                               'color': request.user.profile.color,
                                                                               'description': request.user.profile.description})

        # Username form
        if username_form.is_valid() and username_form.has_changed():
            new_username = username_form.cleaned_data.get('username')

            # Check for duplicate usernames
            if User.objects.filter(username=new_username).count() > 0:
                messages.error(request, f'Taki nick już istnieje')
            else:
                UsernameUpdateForm(request.POST, instance=request.user).save(commit=True)

        # Check for username length
        elif len(request.POST.get("username", "")) > 24:
            messages.error(request, f'Nick jest za długi')

        # Check for illegal characters
        elif not request.POST.get("username", "").isalnum():
            messages.error(request, f'Nick może zawierać tylko litery i cyfry')

        # Save description and image
        if profile_form.is_valid() and profile_form.has_changed():
            if request.user.profile.image and request.user.profile.image.name != 'default.jpg' and profile_form.cleaned_data.get('image') != request.user.profile.image:
                image_name = request.user.profile.image.name.replace("\\", "/");
                if os.path.exists(image_name):
                    os.remove(image_name)
                request.user.profile.image = 'default.jpg'
                request.user.profile.save()

            ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile).save(commit=True)

        if (username_form.is_valid() or not username_form.has_changed()) and profile_form.is_valid():
            messages.success(request, f'Zmiany zostały zapisane.')
            return redirect('profile', request.user.username)
        else:
            return redirect('edit_profile')


class ProfilePage(TemplateView):
    model = Profile
    context_object_name = 'posts'
    template_name = 'profile.html'
    fields = ['content']

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        q_profile = Profile.objects.get(user__username=self.kwargs['username'])
        q_user = User.objects.get(id=q_profile.user.id)
        q_user.color = get_color(q_user)
        context['f_user'] = q_user
        context['q_profile'] = q_profile

        credits_list = []
        db_credits = StaffCredit.objects.filter(user=q_profile)
        for credit in db_credits:
            credit_tuple = (credit.series, credit.role)
            credits_list.append(credit_tuple)
        context['credits'] = list(reversed(credits_list)) if credits_list else []

        context['com_ed'] = CreateComment()
        context['com_ser'] = list(reversed(list(SeriesComment.objects.filter(author=q_user))))
        context['com_ep'] = list(reversed(list(EpisodeComment.objects.filter(author=q_user))))
        context['ban_form'] = BanForm()
        return context

