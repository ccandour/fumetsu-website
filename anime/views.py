from django.shortcuts import render, redirect
from django.contrib import messages

from fumetsu.models import Anime_list, Series_comment, Url_redirects, Relation
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView
)

from .forms import *
from .models import *

from django.views.generic.base import TemplateView
from datetime import datetime
from django.db.models import Count
from django.forms import modelformset_factory

from fumetsu.ban import check_ban, Nap_time, Is_member, Get_color
from django.contrib.auth import logout
import math

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
    template_name = 'anime/index.html'
    fields = ['content']

    def get_context_data(self, **kwargs):
        try:
            if check_ban(self.request.user):
                logout(self.request)
        except:
            pass

        context = super().get_context_data(**kwargs)
        ani = Anime_list.objects.filter(web_name=self.kwargs['anime_name']).first()
        context['posts'] = ani

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

        comment = Series_comment.objects.filter(key_map_id=ani).order_by('-date_posted')
        for comm in comment:
            comm.color = Get_color(comm.author)
        context['comment'] = comment

        context['ep'] = Odc_name.objects.filter(key_map_id=ani).order_by('ep_title')

        kurwa = Tags.objects.filter(key_map_id=ani).only("tags_map")

        list_tags = []
        for tag in kurwa:
            list_tags.append(tag.tags_map)
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
    template_name = 'anime/ep.html'
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
        context['odc_html'] = ep_query.ep_title

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
from .forms import QueryTags
from fumetsu.ban import check_ban


class List(TemplateView):
    model = Anime_list
    context_object_name = 'posts'
    template_name = 'anime/list.html'
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
        context['filter'] = QueryTags()
        context['ses_bool'] = False

        # Set default values for session variables
        self.request.session.setdefault('ile_pozycji', 12)
        self.request.session.setdefault('page', 1)
        total_anime_count = Anime_list.objects.all().count()
        context['page_max'] = math.ceil(total_anime_count / self.request.session['ile_pozycji'])

        # Both tags and search query
        if 'tags' in self.request.session and 'tags_nm' in self.request.session:
            an_list = []

            # Get all tags-series pairs that match the selected tags
            tags_l = Tags.objects.filter(
                key_map__title__contains=self.request.session['tags_nm'],
                tags_map__title__in=self.request.session['tags']
            )

            # Make a dictionary with anime series ids and the number of tags that match the selected tags
            anime_l = tags_l.values('key_map').annotate(Count('id')).order_by().filter(
                id__count__gt=len(self.request.session['tags']) - 1)

            # Add the series to the list
            for ani in anime_l:
                anime_id = ani['key_map']
                anime_instance = Anime_list.objects.filter(id=anime_id).first()
                if anime_instance:
                    an_list.append(anime_instance)

            if self.request.session['page'] * self.request.session['ile_pozycji'] > len(an_list):
                self.request.session['page'] = 0

            # Get the series for current page
            start_index = self.request.session['page'] * self.request.session['ile_pozycji']
            end_index = (self.request.session['page'] + 1) * self.request.session['ile_pozycji']
            context['posts'] = an_list[start_index:end_index]

            context['search'] = True

            context['tags'] = self.request.session['tags']
            context['tags_nm'] = self.request.session['tags_nm']

        # Only tags
        elif 'tags' in self.request.session:
            an_list = []

            # Get all tags-series pairs that match the selected tags
            tags_l = Tags.objects.filter(tags_map__title__in=self.request.session['tags'])

            # Make a dictionary with anime series ids and the number of tags that match the selected tags
            anime_l = tags_l.values('key_map').annotate(Count('id')).order_by().filter(
                id__count__gt=len(self.request.session['tags']) - 1)

            # Add the series to the list
            for ani in anime_l:
                anime_id = ani['key_map']
                anime_instance = Anime_list.objects.filter(id=anime_id).first()
                if anime_instance:
                    an_list.append(anime_instance)

            if self.request.session['page'] * self.request.session['ile_pozycji'] > len(an_list):
                self.request.session['page'] = 0

            # Get the series for current page
            start_index = self.request.session['page'] * self.request.session['ile_pozycji']
            end_index = (self.request.session['page'] + 1) * self.request.session['ile_pozycji']
            context['posts'] = an_list[start_index:end_index]

            context['search'] = True
            context['tags'] = self.request.session['tags']

        # Only search query
        elif 'tags_nm' in self.request.session:
            # Get all the series that contain the search query in their title
            start_index = self.request.session['page'] * self.request.session['ile_pozycji']
            end_index = (self.request.session['page'] + 1) * self.request.session['ile_pozycji']
            context['posts'] = Anime_list.objects.filter(title__contains=self.request.session['tags_nm'])[start_index:end_index]

            context['search'] = True
            context['tags_nm'] = self.request.session['tags_nm']
        else:
            # Get the series for current page
            start_index = self.request.session['page'] * self.request.session['ile_pozycji']
            end_index = (self.request.session['page'] + 1) * self.request.session['ile_pozycji']
            context['posts'] = Anime_list.objects.all()[start_index:end_index]

        context['page'] = self.request.session['page']

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
            return redirect("fumetsu-list")

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

        return redirect("fumetsu-list")
