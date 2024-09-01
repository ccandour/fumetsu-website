from django import forms
from fumetsu.models import SeriesComment
from .models import EpisodeComment


class CreateComment(forms.ModelForm):
    content = forms.CharField(max_length=254,
        label="Dodaj komentarz (minimum 10 znaków)",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Super seria!",
                "class": "form-control focus-ring focus-ring-primary",
                "rows": 3,
            }
        )
        )

    class Meta:
        model = SeriesComment
        fields = ['content']


class CreateCommentEp(forms.ModelForm):
    content = forms.CharField(max_length=254,
        label="Dodaj komentarz (minimum 10 znaków)",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Super odcinek!",
                "class": "form-control focus-ring focus-ring-primary",
                "rows": 3,
            }
        )
        )

    class Meta:
        model = EpisodeComment
        fields = ['content']
