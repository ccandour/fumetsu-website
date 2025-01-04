import json
from datetime import datetime

from django.db.models import Q, Prefetch
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from utils.utils import AnimeSeriesJSONEncoder, tag_label_to_polish
from .forms import *
from django.contrib import messages
from .models import EpisodeComment

from .models import AnimePost

from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse


def search_anime(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        search_text = request.POST.get('search_text')
        tags = request.POST.getlist('tags[]')

        if len(search_text) > 0:
            # Search for anime series with the given search text
            tags_prefetch = Prefetch('tags', queryset=Tag.objects.only('label_polish'))
            query_set = AnimeSeries.objects.filter(
                Q(name_english__icontains=search_text) |
                Q(name_romaji__icontains=search_text)
            ).prefetch_related(tags_prefetch)
        else:
            tags_prefetch = Prefetch('tags', queryset=Tag.objects.only('label_polish'))
            query_set = AnimeSeries.objects.all().prefetch_related(tags_prefetch)
        if any(tag.strip() for tag in tags):
            # Check if the series has all the selected tags
            for series in query_set:
                if not any(tag in series.tags.all() for tag in tags):
                    query_set = query_set.exclude(anilist_id=series.anilist_id)

        # Return appropriate json response
        if len(query_set) > 0:
            response = json.loads(
                json.dumps(sorted(list(query_set), key=lambda x: x.rating, reverse=True), cls=AnimeSeriesJSONEncoder))
        else:
            response = 'Nie znaleziono anime.'

        return JsonResponse({'data': response})
    return JsonResponse({})


def redirect_legacy_anime(request, anime_name, ep=None):
    if ep:
        # Redirect old url to new url using url_redirects and append episode number
        url_redirect = UrlRedirect.objects.filter(old_url=anime_name).first()
        if url_redirect:
            return redirect(f'ep-nm', anime_name=url_redirect.new_url, ep=ep)
    else:
        # Redirect old url to new url using url_redirects
        url_redirect = UrlRedirect.objects.filter(old_url=anime_name).first()
        if url_redirect:
            return redirect(f'anime-nm', url_redirect.new_url)


class Series(TemplateView):
    model = AnimeSeries
    template_name = 'series.html'
    fields = ['content']

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        ani = AnimeSeries.objects.filter(web_name=self.kwargs['anime_name']).first()
        context['series'] = ani

        context['form'] = CreateComment()

        relations = []
        db_relations = Relation.objects.filter(parent_series_id=ani.anilist_id)
        for relation in db_relations:
            related_series = AnimeSeries.objects.filter(anilist_id=relation.child_series_id).first()
            relation_tuple = (related_series, relation.type)
            relations.append(relation_tuple)
        context['relations'] = relations

        staff = []
        db_staff = StaffCredit.objects.filter(series_id=ani.id)
        for credit in db_staff:
            staff_member = Profile.objects.filter(id=credit.user_id).first()
            staff_tuple = (staff_member, credit.role)
            staff.append(staff_tuple)
        context['staff'] = staff

        comment = SeriesComment.objects.filter(key_map_id=ani).order_by('-date_posted')
        for com in comment:
            com.color = com.author.profile.color
        context['comment'] = comment

        context['comment_form'] = CreateComment()

        context['ep'] = AnimeEpisode.objects.filter(key_map_id=ani).order_by('ep_nr')

        context['tags'] = ani.tags.all()

        context['com_ed'] = CreateComment()

        return context

    def post(self, request, *args, **kwargs):
        form = CreateComment(request.POST)
        idd = request.POST.get("idd", "")

        if form.is_valid():
            if len(form.cleaned_data.get('content')) > 9:
                ani = get_object_or_404(AnimeSeries, web_name=self.kwargs['anime_name'])
                f_save = form.save(commit=False)
                f_save.key_map = ani
                f_save.author = request.user
                f_save.save()
                messages.success(request, 'Dodatno komentarz.')
            else:
                messages.warning(request, 'Komentarz jest za krótki (minimum 10 znaków).')

            if 'com_up_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    t_save = SeriesComment.objects.filter(id=idd).first()
                    if t_save.author == request.user and idd:
                        t_save.content = form.cleaned_data.get('content')
                        t_save.date_posted = datetime.now()
                        t_save.save()
                        messages.success(request, 'Poprawiono komentarz')

            if 'com_up_del' in request.POST and idd:
                t_save = SeriesComment.objects.filter(id=idd).first()
                if t_save.author == request.user and idd:
                    t_save.delete()
                messages.success(request, 'Usunięto komentarz')

        return redirect('anime-nm', self.kwargs['anime_name'])


class Episode(TemplateView):
    model = AnimeEpisode
    context_object_name = 'posts'
    template_name = 'ep.html'
    fields = ['content']

    def dispatch(self, *args, **kwargs):
        ani = get_object_or_404(AnimeSeries, web_name=self.kwargs['anime_name'])
        if AnimeEpisode.objects.filter(key_map=ani, ep_nr=self.kwargs['ep']).first():
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('home')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        series = get_object_or_404(AnimeSeries, web_name=self.kwargs['anime_name'])
        episode = AnimeEpisode.objects.filter(key_map=series, ep_nr=self.kwargs['ep']).first()
        context['link'] = Player.objects.filter(key_map=episode)
        context['series'] = series

        context['odc_html'] = episode.ep_nr

        try:
            if episode.subtitles:
                context['subtitles'] = episode.subtitles
        except:
            pass

        comment = EpisodeComment.objects.filter(key_map=episode).order_by('-date_posted')
        for com in comment:
            com.color = com.author.profile.color
        context['comment'] = comment

        context['comment_form'] = CreateCommentEp()

        context['next'] = AnimeEpisode.objects.filter(key_map_id=series, ep_nr__gt=episode.ep_nr).order_by(
            'ep_nr').first()
        context['prev'] = AnimeEpisode.objects.filter(key_map_id=series, ep_nr__lt=episode.ep_nr).order_by(
            '-ep_nr').first()

        return context

    def post(self, request, *args, **kwargs):
        form = CreateCommentEp(request.POST)
        ani = get_object_or_404(AnimeSeries, web_name=self.kwargs['anime_name'])
        ep_query = AnimeEpisode.objects.filter(key_map_id=ani, ep_nr=self.kwargs['ep']).first()
        if form.is_valid():
            if len(form.cleaned_data.get('content')) > 9:
                f_save = form.save(commit=False)
                f_save.key_map = ep_query
                f_save.author = request.user
                f_save.save()
                messages.success(request, 'Dodatno komentarz.')
            else:
                messages.warning(request, 'Komentarz jest za krótki (minimum 10 znaków).')

            if 'com_up_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    idd = request.POST.get("idd", "")
                    t_save = EpisodeComment.objects.filter(key_map=ep_query, id=idd).first()
                    if t_save.author == request.user and idd:
                        t_save.content = form.cleaned_data.get('content')
                        t_save.date_posted = datetime.now()
                        t_save.save()
                        messages.success(request, 'Poprawiono komentarz')

        elif 'com_up_del' in request.POST:
            idd = request.POST.get("idd", "")
            t_save = EpisodeComment.objects.filter(key_map=ep_query, id=idd).first()
            if t_save.author == request.user and idd:
                t_save.delete()
                messages.success(request, 'Usunięto komentarz')
            else:
                messages.error(request, 'Nie udało się usunąć komentarza')

        return redirect('ep-nm', self.kwargs['anime_name'], self.kwargs['ep'])


class List(ListView):
    model = AnimeSeries
    context_object_name = 'series'
    template_name = 'list.html'
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.db.models import Prefetch

        # Prefetch related tags to reduce the number of queries
        tags_prefetch = Prefetch('tags', queryset=Tag.objects.only('label_polish'))
        anime_series = AnimeSeries.objects.all().prefetch_related(tags_prefetch)

        context['qs_json'] = json.dumps(sorted(list(anime_series), key=lambda x: x.rating, reverse=True), cls=AnimeSeriesJSONEncoder)
        context['tags'] = sorted(set(list(Tag.objects.all().values_list('label_polish', flat=True))))

        context['search_term'] = self.request.GET.get('search')
        context['search_tags'] = [tag.strip().title() for tag in
                                  self.request.GET.get('tags').replace('+', ' ').split()] if self.request.GET.get(
            'tags') else []

        return context


class Home(ListView):
    model = AnimePost
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anime'] = AnimePost.objects.all().order_by('-key_map__date_posted')[:12].prefetch_related(
            Prefetch('key_map', queryset=AnimeEpisode.objects.prefetch_related('key_map'))
        )
        return context


class About(ListView):
    model = AnimePost
    template_name = 'about.html'
    fields = ['content']

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        # Prefetch related StaffCredit objects
        db_credits = StaffCredit.objects.select_related('user').all()

        # Create dictionaries to store the counts
        translator_counts = {}
        editor_counts = {}

        # Iterate through the credits and count the roles
        for credit in db_credits:
            if 'Tłumaczenie' in credit.role:
                if credit.user not in translator_counts:
                    translator_counts[credit.user] = 0
                translator_counts[credit.user] += 1
            if 'Korekta' in credit.role:
                if credit.user not in editor_counts:
                    editor_counts[credit.user] = 0
                editor_counts[credit.user] += 1

        # Convert the dictionaries to sorted lists
        translators = sorted(translator_counts.items(), key=lambda x: x[1], reverse=True)
        editors = sorted(editor_counts.items(), key=lambda x: x[1], reverse=True)

        context['administators'] = Profile.objects.filter(user__is_superuser=True)
        context['translators'] = translators
        context['editors'] = editors

        return context


class Announcements(ListView):
    model = AnimePost
    context_object_name = 'announcements'
    queryset = Announcement.objects.all().order_by('-date_posted')
    template_name = 'announcements.html'


class PrivacyPolicy(ListView):
    model = AnimePost
    template_name = 'privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TermsOfService(ListView):
    model = AnimePost
    template_name = 'terms_of_service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteComment(TemplateView):
    def post(self, request, *args, **kwargs):
        episode_comments = EpisodeComment.objects.filter(id=kwargs['pk'])
        if episode_comments and (episode_comments.first().author == request.user or request.user.is_superuser):
            episode_comments.delete()
            messages.success(request, 'Komentarz usunięty.')
        else:
            series_comments = SeriesComment.objects.filter(id=kwargs['pk'])
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
            return HttpResponseRedirect(reverse('home'))


class EditComment(TemplateView):
    model = PostComment
    template_name = 'edit_comment.html'
    referer = ''

    def get_context_data(self, **kwargs):
        # Store the referer in the session
        if 'HTTP_REFERER' in self.request.META:
            self.request.session['previous_referer'] = self.request.META['HTTP_REFERER']

        context = super().get_context_data(**kwargs)
        episode_comments = EpisodeComment.objects.filter(id=kwargs['pk'])
        if episode_comments and (episode_comments.first().author == self.request.user):
            context['form'] = EditCommentForm(instance=episode_comments.first())
            context['comment'] = episode_comments.first()
            context['type'] = 'episode'
            return context
        else:
            series_comments = SeriesComment.objects.filter(id=kwargs['pk'])
            if series_comments and (series_comments.first().author == self.request.user):
                context['form'] = EditCommentForm(instance=series_comments.first())
                context['comment'] = series_comments.first()
                context['type'] = 'series'
                return context
            else:
                redirect('home')

    def post(self, request, *args, **kwargs):
        episode_comments = EpisodeComment.objects.filter(id=kwargs['pk'])
        if episode_comments and (episode_comments.first().author == request.user):
            form = EditCommentForm(request.POST, instance=episode_comments.first())
            if form.is_valid():
                form.save()
                messages.success(request, 'Komentarz zaktualizowany.')
            else:
                messages.error(request, 'Nie udało się zaktualizować komentarza.')
        else:
            series_comments = SeriesComment.objects.filter(id=kwargs['pk'])
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
            return redirect('home')
