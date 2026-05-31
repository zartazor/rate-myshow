from django.db.models import Avg
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from apps.ratings.models import Rating, Watchlist
from apps.recommendations.services.recommender import get_recommendations_for_user
from .models import Genre, Title
from .services.omdb import OmdbError, upsert_title_from_omdb


def title_detail(request, imdb_id):
    title = Title.objects.filter(omdb_id=imdb_id).first()
    if not title:
        title = upsert_title_from_omdb(imdb_id)
    if not title:
        raise Http404("Title not found")

    ratings = Rating.objects.filter(title=title).select_related("user")
    avg_rating = ratings.aggregate(avg=Avg("score"))["avg"] or 0
    score_steps = [x / 2 for x in range(2, 21)]
    distribution = {str(score): ratings.filter(score=score).count() for score in score_steps}

    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(user=request.user, title=title).exists()

    recommended = []
    if request.user.is_authenticated:
        recommended = get_recommendations_for_user(request.user, limit=6)

    return render(
        request,
        "titles/detail.html",
        {
            "title": title,
            "ratings": ratings,
            "avg_rating": avg_rating,
            "distribution": distribution,
            "in_watchlist": in_watchlist,
            "recommended": recommended,
        },
    )


def top_movies(request):
    titles = (
        Title.objects.filter(type="movie")
        .annotate(avg=Avg("rating__score"))
        .order_by("-avg")[:250]
    )
    return render(request, "titles/top_list.html", {"titles": titles, "list_name": "Top 250 Movies"})


def top_tv(request):
    titles = (
        Title.objects.filter(type="series")
        .annotate(avg=Avg("rating__score"))
        .order_by("-avg")[:250]
    )
    return render(request, "titles/top_list.html", {"titles": titles, "list_name": "Top 250 TV Shows"})


def genres(request, genre_id=None):
    all_genres = Genre.objects.all().order_by("name")
    selected = None
    titles = Title.objects.none()

    if genre_id:
        selected = get_object_or_404(Genre, id=genre_id)
        titles = Title.objects.filter(genres=selected)

    return render(
        request,
        "titles/genres.html",
        {"genres": all_genres, "selected": selected, "titles": titles},
    )
