from django import forms
from .models import TopicPost


class TopicPostForm(forms.ModelForm):
    class Meta:
        model = TopicPost
        fields = ['title', 'body']
