from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *
from anime.models import Odc_name, Tags_map, Post, Anime_url, Tags

from django.forms.models import modelformset_factory
from django.utils.translation import gettext_lazy as _

class Form_upload(forms.ModelForm):

    content = forms.CharField(max_length=254,
        label="Opis odcinka",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Opis odcinka."
            }
        )
    )

    image = forms.FileField()

    napisy = forms.FileField(label="Napisy .zip albo .txt", required = False, widget=forms.FileInput)

    class Meta:
        model = Odc_name
        fields = ['key_map','ep_title','title','content','napisy','image']

class Form_upload_edit(forms.ModelForm):

    content = forms.CharField(max_length=254,
        label="Opis posta do odcinka",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Opis."
            }
        )
    )

    ch_box = forms.BooleanField(label=_('Usuń całkowice post'), required=False)

    class Meta:
        model = Post
        fields = ['content','image','ch_box']

class Form_upload_edit_t(forms.ModelForm):

    title = forms.CharField(
        label="Tytuł odcinka",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tytuł"
            }
        )
    )
    
    napisy = forms.FileField(label="Napisy .zip albo .txt", required = False, widget=forms.FileInput)

    ch_box = forms.BooleanField(label=_('Usuń całkowice odcinek i posta'), required=False)

    class Meta:
        model = Odc_name
        fields = ['ep_title','title','napisy','ch_box']

class SeasonForm(forms.ModelForm):
    anime_f = forms.ModelChoiceField(queryset=Key_map.objects.all(),label=_('Jakie anime:'))
    anime_d = forms.ModelChoiceField(queryset=Key_map.objects.all(),label=_('do jakiego anime'))
    description_s = forms.CharField(widget=forms.Textarea(),label=_('powiazanie miedzy drugim a pierwszym'))

    class Meta:
        model = Season
        fields = ['anime_f','anime_d','description','description_s']

        labels = {
            'description': _('powiazanie miedzy pierwszym a drugim'),
        }


class LinkForm(forms.ModelForm):

    class Meta:
        model = Anime_url
        fields = ['key_map']

class LinkFormEp(forms.ModelForm):

    class Meta:
        model = Odc_name
        fields = ['ep_nr']


class AnimeEdForm(forms.ModelForm):


    class Meta:
        model = Anime_list
        fields = ['content','image','image_bg','napisy']

        labels = {
            'content': _('Opis anime'),
            'image': _('Zdjęcie'),
        }

class AnimeEdFormTag(forms.ModelForm):
    ch_box = forms.BooleanField(label=_('Usuń całkowice odcinek i posta'), required=False)

    class Meta:
        model = Tags
        fields = ['tags_map']

class AnimeEdFormKey(forms.ModelForm):

    class Meta:
        model = Key_map
        fields = ['title']        

class Form_ch_url(forms.ModelForm):

    link = forms.CharField(widget=forms.Textarea())
    ch_box = forms.BooleanField(label=_('Usuń całkowice'), required=False)

    class Meta:
        model = Anime_url
        fields = ['web_site','link','ch_box']

        labels = {
            'web_site': _('nazwa playera'),
            'link': _('link do ifame'),
        }


class InfoForm(forms.ModelForm):

    class Meta:
        model = Info_bd
        fields = ['title','content','image']

class InfoForm_pref(forms.ModelForm):

    title = forms.ModelChoiceField(queryset=Info_bd.objects.all())

    class Meta:
        model = Info_bd
        fields = ['title']

class InfoForm_change(forms.ModelForm):

    class Meta:
        model = Info_bd
        fields = ['title','content','image']

class SeriersForm(forms.ModelForm):

    Tags = forms.ModelMultipleChoiceField(queryset=Tags_map.objects.only("title"),
            widget=forms.CheckboxSelectMultiple())

    title = forms.CharField(
        label="Tytuł Anime",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tytuł.",
                "rows":2,
                "cols":30
            }
        )
    )

    class Meta:
        model = Anime_list
        fields = ['title','content','image','image_bg','Tags']

        labels = {
            'content': _('Opis Anime'),
            'image': _('Zdjęcie okładki') 
        }

class HarmonForm(forms.ModelForm):

    ch_box = forms.BooleanField(label=_('Usuń całkowice (zaznacz jakie anime)'), required=False)

    class Meta:
        model = Harmonogram
        fields = ['key_map','content','day','ch_box']

        labels = {
            'content': _('Kiedy wychodzi'),
        }


class Tags_add(forms.ModelForm):

    title = forms.CharField(max_length=128,
        label="nazwa tagu.",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "nazwa tagu"
            }
        )
    )

    class Meta:
        model = Tags_map
        fields = ['title']

class Tags_del(forms.ModelForm):

    title = forms.ModelChoiceField(queryset=Tags_map.objects.all())

    new_title = forms.CharField(max_length=128,
        label="nowa nazwa tagu.",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "nazwa tagu"
            }
        )
    )

    class Meta:
        model = Tags_map
        fields = ['title','new_title']

class CreateComment(forms.ModelForm):

    content = forms.CharField(max_length=254,
        label="Komentarz (minimum 10 znaków)",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Napisz swój komentarz.",
                "rows":3,
                'class': 'komentarz',
            }
        )
    )

    class Meta:
        model = Post_comment
        fields = ['content']


class EditUrl(forms.ModelForm):

    class Meta:
        model = Key_map
        fields = ['web_name']