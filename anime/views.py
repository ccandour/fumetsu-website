from django.shortcuts import render, redirect
from django.contrib import messages

from fumetsu.models import Anime_list, Series_comment, Key_map, Season
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
        k_m = get_object_or_404(Key_map, web_name = self.kwargs['anime_name'])
        ani = Anime_list.objects.filter(key_map=k_m).first()
        ani.web_name = k_m.web_name
        context['posts'] = ani

        context['form'] = CreateComment()


        try:
            if ani.napisy:
                if Nap_time(self.request.user) == True or Is_member(self.request.user) == True:
                    context['napisy'] = ani.napisy
        except:
            pass

        
        id_an_html = []
        id_an_f = Season.objects.filter(id_anime_f=k_m.id_anime)
        for id_an in id_an_f:
            an_list_ses = Anime_list.objects.filter(key_map__id_anime=id_an.id_anime_s).first()
            an_list_ses.desc = id_an_f[0].description
            id_an_html.append(an_list_ses)
        context['family_anime'] = id_an_html

        comment = Series_comment.objects.filter(key_map=k_m).order_by('-date_posted')
        for comm in comment:
            comm.color = Get_color(comm.author)
        context['comment'] = comment

        context['ep'] = Odc_name.objects.filter(key_map=k_m).order_by('ep_title')     
        
        kurwa = Tags.objects.filter(key_map=k_m).only("tags_map")
        
        list_tags = [] #zmien to,  po chuj?
        for tag in kurwa:
            list_tags.append(tag.tags_map)
        context['tags'] = list_tags
        del kurwa

        context['com_ed'] = CreateComment()

        return context

    
    def post(self, request, *args, **kwargs):
        form = CreateComment(request.POST)
        idd = request.POST.get("idd", "")

        messages.success(request, f'aaaaaaaaaaaa')
        if form.is_valid():
            messages.success(request, f'1')
            if 'com_cr_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    k_m = get_object_or_404(Key_map, web_name = self.kwargs['anime_name'])
                    f_save = form.save(commit=False)
                    f_save.key_map = k_m
                    f_save.author = request.user
                    f_save.save()
                    messages.success(request, f'Dodatno komentarz')
                else:
                    messages.success(request, f'komentarz jest za krótki')


            elif 'com_up_bt' in request.POST:

                if len(form.cleaned_data.get('content')) > 9:

                    t_save = Series_comment.objects.filter(id=idd).first()

                    if t_save.author == request.user and idd:
                        t_save.content = form.cleaned_data.get('content')

                        t_save.date_posted = datetime.now()

                        t_save.save()

                        messages.success(request, f'Poprawiono komentarz')


        if 'com_up_del' in request.POST and idd:

            t_save = Series_comment.objects.filter(id=idd).first()

            if t_save.author == request.user and idd:
                t_save.delete()

            messages.success(request, f'Usunięto komentarz')


        return redirect('anime-nm', self.kwargs['anime_name'])

class Anime_episode(TemplateView):
    model = Anime_list
    context_object_name = 'posts'
    template_name = 'anime/ep.html'
    fields = ['content']
    


    def dispatch(self, *args, **kwargs):
        k_m = get_object_or_404(Key_map, web_name = self.kwargs['anime_name'])
        if Odc_name.objects.filter(key_map=k_m, ep_nr=self.kwargs['ep']).first():
            return super(Anime_episode, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):
        try:
            if check_ban(self.request.user):
                logout(self.request)
        except:
            pass

        context = super().get_context_data(**kwargs)
        k_m = get_object_or_404(Key_map, web_name = self.kwargs['anime_name'])
        ep = self.kwargs['ep']
        context['link'] = Anime_url.objects.filter(key_map=k_m, ep_nr=ep)
        context['anime_nm'] = k_m
        context['com_ed'] = CreateCommentEp()

        ep_query = Odc_name.objects.filter(key_map=k_m, ep_nr=ep).first()

        context['odc_html'] = ep_query.ep_title

        try:
            if ep_query.napisy:
                if Nap_time() == True or Is_member(self.request.user) == True:
                    context['napisy'] = ep_query.napisy
        except:
            pass

        comment = Episode_comment.objects.filter(key_map_ep=ep_query).order_by('-date_posted')
        for comm in comment:
            comm.color = Get_color(comm.author)
        context['comment'] = comment

        if Odc_name.objects.filter(key_map=k_m, ep_title__gt=ep_query.ep_title).order_by('ep_title').first():
            context['next'] = Odc_name.objects.filter(key_map=k_m, ep_title__gt=ep_query.ep_title).order_by('ep_title').first()
        if Odc_name.objects.filter(key_map=k_m, ep_title__lte=ep_query.ep_title).order_by('ep_title').first():
            context['prev'] = Odc_name.objects.filter(key_map=k_m, ep_title__lt=ep_query.ep_title).order_by('-ep_title').first()
        del ep


        
        return context

    def post(self, request, *args, **kwargs):
        form = CreateCommentEp(request.POST)
        k_m = get_object_or_404(Key_map, web_name=self.kwargs['anime_name'])
        od_nm = Odc_name.objects.filter(key_map=k_m, ep_nr=self.kwargs['ep']).first()
        if form.is_valid():
            if 'com_cr_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    f_save = form.save(commit=False)
                    f_save.key_map_ep = od_nm
                    f_save.author = request.user
                    f_save.save()
                    messages.success(request, f'Dodatno komentarz')
                else:
                    messages.success(request, f'komentarz jest za krótki')

            elif 'com_up_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    idd = request.POST.get("idd", "")
                    t_save = Episode_comment.objects.filter(key_map_ep = od_nm, id = idd).first()
                    if t_save.author == request.user and idd:
                        f_save = form.save(commit=False)

                        t_save.content = form.cleaned_data.get('content')
                        t_save.date_posted = datetime.now()
                        t_save.save()
                messages.success(request, f'Poprawiono komentarz')
                

        elif 'com_up_del' in request.POST:
            idd = request.POST.get("idd", "")
            t_save = Episode_comment.objects.filter(key_map_ep=od_nm, id=idd).first()
            if t_save.author == request.user and idd:
                t_save.delete()
                messages.success(request, f'Usunięto komentarz')
            else:
                messages.error(request, f'Nie udało się usunąć konta')#coś tu się zjebało DRUPAT!!!

        elif 'ply_error' in request.POST:
            t_save = Player_valid.objects.filter(key_map_ep=od_nm).first()
            if t_save:
                t_save.ilosc = t_save.ilosc + 1
                t_save.save()
            else:
                Player_valid(key_map_ep=od_nm).save()
            messages.success(request, f'Dodano skarge')


        return redirect('ep-nm', self.kwargs['anime_name'], self.kwargs['ep'])

class List(TemplateView):
    model = Anime_list
    context_object_name = 'posts'
    template_name = 'anime/list.html'
    fields = ['content']


    def get_context_data(self, **kwargs):
        try:
            if check_ban(self.request.user):
                logout(self.request)
        except:
            pass

        context = super().get_context_data(**kwargs)
        context['filter'] = QueryTags()
        context['ses_bool'] = False

        try:
            self.request.session['ile_pozycji']
        except:
            self.request.session['ile_pozycji'] = 12

        try:
            if self.request.session['page'] < 0:
                self.request.session['page'] = 0
        except:
            self.request.session['page'] = 0

        context['page_max'] = math.ceil(Anime_list.objects.all().count() / self.request.session['ile_pozycji'])

        try: #__startswith __contains

            if 'tags' in self.request.session and 'tags_nm' in self.request.session:
                an_list = []
                anime_l = Tags.objects.filter(key_map__title__contains=self.request.session['tags_nm'],tags_map__title__in = self.request.session['tags'])

                # Spełnia wszystkie warunki
                anime_l = anime_l.values('key_map').annotate(Count('id')).order_by().filter(id__count__gt=len(self.request.session['tags'])-1)

                for jx in anime_l:   
                    an_list.append(Anime_list.objects.filter(key_map__id=jx['key_map']))

                context['page_max'] = math.ceil(len(an_list) / self.request.session['ile_pozycji'])

                context['ses_bool'] = True 
                context['an_list'] = an_list[self.request.session['page']*self.request.session['ile_pozycji']:(self.request.session['page']*self.request.session['ile_pozycji'])+self.request.session['ile_pozycji']]
                
                if not context['an_list']:
                    if not self.request.session['page'] == 0:
                        self.request.session['page'] = self.request.session['page'] - 1
                        context['an_list'] = an_list[self.request.session['page']*self.request.session['ile_pozycji']:(self.request.session['page']*self.request.session['ile_pozycji'])+self.request.session['ile_pozycji']]
                    else:
                        del self.request.session['tags_nm']
                        del self.request.session['tags']
                        context['not_found'] = "Zgubiłeś się Onii-chan?"

            elif 'tags' in self.request.session:  
                an_list = []
                anime_l = Tags.objects.filter(tags_map__title__in = self.request.session['tags'])
                
                # Spełnia wszystkie warunki
                anime_l = anime_l.values('key_map').annotate(Count('id')).order_by().filter(id__count__gt=len(self.request.session['tags'])-1)

                for jx in anime_l:   
                    an_list.append(Anime_list.objects.filter(key_map__id=jx['key_map']))

                context['ses_bool'] = True


                context['page_max'] = math.ceil(len(an_list) / self.request.session['ile_pozycji'])
                context['an_list'] = an_list[self.request.session['page']*self.request.session['ile_pozycji']:(self.request.session['page']*self.request.session['ile_pozycji'])+self.request.session['ile_pozycji']]



                if not context['an_list']:
                    if not self.request.session['page'] == 0:
                        self.request.session['page'] = self.request.session['page'] - 1
                        context['an_list'] = an_list[self.request.session['page']*self.request.session['ile_pozycji']:(self.request.session['page']*self.request.session['ile_pozycji'])+self.request.session['ile_pozycji']]
                    else:
                        del self.request.session['tags']
                        context['not_found'] = "Zgubiłeś się Onii-chan?"

                #del self.request.session['tags']

            elif 'tags_nm' in self.request.session:

                context['an_list'] = Anime_list.objects.filter(key_map__title__contains=self.request.session['tags_nm']).order_by('key_map__title')
                context['page_max'] = math.ceil(context['an_list'].count() / self.request.session['ile_pozycji'])
                context['an_list'] = context['an_list'][self.request.session['page']*self.request.session['ile_pozycji']:(self.request.session['page']*self.request.session['ile_pozycji'])+self.request.session['ile_pozycji']]

                if not context['an_list']:
                    if not self.request.session['page'] == 0:
                        self.request.session['page'] = self.request.session['page'] - 1
                        context['an_list'] = Anime_list.objects.filter(key_map__title__contains=self.request.session['tags_nm']).order_by('key_map__title')[self.request.session['page']*self.request.session['ile_pozycji']:(self.request.session['page']*self.request.session['ile_pozycji'])+self.request.session['ile_pozycji']]
                    else:
                        del self.request.session['tags_nm']
                        context['not_found'] = "Zgubiłeś się Onii-chan?"

            else:
                context['an_list'] = Anime_list.objects.all().order_by('key_map__title')[self.request.session['page']*self.request.session['ile_pozycji']:(self.request.session['page']*self.request.session['ile_pozycji'])+self.request.session['ile_pozycji']]
                if not self.request.session['page'] == 0 and not context['an_list']:
                    self.request.session['page'] = self.request.session['page'] - 1
                    context['an_list'] = Anime_list.objects.all().order_by('key_map__title')[self.request.session['page']*self.request.session['ile_pozycji']:(self.request.session['page']*self.request.session['ile_pozycji'])+self.request.session['ile_pozycji']]
        except:
            context['an_list'] =  Anime_list.objects.all().order_by('key_map__title')[self.request.session['page']*self.request.session['ile_pozycji']:(self.request.session['page']*self.request.session['ile_pozycji'])+self.request.session['ile_pozycji']]
            if not self.request.session['page'] == 0 and not context['an_list']:
                    self.request.session['page'] = self.request.session['page'] - 1
                    context['an_list'] =  Anime_list.objects.all().order_by('key_map__title')[self.request.session['page']*self.request.session['ile_pozycji']:(self.request.session['page']*self.request.session['ile_pozycji'])+self.request.session['ile_pozycji']]

        context['page'] = self.request.session['page'] + 1

        return context

    def post(self, request, *args, **kwargs):
        form = QueryTags(request.POST)

        if 'page_ch' in request.POST:
            self.request.session['page'] = int(request.POST.get('page_ch')) - 1

        elif 'ses_cl' in request.POST:
            self.request.session['page'] = 0
            try:
                del self.request.session['tags_nm']
            except:
                pass

            try:
                del self.request.session['tags']
            except:
                pass
            return redirect("fumetsu-list")

        elif 'page_12' in request.POST:
            self.request.session['ile_pozycji'] = 12
            self.request.session['page'] = 0
        elif 'page_24' in request.POST:
            self.request.session['ile_pozycji'] = 24
            self.request.session['page'] = 0
        elif 'page_48' in request.POST:
            self.request.session['ile_pozycji'] = 48
            self.request.session['page'] = 0
        elif form.is_valid():
            self.request.session['page'] = 0
            
            if form.cleaned_data.get('name') and form.cleaned_data.get('ch_box'):
                self.request.session['tags_nm'] = form.cleaned_data.get('name')

                tags = []
                self.request.session['tags'] = {}
                for ix in form.cleaned_data.get('ch_box'):
                    tags.append(ix.title)

                self.request.session['tags'] = tags
                del tags

            elif form.cleaned_data.get('name'):
                try:
                    del self.request.session['tags']
                except:
                    pass
                self.request.session['tags_nm'] = form.cleaned_data.get('name')
                
            elif form.cleaned_data.get('ch_box'):
                try:
                    del self.request.session['tags_nm']
                except:
                    pass
                tags = []
                self.request.session['tags'] = {}
                for ix in form.cleaned_data.get('ch_box'):
                    tags.append(ix.title)

                self.request.session['tags'] = tags
                del tags


       

        else:
            messages.error(request, f'nie podałeś nic do wyszukiwania')#coś tu się zjebało DRUPAT!!!

        return redirect("fumetsu-list")
