from django.shortcuts import render, redirect
from .models import Info_bd, Anime_list, Post_comment
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User

from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from anime.models import Episode_comment

from django.forms import modelformset_factory

from anime.models import Tags_map, Tags, Post, Player_valid
from datetime import datetime

from .ban import check_ban
from django.contrib.auth import logout

from django.db.models import Q

from django.http import Http404, HttpResponseRedirect
from django.urls import reverse


class Home(ListView):
    model = Post
    template_name = 'fumetsu/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anime'] = Post.objects.all().order_by('-odc_nm__date_posted')[:4]
        context['info'] = Info_bd.objects.all().order_by('-date_posted')[:3]
        return context


class about(ListView):
    model = Post
    template_name = 'fumetsu/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class google_auth(ListView):
    model = Post
    template_name = 'fumetsu/google5299714afc51785a.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Info(ListView):
    model = Post
    context_object_name = 'posts'
    queryset = Info_bd.objects.all().order_by('-date_posted')
    template_name = 'fumetsu/info.html'


class Info_d(ListView):
    model = Post
    template_name = 'fumetsu/info_d.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        post_h = Info_bd.objects.filter(idd=self.kwargs['pkk']).first()
        context['content'] = post_h
        context['form'] = CreateComment()
        context['comment'] = Post_comment.objects.filter(post_map=post_h).order_by('-date_posted')
        return context

    def post(self, request, *args, **kwargs):
        form = CreateComment(request.POST)

        if form.is_valid():
            if 'com_cr_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    k_m = get_object_or_404(Info_bd, idd=self.kwargs['pkk'])
                    f_save = form.save(commit=False)
                    f_save.post_map = k_m
                    f_save.author = request.user
                    f_save.save()
                    messages.success(request, f'Dodatno komentarz')
                else:
                    messages.success(request, f'komentarz jest za krótki')

            elif 'com_up_bt' in request.POST:
                if len(form.cleaned_data.get('content')) > 9:
                    idd = request.POST.get("idd", "")
                    t_save = Post_comment.objects.filter(id=idd).first()
                    if t_save.author == request.user and idd:
                        f_save = form.save(commit=False)

                        t_save.content = form.cleaned_data.get('content')
                        t_save.date_posted = datetime.now()
                        t_save.save()
                messages.success(request, f'Poprawiono komentarz')


        elif 'com_up_del' in request.POST:
            idd = request.POST.get("idd", "")
            t_save = Post_comment.objects.filter(id=idd).first()
            if t_save.author == request.user and idd:
                t_save.delete()
                messages.success(request, f'Usunięto komentarz')
            else:
                messages.error(request, f'Nie udało się usunąć konta')  #coś tu się zjebało DRUPAT!!!

        return redirect('fumetsu-infod', self.kwargs['pkk'])


#działa
class Cre_series(ListView):
    model = Post
    template_name = 'fumetsu/cre_series.html'

    def get_user(self, *args, **kwargs):
        return (self.request.user.groups.filter(name='content_creator').exists())

    def dispatch(self, *args, **kwargs):
        if self.get_user():
            return super(Cre_series, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SeriersForm()
        context['tags_add'] = Tags_add()
        context['tags_del'] = Tags_del()

        try:
            ex = modelformset_factory(Harmonogram, extra=2, form=HarmonForm)
            context['form_h'] = ex(queryset=Harmonogram.objects.all())

        except:
            pass

        return context

    def post(self, request, *args, **kwargs):
        try:
            ex = modelformset_factory(Harmonogram, extra=2, form=HarmonForm)
            harmon_form = ex(request.POST)

            for form in harmon_form:
                if form.is_valid():
                    harmon_post = form.save(commit=False)
                    if form.cleaned_data.get('ch_box'):
                        harmon_post.delete()
                    elif form.cleaned_data.get('day') < 0:
                        pass
                    elif form.cleaned_data.get('day') > 7:
                        pass
                    elif form.cleaned_data.get('key_map'):
                        if form.cleaned_data.get('content'):
                            harmon_post.save()

                    del harmon_post

            messages.success(request, "Zmieniono harmonogram")

            return redirect('Cre-ser')

        except:
            form_p = SeriersForm(request.POST, request.FILES)
            form_t = Tags_add(request.POST)
            form_td = Tags_del(request.POST)

            if form_p.is_valid():
                try:
                    idd = (Anime_list.objects.all().order_by('-id_anime').first().id_anime + 1)
                except:
                    idd = 0

                f_k = Anime_list()
                f_k.id_anime = idd
                f_k.title = form_p.cleaned_data.get('title')
                web_name = ''.join(e for e in f_k.title if e.isalnum())
                f_k.web_name = web_name
                f_k.save()

                f_cr = form_p.save(commit=False)
                f_cr.id_anime = idd
                f_cr.key_map = f_k
                f_cr.save()

                for ta in form_p.cleaned_data.get('Tags'):
                    f_t = Tags()
                    ids = Tags_map.objects.filter(title=ta).first()
                    f_t.tags_map = ids
                    f_t.key_map = f_k  #chyba tu
                    f_t.save()
                    del f_t

                messages.success(request, "Dodano anime.")
            elif form_td.is_valid():  #popraw usuń tag
                q_t = Tags_map.objects.filter(title__iexact=form_td.cleaned_data.get('title')).first()
                #f_t = form_td.save(commit=False)
                if form_td.cleaned_data.get('new_title'):
                    q_t.title = form_td.cleaned_data.get('new_title')
                    q_t.save()
                    messages.success(request, "poprawiono tag.")
                else:
                    q_t.delete()
                    messages.success(request, "Usunięto tag.")

            elif form_t.is_valid():  #nowy tag
                f_t = form_t.save(commit=False)
                if form_t.cleaned_data.get('title'):
                    if not Tags_map.objects.filter(title__iexact=form_t.cleaned_data.get('title')):
                        f_t.save()
                        messages.success(request, "Dodano tag.")
                    else:
                        messages.success(request, "Tagi tag już istneje.")
                else:
                    messages.success(request, "Podaj tag.")
            else:
                messages.success(request, "cosik się popsuło. Jeszcze raz.")

            return redirect('Cre-ser')


#to działa w 100%
class Cre_ani(TemplateView):
    template_name = 'fumetsu/cre_ani.html'

    def get_user(self, *args, **kwargs):
        return (self.request.user.groups.filter(name='Uploader').exists())

    def dispatch(self, *args, **kwargs):
        if self.get_user():
            return super(Cre_ani, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_up'] = Form_upload()
        context['form_ep_ch'] = LinkForm()
        context['form_ch_ep'] = LinkFormEp()
        context['form_season'] = SeasonForm()

        try:
            k_m = get_object_or_404(Anime_list, web_name=self.request.session['key_map'])
        except:
            pass

        try:
            ex = modelformset_factory(Anime_url, extra=2, form=Form_ch_url)
            context['form_ep_fix'] = ex(queryset=Anime_url.objects.filter(
                key_map=k_m,
                ep_nr=self.request.session['urls_ep'])
            )
        except:
            pass

        try:
            ex_e = modelformset_factory(Post, extra=0, form=Form_upload_edit)
            ex_f = ex_e(queryset=Post.objects.filter(
                odc_nm__key_map=k_m,
                odc_nm__ep_nr=self.request.session['urls_ep'])
            )

            context['form_upload_edit'] = ex_f
            ex_o = modelformset_factory(Odc_name, extra=0, form=Form_upload_edit_t)
            ex_o = ex_o(queryset=Odc_name.objects.filter(
                key_map=k_m,
                ep_nr=self.request.session['urls_ep'])
            )
            context['form_upload_edit_t'] = ex_o
            context['napisy'] = Odc_name.objects.filter(key_map=k_m,
                                                        ep_nr=self.request.session['urls_ep']).first().napisy
        except:
            pass
            #daj jakieś info ze nie ma

        return context

    def post(self, request, *args, **kwargs):
        form = Form_upload(request.POST, request.FILES)
        form_ch = LinkForm(request.POST)
        form_ch_ep = LinkFormEp(request.POST)

        #popraw linka
        try:
            ex = modelformset_factory(Anime_url, extra=3, form=Form_ch_url)
            urls_form = ex(request.POST)

            if urls_form.is_valid():
                Key_mp = get_object_or_404(Anime_list, web_name=self.request.session['key_map'])
                for form in urls_form:
                    urls_post = form.save(commit=False)
                    if form.cleaned_data.get('ch_box'):
                        urls_post.delete()
                    elif form.cleaned_data.get('link'):
                        urls_post.key_map = Key_mp
                        urls_post.odc_nm = Odc_name.objects.filter(key_map=Key_mp,
                                                                   ep_nr=self.request.session['urls_ep']).first()
                        urls_post.title = f"Anime: {Key_mp.title} i odc: {self.request.session['urls_ep']}"
                        urls_post.web_site = form.cleaned_data.get('web_site')
                        urls_post.ep_nr = self.request.session['urls_ep']
                        urls_post.link = form.cleaned_data.get('link')
                        urls_post.save()
                    del urls_post

                messages.success(request, self.request.session['key_map'])
                messages.success(request, "Dodano linki")
                return redirect('Cre-ani')

        except:
            pass

        try:
            ex = modelformset_factory(Post, extra=0, form=Form_upload_edit)
            urls_form = ex(request.POST, request.FILES)

            if urls_form.is_valid():
                if urls_form[0].cleaned_data.get('ch_box'):
                    for form in urls_form:
                        urls_post = form.save(commit=False)
                        urls_post.delete()
                    #urls_form.delete()
                else:
                    urls_form.save()
                messages.success(request, "Poprawiono posta")
                return redirect('Cre-ani')

        except:
            pass

        try:
            ex_o = modelformset_factory(Odc_name, extra=0, form=Form_upload_edit_t)
            urls_form_t = ex_o(request.POST, request.FILES)

            if urls_form_t.is_valid():
                if urls_form_t[0].cleaned_data.get('ch_box'):
                    for form in urls_form_t:
                        urls_post = form.save(commit=False)
                        urls_post.delete()
                    #urls_form_t.delete()
                else:
                    urls_form_t.save()
                messages.success(request, "Poprawiono odcinek")
                return redirect('Cre-ani')

        except Exception as e:
            pass

        #dodaj odc to juz dziala 25.12
        form = Form_upload(request.POST, request.FILES)
        form_season = SeasonForm(request.POST)

        if form.is_valid():
            if 'add_post' in request.POST:
                try:
                    self.request.session['key_map'] = get_object_or_404(Anime_list, title=form.cleaned_data.get(
                        'key_map').title).web_name
                    self.request.session['urls_ep'] = form.cleaned_data.get('ep_title')
                    test = Odc_name.objects.filter(key_map=form.cleaned_data.get('key_map'),
                                                   ep_title=form.cleaned_data.get('ep_title')).first()
                    messages.success(request, test)
                    if not test:

                        f_cr = form.save(commit=False)
                        try:
                            last_ep_nr = Odc_name.objects.filter(key_map=form.cleaned_data.get('key_map')).latest(
                                'ep_nr').ep_nr
                            f_cr.ep_nr = last_ep_nr + 1
                        except:
                            f_cr.ep_nr = 1

                        form.save()

                        f_post = Post()
                        f_post.odc_nm = Odc_name.objects.filter(key_map=form.cleaned_data.get('key_map'),
                                                                ep_title=form.cleaned_data.get('ep_title')).first()
                        f_post.content = form.cleaned_data.get('content')
                        f_post.image = form.cleaned_data.get('image')
                        f_post.save()

                    else:
                        messages.success(request, "Ten odc już istneje")
                except:
                    messages.success(request, "nie stworzono posta")
            return redirect('Cre-ani')

        elif form_season.is_valid():
            if 'season_post' in request.POST:
                if form_season.cleaned_data['anime_f'] != form_season.cleaned_data['anime_d']:
                    key_anime_f = get_object_or_404(Anime_list, title=form_season.cleaned_data['anime_f'])
                    key_anime_s = get_object_or_404(Anime_list, title=form_season.cleaned_data['anime_d'])
                    f_season = form_season.save(commit=False)
                    f_season.id_anime_f = key_anime_f.id_anime
                    f_season.id_anime_s = key_anime_s.id_anime

                    f_season_s = Season()
                    f_season_s.id_anime_f = key_anime_s.id_anime
                    f_season_s.id_anime_s = key_anime_f.id_anime
                    f_season_s.description = form_season.cleaned_data['description_s']
                    f_season_s.save()
                    f_season.save()
                    messages.success(request, "Dodano powiazanie.")

        elif form_ch.is_valid():  #wyświetlanie odc do poprawy
            if 'check_urls' in request.POST:
                Key_mp = get_object_or_404(Anime_list, title=form.cleaned_data.get('key_map').title)
                self.request.session['key_map'] = Key_mp.web_name

                messages.success(request, "Wybierz odc.")


        elif form_ch_ep.is_valid():
            if 'check_urls_ep' in request.POST:
                self.request.session['urls_ep'] = form_ch_ep.cleaned_data.get('ep_nr')
                messages.success(request, "wybrano.")

        else:
            messages.success(request, "cosik się popsuło. Jeszcze raz.")

        return redirect('Cre-ani')


#teraz tu
class Ed_an(TemplateView):
    template_name = 'fumetsu/edit_an.html'

    def get_user(self, *args, **kwargs):
        return (self.request.user.groups.filter(name='Uploader').exists())

    def dispatch(self, *args, **kwargs):
        if self.get_user():
            return super(Ed_an, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_an_ch'] = LinkForm()
        context['form_an_url'] = EditUrl()

        try:
            key_mp = get_object_or_404(Anime_list, web_name=self.request.session['key_map'])
            ex = modelformset_factory(Anime_list, extra=0, form=AnimeEdForm)
            context['form_an'] = ex(queryset=Anime_list.objects.filter(
                key_map=key_mp)
            )

            ex_k = modelformset_factory(Anime_list, extra=0, form=AnimeEdFormKey)
            context['form_key'] = ex_k(queryset=Anime_list.objects.filter(
                web_name=key_mp.web_name)
            )

            ex_t = modelformset_factory(Tags, extra=2, form=AnimeEdFormTag)
            context['form_tag'] = ex_t(queryset=Tags.objects.filter(
                key_map=key_mp)
            )

            context['ed_an'] = key_mp


        except:
            pass

        return context

    def post(self, request, *args, **kwargs):

        if 'upd_dis' in request.POST:
            try:
                ex = modelformset_factory(Anime_list, extra=0, form=AnimeEdForm)
                an_form = ex(request.POST, request.FILES)

                if an_form.is_valid():
                    an_form.save()
                    messages.success(request, "Poprawiono anime.")
                    return redirect('ed-an')
                else:
                    messages.success(request, "nie udało się poprawić anime.")
                    return redirect('ed-an')
            except:
                pass

        elif 'ed_url' in request.POST:
            form_url = EditUrl(request.POST)
            if form_url.is_valid():
                f_url = form_url.save(commit=False)
                web_name = ''.join(e for e in f_url.web_name if e.isalnum())
                if not Anime_list.objects.filter(web_name=web_name).first():
                    query_url = Anime_list.objects.filter(web_name=self.request.session['key_map']).first()
                    query_url.web_name = web_name
                    query_url.save()
                    self.request.session['key_map'] = web_name
                    messages.success(request, "poprawiono url anime.")
                else:
                    messages.success(request, "Taki url istnieje.")

        elif 'upd_tg' in request.POST:
            try:
                ext = modelformset_factory(Tags, extra=2, form=AnimeEdFormTag)
                at_form = ext(request.POST)
                if at_form.is_valid():
                    Key_mp = get_object_or_404(Anime_list, web_name=self.request.session['key_map'])
                    for form in at_form:
                        at_f = form.save(commit=False)
                        if form.cleaned_data.get('ch_box'):
                            at_f.delete()
                        elif form.cleaned_data.get('tags_map') is not None:
                            at_f.key_map = Key_mp
                            at_f.save()
                            del at_f
                    messages.success(request, "Poprawiono Tagi.")
            except:
                messages.success(request, "Nie udało się poprawić tagów.")
        elif 'upd_nm' in request.POST:
            try:
                exk = modelformset_factory(Anime_list, extra=0, form=AnimeEdFormKey)
                k_form = exk(request.POST)
                if k_form.is_valid():
                    po_k = k_form[0].save(commit=False)
                    if request.POST.get("zmiana", ""):
                        web_name = ''.join(e for e in po_k.title if e.isalnum())
                        po_k.web_name = web_name
                        self.request.session['key_map'] = web_name
                    po_k.save()
                    messages.success(request, "Poprawiono nazwę.")
                else:
                    messages.success(request, "Nie udało się poprawić nazwy.")
            except:
                pass
        elif 'check_urls' in request.POST:
            form = LinkForm(request.POST)
            if form.is_valid():
                Key_mp = get_object_or_404(Anime_list, title=form.cleaned_data.get('key_map').title)
                if Key_mp:
                    self.request.session['key_map'] = Key_mp.web_name
                else:
                    messages.success(request, "Nie znaleziono takiego odc.")
                    try:
                        del self.request.session['key_map']
                    except:
                        pass

        return redirect('ed-an')


class Cre_info(TemplateView):
    template_name = 'fumetsu/cre_info.html'

    def get_user(self, *args, **kwargs):
        return (self.request.user.groups.filter(name='Informator').exists())

    def dispatch(self, *args, **kwargs):
        if self.get_user():
            return super(Cre_info, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = InfoForm()

        context['form_pref'] = InfoForm_pref()

        try:
            ex = modelformset_factory(Info_bd, extra=0, form=InfoForm_change)
            context['form_change'] = ex(queryset=Info_bd.objects.filter(
                id=self.request.session['post_change'])
            )
        except:
            pass

        return context

    def post(self, request, *args, **kwargs):

        try:
            ex = modelformset_factory(Info_bd, extra=0, form=InfoForm_change)
            an_form = ex(request.POST, request.FILES)
            if an_form.is_valid():
                an_form.save()
                messages.success(request, "Poprawiono posta.")
                return redirect('Cre-info')
            else:
                messages.success(request, "Nie poprawiono posta.")
                return redirect('Cre-info')
        except:
            form = InfoForm(request.POST, request.FILES)
            Form_pref = InfoForm_pref(request.POST)

            if form.is_valid():
                f_cr = form.save(commit=False)
                if Info_bd.objects.all().exists():
                    idd = Info_bd.objects.all().order_by('-date_posted').first().idd + 1
                else:
                    idd = 1
                f_cr.idd = idd
                f_cr.save()
                del f_cr
                messages.success(request, "Dodano posta.")
                return redirect('fumetsu-infod', idd)
            elif Form_pref.is_valid():
                self.request.session['post_change'] = form.cleaned_data.get('title')  #daje id
                return redirect('Cre-info')
            else:
                messages.success(request, "cosik się popsuło. Jeszcze raz.")
                return redirect('Cre-info')


class Link_error(TemplateView):
    model = Player_valid

    template_name = 'fumetsu/link_error.html'

    def get_user(self, *args, **kwargs):
        return (self.request.user.groups.filter(Q(name='Moderator') | Q(name='Uploader')).exists())

    def dispatch(self, *args, **kwargs):
        if self.get_user():
            return super(Link_error, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Player_valid.objects.all()

        return context

    def post(self, request, *args, **kwargs):

        od_nm = Player_valid.objects.filter(key_map_ep__key_map__id_anime=request.POST.get("hrfd", "")).first()
        od_nm.delete()
        messages.success(request, f'Usunięto skarge')

        return redirect('lnk-err')
