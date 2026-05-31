from django.urls import path

from . import views

urlpatterns = [
    path("<str:imdb_id>/", views.title_detail, name="title_detail"),
    path("top/movies/", views.top_movies, name="top_movies"),
    path("top/tv/", views.top_tv, name="top_tv"),
    path("genres/", views.genres, name="genres"),
    path("genres/<int:genre_id>/", views.genres, name="genre_detail"),
]
