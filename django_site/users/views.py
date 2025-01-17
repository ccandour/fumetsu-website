import os

import unidecode

from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic.base import TemplateView

from core.forms import CreateComment
from core.models import EpisodeComment
from core.models import StaffCredit, SeriesComment
from core.settings import MEDIA_ROOT
from utils.utils import generate_upload_path
from .forms import *
from .tokens import account_activation_token


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.cleaned_data['username'] = unidecode.unidecode(form.cleaned_data.get('username'))
            user = form.save(commit=False)
            if User.objects.filter(email=form.cleaned_data.get('email')).first() or User.objects.filter(
                    username=form.cleaned_data['username']).first():
                messages.error(request, f'Ten email jest już zarejestrowany.')
                return render(request, '../templates/signup.html', {'form': form})
            else:
                user.is_active = False
                user.username = form.cleaned_data['username']

                user.save()
                # db_user = User.objects.get(username=user.username)
                # Profile.objects.create(user=db_user)

                current_site = get_current_site(request)
                message = render_to_string('../templates/signup_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'protocol': request.scheme,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = f'Aktywacja konta na {os.environ.get("SITE_NAME")}'
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                messages.success(request, f'Na podany adres e-mail został wysłany link aktywacyjny.')
                return redirect('home')
        else:
            if form.has_error('username'):
                messages.error(request, list(form.errors['username']).pop(0))
            elif form.has_error('email'):
                messages.error(request, list(form.errors['email']).pop(0))
            elif form.has_error('password1'):
                messages.error(request, list(form.errors['password1']).pop(0))
            elif form.has_error('password2'):
                messages.error(request, list(form.errors['password2']).pop(0))
            return render(request, '../templates/signup.html', {'form': form})
    else:
        return render(request, '../templates/signup.html', {'form': SignupForm()})


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
        return redirect('home')


def login_cas(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')

            try:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Pomyślnie zalogowano.')
                    return redirect('home')
                else:
                    messages.error(request, f"Nazwa użytkownika lub hasło są nieprawidłowe.")
            except:
                messages.error(request, f"Nazwa użytkownika lub hasło są nieprawidłowe.")
        else:
            messages.error(request, f"Nazwa użytkownika lub hasło są nieprawidłowe.")
    else:
        form = UserLoginForm()
    return render(request, '../templates/login.html', {'form': form})


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
    return render(request, '../templates/password_change.html', {
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
                message = render_to_string('../templates/password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'protocol': request.scheme,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': reset_token,
                })
                mail_subject = f'Resetowanie hasła na {os.environ.get("SITE_NAME")}'
                to_email = mail
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

            messages.success(request, 'Na podany adres e-mail został wysłany link do resetowania hasła.')
            return redirect('home')
    else:
        return render(request, '../templates/password_reset.html', {'form': CustomPasswordResetForm()})


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
            return redirect('home')
        else:
            messages.error(request, 'Nie udało się zmienić hasła.')
            return redirect('home')
    else:
        user = User.objects.get(pk=urlsafe_base64_decode(uidb64))
        form = CustomSetPasswordForm(user)
        return render(request, '../templates/password_reset_confirm.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, f'Pomyślnie wylogowano')
    return redirect('home')


class EditProfile(TemplateView):
    template_name = '../templates/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_staff = True if self.request.user.profile.id in StaffCredit.objects.values_list('user_id',
                                                                                           flat=True) or self.request.user.is_superuser else False

        context['username_form'] = UsernameUpdateForm(instance=self.request.user)
        context['mail_form'] = MailUpdateForm(instance=self.request.user)
        context['p_form'] = ProfileUpdateForm(instance=self.request.user.profile, staff=is_staff)
        context['users'] = self.request.user
        context['r_valid'] = ["<hr>", "<br>", "<a>", "<center>"]

        return context

    def post(self, request, *args, **kwargs):

        username_form = UsernameUpdateForm(request.POST, request.FILES, instance=self.request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=self.request.user.profile)

        # Append image and description to profile form because they end up in the username form (bruh)
        profile_form.files.appendlist('image', username_form.files.get('image'))
        profile_form.data.appendlist('description', username_form.data.get('description'))
        profile_form.data.appendlist('color', username_form.data.get('color'))

        # Username form
        if username_form.is_valid() and username_form.has_changed():
            new_username = username_form.cleaned_data.get('username')

            # Check for duplicate usernames
            if User.objects.filter(username=new_username).count() > 0:
                messages.error(request, f'Taki nick już istnieje')
            else:
                username_form.save()

        # Check for username length
        elif len(request.POST.get("username", "")) > 24:
            messages.error(request, f'Nick jest za długi')

        # Check for illegal characters
        elif not request.POST.get("username", "").isalnum():
            messages.error(request, f'Nick może zawierać tylko litery i cyfry')

        # Save description and image
        if profile_form.is_valid() and (profile_form.has_changed() or profile_form.files.get(
                    'image') != request.user.profile.image):
            profile_form.save()
            request.user.profile.save()

        if (username_form.is_valid() or not username_form.has_changed()) and profile_form.is_valid():
            messages.success(request, f'Zmiany zostały zapisane.')
            return redirect('profile', request.user.username)
        else:
            return redirect('edit_profile')


class ProfilePage(TemplateView):
    model = Profile
    context_object_name = 'posts'
    template_name = '../templates/profile.html'
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q_profile = Profile.objects.prefetch_related(
            Prefetch('staffcredit_set', queryset=StaffCredit.objects.select_related('series'))
        ).get(user__username=self.kwargs['username'])
        q_user = User.objects.get(id=q_profile.user.id)
        q_user.is_staff = StaffCredit.objects.filter(user=q_profile).exists() or q_user.is_superuser
        context['f_user'] = q_user
        context['q_profile'] = q_profile

        credits_list = []
        db_credits = q_profile.staffcredit_set.all()
        for credit in db_credits:
            credit_tuple = (credit.series, credit.role)
            credits_list.append(credit_tuple)
        context['credits'] = list(reversed(sorted(credits_list, key=lambda c: int(c[0].anilist_id)))) if credits_list else []

        context['com_ed'] = CreateComment()
        context['com_ser'] = list(reversed(list(SeriesComment.objects.filter(author=q_user))))
        context['com_ep'] = list(reversed(list(EpisodeComment.objects.filter(author=q_user))))
        context['ban_form'] = BanForm()
        return context