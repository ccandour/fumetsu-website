from django import forms
from fumetsu.models import Series_comment
from .models import Episode_comment


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
        model = Series_comment
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
        model = Episode_comment
        fields = ['content']
