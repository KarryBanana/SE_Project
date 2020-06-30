from django.conf.urls import url
from Book import views
from django.urls import re_path

urlpatterns = [
    url(r'^$', views.book_display, name='index'),
    url(r'^detail/(?P<id>.*)', views.book_detail, name='book_detail'),
    url(r'^book_display/', views.book_display, name='book_display'),
    url(r'^search/', views.book_search, name='search'),
    url(r'^genre/(?P<genre>[\w]+)/', views.book_search_by_genre, name='book_genre'),
    url(r'^add_comment/(?P<id>\d+)/', views.add_comment, name='add_comment'),
    url(r'^report_comment/(?P<comment_id>\d+)/', views.reportBookComment,name='report_comment'),
    url(r'digg/', views.digg, name='digg'),
]