from django import forms
from .models import BookComment


class BookCommentForm(forms.Form):
    class Meta:
        model = BookComment
        fields = ['title', 'content']


class BookCommentReportForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)  # 投诉理由