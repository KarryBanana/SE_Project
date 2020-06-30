from django import forms
from .models import MovieComment,MovieCommentReport

class CommentForm(forms.Form):
    class Meta:
        model = MovieComment
        fields = ['title', 'content']


class MovieCommentReportForm(forms.Form):
    class Meta:
        model = MovieCommentReport
        fields = ['reporter', 'reason']
