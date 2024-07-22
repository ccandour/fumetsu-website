import sys

from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from fumetsu.models import Anime_list, Series_comment, Url_redirects, Relation, Staff_credits
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
from django.forms import modelformset_factory

from fumetsu.ban import check_ban, Nap_time, Is_member, Get_color
from django.contrib.auth import logout
import math

def search_anime(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        search_text = request.POST.get('search_text')
        tags = request.POST.getlist('tags[]')

        if len(search_text) > 0:
            # Search for anime series with the given search text
            query_set = Anime_list.objects.filter(
                Q(name_english__icontains=search_text) |
                Q(name_romaji__icontains=search_text)
            )
        else:
            query_set = Anime_list.objects.all()
        if any(tag.strip() for tag in tags):
            # Check if the series has all the selected tags
            for series in query_set:
                series_tags = Tags.objects.filter(anime_anilist_id=series.anilist_id).values_list('label_polish', flat=True)
                if not set(tags).issubset(set(series_tags)):
                    query_set = query_set.exclude(anilist_id=series.anilist_id)

        # Return appropriate json response
        if len(query_set) > 0:
            response = json.loads(json.dumps(sorted(list(query_set), key=lambda x: x.rating, reverse=True), cls=AnimeSeriesJSONEncoder))
        else:
            response = 'No anime found.'

        return JsonResponse({'data': response})
    return JsonResponse({})

def redirect_legacy_anime(request, anime_name, ep=None):
    if ep:
        # Redirect old url to new url using url_redirects and append episode number
        url_redirect = Url_redirects.objects.filter(old_url=anime_name).first()
        if url_redirect:
            return redirect(f'ep-nm', anime_name=url_redirect.new_url, ep=ep)
    else:
        # Redirect old url to new url using url_redirects
        url_redirect = Url_redirects.objects.filter(old_url=anime_name).first()
        if url_redirect:
            return redirect(f'anime-nm', url_redirect.new_url)


class Anime_content(TemplateView):
    model = Anime_list
    template_name = 'series.html'
    fields = ['content']

    def get_context_data(self, **kwargs):
        try:
            if check_ban(self.request.user):
                logout(self.request)
        except:
            pass

        context = super().get_context_data(**kwargs)
        ani = Anime_list.objects.filter(web_name=self.kwargs['anime_name']).first()
        context['series'] = ani

        context['form'] = CreateComment()

        try:
            if ani.napisy:
                if Nap_time(self.request.user) or Is_member(self.request.user):
                    context['napisy'] = ani.napisy
        except:
            pass

        relations = []
        db_relations = Relation.objects.filter(parent_series_id=ani.anilist_id)
        for relation in db_relations:
            related_series = Anime_list.objects.filter(anilist_id=relation.child_series_id).first()
            relation_tuple = (related_series, relation.type)
            relations.append(relation_tuple)
        context['relations'] = relations

        staff = []
        db_staff = Staff_credits.objects.filter(series_id=ani.id)
        for credit in db_staff:
            staff_member = Profile.objects.filter(id=credit.user_id).first()
            staff_tuple = (staff_member, credit.role)
            staff.append(staff_tuple)
        context['staff'] = staff

        comment = Series_comment.objects.filter(key_map_id=ani).order_by('-date_posted')
        for comm in comment:
            comm.color = Get_color(comm.author)
        context['comment'] = comment

        context['ep'] = Odc_name.objects.filter(key_map_id=ani).order_by('ep_title')

        kurwa = Tags.objects.filter(anime_anilist_id=ani.anilist_id).only("label")

        list_tags = []
        for tag in kurwa:
            list_tags.append(tag_label_to_polish(tag.label))
        context['tags'] = list_tags

        context['com_ed'] = CreateComment()

        return context

    def post(self, request, *args, **kwargs):
        form = CreateComment(request.POST)
        idd = request.POST.get("idd", "")

        messages.success(request, 'aaaaaaaaaaaa')
        if form.is_valid():
            messages.success(request, '1')
            if 'com_cr_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    ani = get_object_or_404(Anime_list, web_name=self.kwargs['anime_name'])
                    f_save = form.save(commit=False)
                    f_save.anime = ani
                    f_save.author = request.user
                    f_save.save()
                    messages.success(request, 'Dodatno komentarz')
                else:
                    messages.success(request, 'komentarz jest za krótki')

            elif 'com_up_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    t_save = Series_comment.objects.filter(id=idd).first()
                    if t_save.author == request.user and idd:
                        t_save.content = form.cleaned_data.get('content')
                        t_save.date_posted = datetime.now()
                        t_save.save()
                        messages.success(request, 'Poprawiono komentarz')

        if 'com_up_del' in request.POST and idd:
            t_save = Series_comment.objects.filter(id=idd).first()
            if t_save.author == request.user and idd:
                t_save.delete()
            messages.success(request, 'Usunięto komentarz')

        return redirect('anime-nm', self.kwargs['anime_name'])


class Anime_episode(TemplateView):
    model = Anime_list
    context_object_name = 'posts'
    template_name = 'ep.html'
    fields = ['content']

    def dispatch(self, *args, **kwargs):
        ani = get_object_or_404(Anime_list, web_name=self.kwargs['anime_name'])
        if Odc_name.objects.filter(key_map_id=ani, ep_nr=self.kwargs['ep']).first():
            return super().dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):
        try:
            if check_ban(self.request.user):
                logout(self.request)
        except:
            pass

        context = super().get_context_data(**kwargs)
        ani = get_object_or_404(Anime_list, web_name=self.kwargs['anime_name'])
        ep = self.kwargs['ep']
        context['link'] = Anime_url.objects.filter(key_map_id=ani, ep_nr=ep)
        context['anime_nm'] = ani
        context['com_ed'] = CreateCommentEp()

        ep_query = Odc_name.objects.filter(key_map_id=ani, ep_nr=ep).first()
        context['odc_html'] = ep_query.ep_nr

        try:
            if ep_query.napisy:
                if Nap_time() or Is_member(self.request.user):
                    context['napisy'] = ep_query.napisy
        except:
            pass

        comment = Episode_comment.objects.filter(key_map_ep=ep_query).order_by('-date_posted')
        for comm in comment:
            comm.color = Get_color(comm.author)
        context['comment'] = comment

        context['next'] = Odc_name.objects.filter(key_map_id=ani, ep_title__gt=ep_query.ep_title).order_by(
            'ep_title').first()
        context['prev'] = Odc_name.objects.filter(key_map_id=ani, ep_title__lt=ep_query.ep_title).order_by(
            '-ep_title').first()

        return context

    def post(self, request, *args, **kwargs):
        form = CreateCommentEp(request.POST)
        ani = get_object_or_404(Anime_list, web_name=self.kwargs['anime_name'])
        ep_query = Odc_name.objects.filter(key_map_id=ani, ep_nr=self.kwargs['ep']).first()
        if form.is_valid():
            if 'com_cr_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    f_save = form.save(commit=False)
                    f_save.episode = ep_query
                    f_save.author = request.user
                    f_save.save()
                    messages.success(request, 'Dodatno komentarz')
                else:
                    messages.success(request, 'komentarz jest za krótki')

            elif 'com_up_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    idd = request.POST.get("idd", "")
                    t_save = Episode_comment.objects.filter(key_map_ep=ep_query, id=idd).first()
                    if t_save.author == request.user and idd:
                        t_save.content = form.cleaned_data.get('content')
                        t_save.date_posted = datetime.now()
                        t_save.save()
                        messages.success(request, 'Poprawiono komentarz')

        elif 'com_up_del' in request.POST:
            idd = request.POST.get("idd", "")
            t_save = Episode_comment.objects.filter(key_map_ep=ep_query, id=idd).first()
            if t_save.author == request.user and idd:
                t_save.delete()
                messages.success(request, 'Usunięto komentarz')
            else:
                messages.error(request, 'Nie udało się usunąć komentarza')

        elif 'ply_error' in request.POST:
            t_save = Player_valid.objects.filter(episode=ep_query).first()
            if t_save:
                t_save.ilosc += 1
                t_save.save()
            else:
                Player_valid(key_map_ep=ep_query).save()
            messages.success(request, 'Dodano skargę')

        return redirect('ep-nm', self.kwargs['anime_name'], self.kwargs['ep'])


from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Count
import math
from .models import Anime_list, Tags
# from .forms import QueryTags
from fumetsu.ban import check_ban
import json


class List(ListView):
    model = Anime_list
    context_object_name = 'posts'
    template_name = 'list.html'
    fields = ['content']

    def get_context_data(self, **kwargs):
        # Check if user is banned
        try:
            if check_ban(self.request.user):
                logout(self.request)
                print("User banned, logging out")
        except Exception as e:
            print(f"Error checking ban: {e}")

        context = super().get_context_data(**kwargs)

        context['qs_json'] = json.dumps(list(Anime_list.objects.all()), cls=AnimeSeriesJSONEncoder)
        context['tags'] = sorted(set(list(Tags.objects.all().values_list('label_polish', flat=True))))

        context['search_term'] = self.request.GET.get('search')
        context['search_tags'] = [tag.strip().title() for tag in self.request.GET.get('tags').replace('+', ' ').split()] if self.request.GET.get('tags') else []


        return context

    def post(self, request, *args, **kwargs):
        form = QueryTags(request.POST)

        if 'page_ch' in request.POST:
            self.request.session['page'] = int(request.POST.get('page_ch')) - 1

        # Clear the session (filters) if requested
        elif 'ses_cl' in request.POST:
            self.request.session['page'] = 0
            self.request.session.pop('tags_nm', None)
            self.request.session.pop('tags', None)
            return redirect("anime-list")

        # Change the number of items per page
        elif 'page_12' in request.POST:
            self.request.session['ile_pozycji'] = 12
            self.request.session['page'] = 0
        elif 'page_24' in request.POST:
            self.request.session['ile_pozycji'] = 24
            self.request.session['page'] = 0
        elif 'page_48' in request.POST:
            self.request.session['ile_pozycji'] = 48
            self.request.session['page'] = 0

        # Set the initial page to 0
        elif form.is_valid():
            self.request.session['page'] = 0

            if form.cleaned_data.get('name') and form.cleaned_data.get('ch_box'):
                self.request.session['tags_nm'] = form.cleaned_data.get('name')
                tags = [ix.title for ix in form.cleaned_data.get('ch_box')]
                self.request.session['tags'] = tags

            elif form.cleaned_data.get('name'):
                self.request.session.pop('tags', None)
                self.request.session['tags_nm'] = form.cleaned_data.get('name')

            elif form.cleaned_data.get('ch_box'):
                self.request.session.pop('tags_nm', None)
                tags = [ix.title for ix in form.cleaned_data.get('ch_box')]
                self.request.session['tags'] = tags
                print(f"Search set - tags: {self.request.session['tags']}")

        else:
            messages.error(request, 'Nie podałeś nic do wyszukiwania')
            print("Form is not valid")

        return redirect("anime-list")
