import json
import sys

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from fumetsu.models import AnimeSeries, SeriesComment, UrlRedirect, Relation, StaffCredit
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView
)

from users.models import Profile
from utils.utils import tag_label_to_polish, AnimeSeriesJSONEncoder
from .forms import *
from .models import *

from django.views.generic import ListView
from django.views.generic.base import TemplateView
from datetime import datetime
from django.db.models import Count, Q

from fumetsu.ban import get_color



def search_anime(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        search_text = request.POST.get('search_text')
        tags = request.POST.getlist('tags[]')

        if len(search_text) > 0:
            # Search for anime series with the given search text
            query_set = AnimeSeries.objects.filter(
                Q(name_english__icontains=search_text) |
                Q(name_romaji__icontains=search_text)
            )
        else:
            query_set = AnimeSeries.objects.all()
        if any(tag.strip() for tag in tags):
            # Check if the series has all the selected tags
            for series in query_set:
                series_tags = Tag.objects.filter(anime_anilist_id=series.anilist_id).values_list('label_polish',
                                                                                                 flat=True)
                if not set(tags).issubset(set(series_tags)):
                    query_set = query_set.exclude(anilist_id=series.anilist_id)

        # Return appropriate json response
        if len(query_set) > 0:
            response = json.loads(
                json.dumps(sorted(list(query_set), key=lambda x: x.rating, reverse=True), cls=AnimeSeriesJSONEncoder))
        else:
            response = 'No anime found.'

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

        db_tags = Tag.objects.filter(anime_anilist_id=ani.anilist_id).only("label")

        list_tags = []
        for tag in db_tags:
            list_tags.append(tag_label_to_polish(tag.label))
        context['tags'] = list_tags

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
    model = AnimeSeries
    context_object_name = 'posts'
    template_name = 'ep.html'
    fields = ['content']

    def dispatch(self, *args, **kwargs):
        ani = get_object_or_404(AnimeSeries, web_name=self.kwargs['anime_name'])
        if AnimeEpisode.objects.filter(key_map_id=ani, ep_nr=self.kwargs['ep']).first():
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        ani = get_object_or_404(AnimeSeries, web_name=self.kwargs['anime_name'])
        ep = self.kwargs['ep']
        context['link'] = Player.objects.filter(key_map_id=ani, ep_nr=ep)
        context['anime_nm'] = ani

        ep_query = AnimeEpisode.objects.filter(key_map_id=ani, ep_nr=ep).first()
        context['odc_html'] = ep_query.ep_nr

        try:
            if ep_query.subtitles:
                context['subtitles'] = ep_query.subtitles
        except:
            pass

        comment = EpisodeComment.objects.filter(key_map_ep=ep_query).order_by('-date_posted')
        for com in comment:
            com.color = com.author.profile.color
        context['comment'] = comment

        context['comment_form'] = CreateCommentEp()

        context['next'] = AnimeEpisode.objects.filter(key_map_id=ani, ep_nr__gt=ep_query.ep_nr).order_by(
            'ep_nr').first()
        context['prev'] = AnimeEpisode.objects.filter(key_map_id=ani, ep_nr__lt=ep_query.ep_nr).order_by(
            '-ep_nr').first()

        return context

    def post(self, request, *args, **kwargs):
        form = CreateCommentEp(request.POST)
        ani = get_object_or_404(AnimeSeries, web_name=self.kwargs['anime_name'])
        ep_query = AnimeEpisode.objects.filter(key_map_id=ani, ep_nr=self.kwargs['ep']).first()
        if form.is_valid():
            if len(form.cleaned_data.get('content')) > 9:
                f_save = form.save(commit=False)
                f_save.key_map_ep = ep_query
                f_save.author = request.user
                f_save.save()
                messages.success(request, 'Dodatno komentarz.')
            else:
                messages.warning(request, 'Komentarz jest za krótki (minimum 10 znaków).')

            if 'com_up_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    idd = request.POST.get("idd", "")
                    t_save = EpisodeComment.objects.filter(key_map_ep=ep_query, id=idd).first()
                    if t_save.author == request.user and idd:
                        t_save.content = form.cleaned_data.get('content')
                        t_save.date_posted = datetime.now()
                        t_save.save()
                        messages.success(request, 'Poprawiono komentarz')

        elif 'com_up_del' in request.POST:
            idd = request.POST.get("idd", "")
            t_save = EpisodeComment.objects.filter(key_map_ep=ep_query, id=idd).first()
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

        context['qs_json'] = json.dumps(list(AnimeSeries.objects.all()), cls=AnimeSeriesJSONEncoder)
        context['tags'] = sorted(set(list(Tag.objects.all().values_list('label_polish', flat=True))))

        context['search_term'] = self.request.GET.get('search')
        context['search_tags'] = [tag.strip().title() for tag in
                                  self.request.GET.get('tags').replace('+', ' ').split()] if self.request.GET.get(
            'tags') else []

        return context
