from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from fumetsu.models import Series_comment, Anime_list
from .models import Tags_map, Episode_comment
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from captcha.fields import ReCaptchaField, ReCaptchaV2Checkbox 

class CreateComment(forms.ModelForm):

    content = forms.CharField(max_length=254,
        label="Komentarz (minimum 10 znaków)",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Napisz swój komentarz.",
                'class': 'komentarz',
                "rows":3,
            }
        )
    )

    class Meta:
        model = Series_comment
        fields = ['content']


class CreateCommentEp(forms.ModelForm):
    content = forms.CharField(max_length=254,
        label="Komentarz (minimum 10 znaków)",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Napisz swój komentarz.",
                'class': 'komentarz',
                 "rows":3,
            }
        )
    )

    class Meta:
        model = Episode_comment
        fields = ['content']


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

    ch_box = forms.ModelMultipleChoiceField(
                       widget = forms.CheckboxSelectMultiple,
                       label="Tagi.",
                       required=False,
                       queryset = Tags_map.objects.all().only("title")
               )

    class Meta:
        model = Anime_list
        fields = ['name','ch_box']
