from django.urls import path

from . import views

urlpatterns = [
    path("<str:imdb_id>/rate/", views.rate_title, name="rate_title"),
    path("<str:imdb_id>/watchlist/", views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("history/", views.history, name="history"),
]
