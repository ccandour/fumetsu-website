from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import os
from django.shortcuts import get_object_or_404

from fumetsu.models import Series_comment, Key_map
from django.views.generic.base import TemplateView
from anime.forms import *
from .forms import *
from datetime import datetime, timezone
from anime.models import Episode_comment
from django.db.models import Q

from django.contrib.auth import authenticate, login

from django.contrib.auth.backends import ModelBackend


from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from fumetsu.ban import check_ban, Get_color
from django.contrib.auth import logout

import re
import unidecode


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.cleaned_data['username'] = unidecode.unidecode(form.cleaned_data.get('username'))
            user = form.save(commit=False)
            if User.objects.filter(email = form.cleaned_data.get('email')).first() or User.objects.filter(username = form.cleaned_data['username']).first():
                messages.success(request, f'Ten email lub nick już istnieje.')
                return render(request,'users/signup.html', {'form':form})
            else:

                user.is_active = False
                user.username = form.cleaned_data['username']
                user.save()
                current_site = get_current_site(request)
                message = render_to_string('users/acc_active_email.html', {
                    'user':user, 
                    'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                mail_subject = 'Aktywuj konto do Fumetsu-subs.'
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                return render(request,'users/confirm_email.html')

    else:
        form = SignupForm()
    
    return render(request, 'users/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
        return HttpResponse('Dziękujemy za potwierdzenie e-mailu. Możesz się teraz zalogować.')
    else:
        return HttpResponse('Nieprawidłowy link!')


def login_cas(request):

    if request.method == 'POST':
        form = UserLoginForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('username')

            try:
                users = User.objects.get(username=username)
                if users.is_active == False:
                    now = datetime.now(timezone.utc)
                    q_user = Profile.objects.filter(user=users)
                    q_users = q_user.filter(Q(ban__isnull=True) | Q(ban__gt=now))
                    if q_users.count() > 0 and q_user.first().ban != None:
                        messages.success(request, f"jesteś zbanowany do {q_users.first().ban}")
                    else:
                        users.is_active = True
                        users.save()


                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('fumetsu-home')
            except:
                messages.success(request, f"Nie ma takiego konta.")
        else:
            return render(request, 'users/login.html', {'form': form})
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})



class profile(TemplateView):
    template_name = 'users/profile.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['p_form'] =  ProfileUpdateForm(instance=self.request.user.profile)
        context['nick_form'] = UserNameUpdateForm(instance=self.request.user.profile)
        context['users'] = self.request.user
        context['r_valid'] = ["hr", "br", "a", "center"]


        return context

    def post(self, request, *args, **kwargs):

        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES)

        nick_form = UserNameUpdateForm(request.POST)
        if nick_form.is_valid():
            alphanumeric = [character for character in request.POST.get("nick", "") if character.isalnum()]
            raw_nick = "".join(alphanumeric)
            if Profile.objects.filter(nick__iexact=raw_nick).count() > 0:
                #messages.success(request, Profile.objects.filter(nick__iexact=raw_nick))
                messages.success(request, f'Taki nick już istnieje')
            else:
                UserNameUpdateForm(request.POST,instance=request.user.profile).save()
        elif len(request.POST.get("nick", "")) > 24:
                messages.success(request, f'Nick jest za długi')

        """
        nick_form = UserNameUpdateForm(request.POST)
        if nick_form.is_valid() and request.POST.get("nick", ""):
            q_porfile = Profile.objects.filter(id=self.request.user.profile.id).first()
            f_save = nick_form.save(commit=False)
            try:
                alphanumeric = [character for character in f_save.nick if character.isalnum()]
                web_urls = "".join(alphanumeric)
                if Profile.objects.filter(web_name=web_urls, nick = q_porfile.nick).count() > 0:

                    messages.success(request, "Takia nazwa już istenieje")
                else:
                    messages.success(request, "wolne_2")
            except:
                messages.success(request, "wolne")
        """

        if p_form.is_valid():
            # lista dozwolonych tagow ,"div", "style"
            check_tag = ["a", "center"]
            r_valid = ["hr", "br"] + check_tag
            good_valid = True
            #a_stack = 0

            dynks_open = p_form["description"].value().count("<")
            dynks_close = p_form["description"].value().count(">")

            for line in re.split('(<[^>]*>)', p_form["description"].value())[1::2]:
                if not '<' in line and not '>' in line:
                    good_valid = False
                elif not any(c in line for c in r_valid):
                    good_valid = False

                #for c in check_tag:
                #    if c in line:
                #        if bool(re.search('</', line)):
                #            a_stack -= 1
                #       elif bool(re.search('<', line)):
                #            a_stack += 1

            #if a_stack != 0:
            #    good_valid = False
            #if a_stack > 0:
            #    messages.success(request, f'nie zamknięty </')
            #elif a_stack < 0:
            #    messages.success(request, f'nie otwarty <')
            if dynks_open != dynks_close:
                good_valid = False
            if dynks_open > dynks_close:
                messages.success(request, f'nie zamknięty <>')
            elif dynks_open < dynks_close:
                messages.success(request, f'nie otwarty <>')

            if good_valid:
                ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile).save()
                messages.success(request, f'Opis został zmodyfikowany.')
            else:
                messages.success(request, f'Masz nie odpowiedni tag albo złą składnie.')

        else:
            return redirect('profile')

        return redirect('user-inf', request.user.profile.web_name)


class Profile_page(TemplateView):
    model = Profile
    context_object_name = 'posts'
    template_name = 'users/user.html'
    fields = ['content']
           
    def dispatch(self, *args, **kwargs):

        #try:
            #if check_ban(User.objects.get(username=self.kwargs['user_name'])):
                #return redirect('fumetsu-home')
        #except:
            #pass
    
        try:
            User.objects.get(profile__web_name=self.kwargs['user_name'])
            return super(Profile_page, self).dispatch(*args, **kwargs)
        except:
            return redirect('fumetsu-home')            
        
    def get_context_data(self, **kwargs):
        #try:
            #if check_ban(self.request.user):
                #logout(self.request)
        #except:
            #pass

        context = super().get_context_data(**kwargs)
        q_profile = Profile.objects.get(web_name=self.kwargs['user_name'])
        q_user = User.objects.get(id=q_profile.user.id)
        q_user.color = Get_color(q_user)
        context['f_user'] = q_user
        context['q_profile'] = q_profile
        context['com_ed'] = CreateComment()
        context['com_ser'] = Series_comment.objects.filter(author = q_user)
        context['com_ep'] = Episode_comment.objects.filter(author = q_user)
        context['ban_form'] = BanForm()
        return context

      
    def post(self, request, *args, **kwargs):
        form = CreateComment(request.POST)
        idd = request.POST.get("idd", "")
        ban_form = BanForm(request.POST)
        q_profile = Profile.objects.get(web_name=self.kwargs['user_name'])
        users = User.objects.get(id=q_profile.user.id)

        if ban_form.is_valid():

            messages.success(request, users.is_active)

            users.is_active = False
            users.save()
            prof = Profile.objects.filter(user = users).first()
            prof.ban = ban_form.cleaned_data['ban']
            prof.save()

            messages.success(request, users.is_active)

            messages.success(request, f'Zbanowano użytkownika')
            return redirect('user-inf', self.kwargs['user_name'])

        if form.is_valid():
            if 'com_up_bt' in request.POST:

                if len(form.cleaned_data.get('content')) > 9:
                    t_save = Episode_comment.objects.filter(id=idd).first()
                    if not t_save:
                        t_save = Series_comment.objects.filter(id = idd).first()

                    if t_save.author == users and idd:
                        t_save.content = form.cleaned_data.get('content')
                        t_save.date_posted = datetime.now()
                        t_save.save()
                        messages.success(request, f'Poprawiono komentarz')

        elif 'com_up_del' in request.POST and idd:
            t_save = Episode_comment.objects.filter(id=idd).first()
            if not t_save:
                t_save = Series_comment.objects.filter(id=idd).first()

            if t_save.author == users and idd:
                t_save.delete()
            messages.success(request, f'Usunięto komentarz')

        return redirect('user-inf', self.kwargs['user_name'])
    
