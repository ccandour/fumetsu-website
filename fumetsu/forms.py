from django import forms
from django.utils.safestring import mark_safe

from .models import *


class EditCommentForm(forms.ModelForm):
    content = forms.CharField(
        max_length=1024,
        label=mark_safe(
            'Komentarz (obsługuje <a href="https://www.markdownguide.org/basic-syntax/" target="_blank">Markdown</a>)'),
        widget=forms.Textarea(
            attrs={
                "placeholder": "Ale świetna seria! Nie mogę się doczekać kolejnego odcinka!",
                "class": "form-control form-control-lg focus-ring focus-ring-primary"
            }
        )
    )

    class Meta:
        model = PostComment
        fields = ['content']
