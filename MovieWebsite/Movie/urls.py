"""Defines url patterns for Cinema_Pages"""

from django.urls import path, re_path
from Movie import views

urlpatterns = [
    # Home page.
    re_path(r'^$|^index$', views.movie_display, name='index'),
    re_path(r'^movie_display/', views.movie_display, name='movie_display'),
    re_path(r'^id/(?P<id>\d+)/', views.movie_detail, name='movie_detail'),
    re_path(r'^genre/(?P<genre>[\w]+)/', views.movie_search_by_genre, name='movie_genre'),
    re_path(r'^year/(?P<year>[0-9]{2,4})/', views.movie_search_by_year, name='movie_year'),
    re_path(r'^search/', views.movie_search_form, name='movie_search_form'),
    re_path(r'^add_comment/(?P<id>\d+)/', views.add_comment, name='add_comment'),
    re_path(r'^report_comment/(?P<comment_id>\d+)/', views.reportMovieComment, name='report_comment'),
    re_path(r'digg/', views.digg, name='digg'),

    # API
    re_path(r'^api/movie/id/(?P<id>[0-9]{6,})/', views.search_by_id),
    re_path(r'^api/movie/title/(?P<title>[\w]+)/', views.search_by_title),
    re_path(r'^api/movie/original_title/(?P<original_title>[\w\s]+)/', views.search_by_original_title),
    re_path(r'^api/movie/genre/(?P<genre>[\w]+)/', views.search_by_genre),
    re_path(r'^api/movie/year/(?P<year>[0-9]{4})/', views.search_by_year),


]
