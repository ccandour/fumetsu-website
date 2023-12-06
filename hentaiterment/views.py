from django.shortcuts import render, redirect

from django.views.generic import ListView
from django.views.generic.base import TemplateView

from .models import *
from .forms import *

from fumetsu.ban import check_ban
from django.contrib.auth import logout

from django.contrib import messages
from django.shortcuts import get_object_or_404

class KH_Home(ListView):
	model = KH_Post
	template_name = 'hentaiterment/index.html'

	def dispatch(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return super(KH_Home, self).dispatch(*args, **kwargs)
		else:
			return redirect('fumetsu-home')

	def get_context_data(self, **kwargs):

		try:
			if check_ban(self.request.user):
				logout(self.request)
		except:
			pass

		context = super().get_context_data(**kwargs)
		context['anime'] = KH_Post.objects.all().order_by('-odc_nm__date_posted')[:4]
		return context

class KH_upld(TemplateView): 
    template_name = 'hentaiterment/cr_an.html' 

    def get_user(self, *args, **kwargs):
        return (self.request.user.groups.filter(name='Biuro').exists())

    def dispatch(self, *args, **kwargs):
        if self.get_user():
            return super(KH_upld, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_up'] = Form_upload()
        context['form_ep_ch'] = LinkForm()
        context['form_ch_ep'] = LinkFormEp()
        
        try:
            k_m = get_object_or_404(KH_Key_map, web_name = self.request.session['key_map'])
        except:
            pass

        try:
            ex = modelformset_factory(KH_Anime_url, extra=2, form=Form_ch_url)
            context['form_ep_fix'] = ex(queryset=KH_Anime_url.objects.filter(
                odc_nm__key_map = k_m,
                ep_nr = self.request.session['urls_ep'])
            )
        except:
            pass



        try:
            ex_e = modelformset_factory(KH_Post, extra=0, form=Form_upload_edit)
            ex_f = ex_e(queryset=KH_Post.objects.filter(
                odc_nm__key_map = k_m,
                odc_nm__ep_nr = self.request.session['urls_ep'])
            )
            
            context['form_upload_edit'] = ex_f
            ex_o = modelformset_factory(KH_Odc_name, extra=0, form=Form_upload_edit_t)
            ex_o = ex_o(queryset=KH_Odc_name.objects.filter(
                key_map = k_m,
                ep_nr = self.request.session['urls_ep'])
            )
            context['form_upload_edit_t'] = ex_o
            context['napisy'] = KH_Odc_name.objects.filter(key_map=k_m,ep_nr=self.request.session['urls_ep']).first().napisy
        except :
            pass
            #daj jakieś info ze nie ma hen_list
            
        return context


    def post(self, request, *args, **kwargs):
        form = Form_upload(request.POST,request.FILES)
        form_ch = LinkForm(request.POST)
        form_ch_ep = LinkFormEp(request.POST)
        
        #popraw linka
        try:
            ex = modelformset_factory(KH_Anime_url, extra=3, form=Form_ch_url)
            urls_form = ex(request.POST)

            if urls_form.is_valid():
                Key_mp = get_object_or_404(KH_Key_map, web_name = self.request.session['key_map'])
                for form in urls_form:
                    urls_post = form.save(commit=False)
                    if form.cleaned_data.get('ch_box'):
                        urls_post.delete()
                    elif form.cleaned_data.get('link'):
                        urls_post.key_map = Key_mp
                        urls_post.odc_nm = KH_Odc_name.objects.filter(key_map=Key_mp,ep_nr=self.request.session['urls_ep']).first()
                        urls_post.title = f"Anime: {Key_mp.title} i odc: {self.request.session['urls_ep']}"
                        urls_post.web_site = form.cleaned_data.get('web_site')
                        urls_post.ep_nr = self.request.session['urls_ep']
                        urls_post.link = form.cleaned_data.get('link')
                        urls_post.save()
                    del urls_post

                messages.success(request, self.request.session['key_map'])
                messages.success(request, "Dodano linki")
                return redirect('kh-upload')

        except:
            pass

        try:
            ex = modelformset_factory(KH_Post, extra=0, form=Form_upload_edit)
            urls_form = ex(request.POST,request.FILES)

            if urls_form.is_valid():
                if urls_form[0].cleaned_data.get('ch_box'):
                    for form in urls_form:
                        urls_post = form.save(commit=False)
                        urls_post.delete()
                    #urls_form.delete()
                else:
                    urls_form.save()
                messages.success(request, "Poprawiono posta")
                return redirect('kh-upload')

        except:
            pass

        try:
            ex_o = modelformset_factory(KH_Odc_name, extra=0, form=Form_upload_edit_t)
            urls_form_t = ex_o(request.POST,request.FILES)

            if urls_form_t.is_valid():
                if urls_form_t[0].cleaned_data.get('ch_box'):
                    for form in urls_form_t:
                        urls_post = form.save(commit=False)
                        urls_post.delete()
                    #urls_form_t.delete()
                else:
                    urls_form_t.save()
                messages.success(request, "Poprawiono odcinek")
                return redirect('kh-upload')

        except Exception as e:
            pass

        #dodaj odc to juz dziala 25.12
        form = Form_upload(request.POST,request.FILES)
        
        if form.is_valid():
            if 'add_post' in request.POST:
                try:
                    self.request.session['key_map'] = get_object_or_404(KH_Key_map, title=form.cleaned_data.get('key_map').title).web_name
                    self.request.session['urls_ep'] = form.cleaned_data.get('ep_title')
                    test = KH_Odc_name.objects.filter(key_map = form.cleaned_data.get('key_map'), ep_title = form.cleaned_data.get('ep_title')).first()
                    messages.success(request, test)
                    if not test:

                        f_cr = form.save(commit=False)
                        try:
                            last_ep_nr = KH_Odc_name.objects.filter(key_map = form.cleaned_data.get('key_map')).latest('ep_nr').ep_nr
                            f_cr.ep_nr = last_ep_nr+1
                        except:
                            f_cr.ep_nr = 0 

                        form.save()

                        f_post = KH_Post()
                        f_post.odc_nm = KH_Odc_name.objects.filter(key_map = form.cleaned_data.get('key_map'), ep_title = form.cleaned_data.get('ep_title')).first()
                        f_post.content = form.cleaned_data.get('content')
                        f_post.image = form.cleaned_data.get('image')
                        f_post.save()
                        
                    else:
                        messages.success(request, "Ten odc już istneje")
                except Exception as e:
                	raise e
                #except :
                #    messages.success(request, "nie stworzono posta")
            return redirect('kh-upload')

        elif form_ch.is_valid():#wyświetlanie odc do poprawy
            if 'check_urls' in request.POST:
                Key_mp = get_object_or_404(KH_Key_map, title = form.cleaned_data.get('key_map').title)
                self.request.session['key_map'] = Key_mp.web_name
                
                messages.success(request, "Wybierz odc.")


        elif form_ch_ep.is_valid():
            if 'check_urls_ep' in request.POST:
                self.request.session['urls_ep'] = form_ch_ep.cleaned_data.get('ep_nr')
                messages.success(request, "wybrano.")

        else:
            messages.success(request, "cosik się popsuło. Jeszcze raz.")
            
        return redirect('kh-upload')




class KH_Cre_series(ListView):
    model = KH_Post
    template_name = 'hentaiterment/cr_sr.html'

    def get_user(self, *args, **kwargs):
        return (self.request.user.groups.filter(name='Biuro').exists())

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(KH_Cre_series, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = SeriersForm()

        return context

    def post(self, request, *args, **kwargs):
        form_p = SeriersForm(request.POST, request.FILES)

        if form_p.is_valid():
            try:
                idd = (KH_Key_map.objects.all().order_by('-id_anime').first().id_anime + 1)
            except:
                idd = 0

            f_k = KH_Key_map()
            f_k.id_anime = idd
            f_k.title = form_p.cleaned_data.get('title')
            web_name = ''.join(e for e in f_k.title if e.isalnum())
            f_k.web_name = web_name
            f_k.save()

            f_cr = form_p.save(commit=False)
            f_cr.key_map = f_k
            f_cr.save()

            messages.success(request, "Dodano Hentaia.")

        return redirect('kh-create')




class KH_list(TemplateView):
    model = KH_Anime_list
    context_object_name = 'posts'
    template_name = 'hentaiterment/hen_list.html'
    fields = ['content']

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(KH_list, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):
        try:
            if check_ban(self.request.user):
                logout(self.request)
        except:
            pass

        context = super().get_context_data(**kwargs)


        context['an_list'] = KH_Anime_list.objects.all().order_by()

        return context


class Hentai_content(TemplateView):
    model = KH_Anime_list
    template_name = 'hentaiterment/hentai_index.html'
    fields = ['content']

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return super(Hentai_content, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')
    
    def get_context_data(self, **kwargs):
        try:
            if check_ban(self.request.user):
                logout(self.request)
        except:
            pass

        context = super().get_context_data(**kwargs)
        k_m = get_object_or_404(KH_Key_map, web_name = self.kwargs['hentai_name'])
        ani = KH_Anime_list.objects.filter(key_map=k_m)
        ani.web_name = k_m.web_name
        context['posts'] = ani

        context['ep'] = KH_Odc_name.objects.filter(key_map=k_m).order_by('ep_title')     
        
        return context

class KH_Anime_episode(TemplateView):
    model = KH_Anime_list
    context_object_name = 'posts'
    template_name = 'hentaiterment/hentai_ep_index.html'
    fields = ['content']
    


    def dispatch(self, *args, **kwargs):

        if self.request.user.is_authenticated:
            return super(KH_Anime_episode, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

        k_m = get_object_or_404(KH_Key_map, web_name = self.kwargs['hentai_name'])
        if KH_Odc_name.objects.filter(key_map=k_m, ep_nr=self.kwargs['ep']).first():
            return super(KH_Anime_episode, self).dispatch(*args, **kwargs)
        else:
            return redirect('fumetsu-home')

    def get_context_data(self, **kwargs):
        try:
            if check_ban(self.request.user):
                logout(self.request)
        except:
            pass

        context = super().get_context_data(**kwargs)
        k_m = get_object_or_404(KH_Key_map, web_name = self.kwargs['hentai_name'])
        ep = self.kwargs['ep']
        try:
        	context['link'] = KH_Anime_url.objects.filter(odc_nm__key_map=k_m, odc_nm__ep_nr=ep)
        except:
        	pass

        context['anime_nm'] = k_m

        ep_query = KH_Odc_name.objects.filter(key_map=k_m, ep_nr=ep).first()
        context['odc_html'] = ep_query


        if KH_Odc_name.objects.filter(key_map=k_m, ep_title__gt=ep_query.ep_title).order_by('ep_title').first():
            context['next'] = KH_Odc_name.objects.filter(key_map=k_m, ep_title__gt=ep_query.ep_title).order_by('ep_title').first()
        if KH_Odc_name.objects.filter(key_map=k_m, ep_title__lte=ep_query.ep_title).order_by('ep_title').first():
            context['prev'] = KH_Odc_name.objects.filter(key_map=k_m, ep_title__lt=ep_query.ep_title).order_by('-ep_title').first()
        del ep


        
        return context
