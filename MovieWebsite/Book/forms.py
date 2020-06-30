from django import forms
from .models import BookComment,BookCommentReport


class BookCommentForm(forms.Form):
    class Meta:
        model = BookComment
        fields = ['title', 'content']


class BookCommentReportForm(forms.Form):
    class Meta:
        model = BookCommentReport
        fields = ['reporter', 'reason']