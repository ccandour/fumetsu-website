from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

from django.forms.models import modelformset_factory
from django.utils.translation import gettext_lazy as _


class SeriersForm(forms.ModelForm):


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
        model = KH_Anime_list
        fields = ['title','content','image','image_bg']

        labels = {
            'content': _('Opis Anime'),
            'image': _('Zdjęcie okładki')
        }



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
        model = KH_Odc_name
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
        model = KH_Post
        fields = ['content','image','ch_box']

class LinkForm(forms.ModelForm):

    class Meta:
        model = KH_Anime_list
        fields = ['key_map']

class LinkFormEp(forms.ModelForm):

    class Meta:
        model = KH_Odc_name
        fields = ['ep_nr']

class SeriersForm(forms.ModelForm):

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
        model = KH_Anime_list
        fields = ['title','content','image','image_bg']

        labels = {
            'content': _('Opis Anime'),
            'image': _('Zdjęcie okładki') 
        }

class QueryTags(forms.ModelForm):
    name = forms.CharField(max_length=254,
        label="wyszukaj po nazwie.",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "nazwa anime",
                'class': 'search',
            }
        )
    )
    class Meta:
        model = KH_Anime_list
        fields = ['name']

class Form_ch_url(forms.ModelForm):

    link = forms.CharField(widget=forms.Textarea())
    ch_box = forms.BooleanField(label=_('Usuń całkowice'), required=False)

    class Meta:
        model = KH_Anime_url
        fields = ['web_site','link','ch_box']

        labels = {
            'web_site': _('nazwa playera'),
            'link': _('link do ifame'),
        }


class Form_upload_edit_t(forms.ModelForm):
    title = forms.CharField(
        label="Tytuł odcinka",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tytuł"
            }
        )
    )

    napisy = forms.FileField(label="Napisy .zip albo .txt", required=False, widget=forms.FileInput)

    ch_box = forms.BooleanField(label=_('Usuń całkowice odcinek i posta'), required=False)

    class Meta:
        model = KH_Odc_name
        fields = ['ep_title', 'title', 'napisy', 'ch_box']