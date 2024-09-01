from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from .forms import *
from django.contrib import messages
from anime.models import Episode_comment

from anime.models import Post

from django.http import HttpResponseRedirect
from django.urls import reverse


class Home(ListView):
    model = Post
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anime'] = Post.objects.all().order_by('-odc_nm__date_posted')[:12]
        return context


class About(ListView):
    model = Post
    template_name = 'about.html'
    fields = ['content']

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Prepare a lists of staff members
        administators = Profile.objects.filter(user__is_superuser='True')
        translators = []
        editors = []

        db_credits = Staff_credits.objects.all()
        for credit in db_credits:
            if credit.role == 'Tłumaczenie' and [credit.user, len(list(
                    Staff_credits.objects.filter(user=credit.user, role='Tłumaczenie')))] not in translators:
                translators.append(
                    [credit.user, len(list(Staff_credits.objects.filter(user=credit.user, role='Tłumaczenie')))])
            elif credit.role == 'Korekta' and [credit.user, len(list(
                    Staff_credits.objects.filter(user=credit.user, role='Korekta')))] not in editors:
                editors.append([credit.user, len(list(Staff_credits.objects.filter(user=credit.user, role='Korekta')))])

        translators.sort(key=lambda x: x[1], reverse=True)
        editors.sort(key=lambda x: x[1], reverse=True)

        context['administators'] = administators
        context['translators'] = translators
        context['editors'] = editors

        return context


class Announcements(ListView):
    model = Post
    context_object_name = 'announcements'
    queryset = Info_bd.objects.all().order_by('-date_posted')
    template_name = 'announcements.html'


class PrivacyPolicy(ListView):
    model = Post
    template_name = 'privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TermsOfService(ListView):
    model = Post
    template_name = 'terms_of_service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteComment(TemplateView):
    def post(self, request, *args, **kwargs):
        episode_comments = Episode_comment.objects.filter(id=kwargs['pk'])
        if episode_comments and (episode_comments.first().author == request.user or request.user.is_superuser):
            episode_comments.delete()
            messages.success(request, 'Komentarz usunięty.')
        else:
            series_comments = Series_comment.objects.filter(id=kwargs['pk'])
            if series_comments and (series_comments.first().author == request.user or request.user.is_superuser):
                series_comments.delete()
                messages.success(request, 'Komentarz usunięty.')
            else:
                messages.error(request, 'Nie masz uprawnień do usunięcia tego komentarza.')

        if 'HTTP_REFERER' in request.META and 'edit-comment' not in request.META['HTTP_REFERER']:
            return HttpResponseRedirect(request.META['HTTP_REFERER'])
        elif 'previous_referer' in request.session:
            referer = request.session['previous_referer']
            del request.session['previous_referer']
            return HttpResponseRedirect(referer)
        else:
            return HttpResponseRedirect(reverse('fumetsu-home'))


class EditComment(TemplateView):
    model = Post_comment
    template_name = 'edit_comment.html'
    referer = ''

    def get_context_data(self, **kwargs):
        # Store the referer in the session
        if 'HTTP_REFERER' in self.request.META:
            self.request.session['previous_referer'] = self.request.META['HTTP_REFERER']

        context = super().get_context_data(**kwargs)
        episode_comments = Episode_comment.objects.filter(id=kwargs['pk'])
        if episode_comments and (episode_comments.first().author == self.request.user):
            context['form'] = EditCommentForm(instance=episode_comments.first())
            context['comment'] = episode_comments.first()
            context['type'] = 'episode'
            return context
        else:
            series_comments = Series_comment.objects.filter(id=kwargs['pk'])
            if series_comments and (series_comments.first().author == self.request.user):
                context['form'] = EditCommentForm(instance=series_comments.first())
                context['comment'] = series_comments.first()
                context['type'] = 'series'
                return context
            else:
                redirect('fumetsu-home')

    def post(self, request, *args, **kwargs):
        episode_comments = Episode_comment.objects.filter(id=kwargs['pk'])
        if episode_comments and (episode_comments.first().author == request.user):
            form = EditCommentForm(request.POST, instance=episode_comments.first())
            if form.is_valid():
                form.save()
                messages.success(request, 'Komentarz zaktualizowany.')
            else:
                messages.error(request, 'Nie udało się zaktualizować komentarza.')
        else:
            series_comments = Series_comment.objects.filter(id=kwargs['pk'])
            if series_comments and (series_comments.first().author == request.user):
                form = EditCommentForm(request.POST, instance=series_comments.first())
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Komentarz zaktualizowany.')
                else:
                    messages.error(request, 'Nie udało się zaktualizować komentarza.')
            else:
                messages.error(request, 'Nie masz uprawnień do edycji tego komentarza.')

        if 'previous_referer' in request.session:
            referer = request.session['previous_referer']
            del request.session['previous_referer']
            return HttpResponseRedirect(referer)
        else:
            return redirect('fumetsu-home')
