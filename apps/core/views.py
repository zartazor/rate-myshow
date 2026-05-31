from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from apps.ratings.models import Rating
from apps.recommendations.services.recommender import get_recommendations_for_user
from apps.titles.models import Title
from apps.titles.services.omdb import search_titles, upsert_title_from_omdb
from .constants import POPULAR_MOVIE_IDS, TOP_TV_IDS, TRENDING_IDS


def _hydrate_titles(omdb_ids):
    titles = []
    for omdb_id in omdb_ids:
        title = upsert_title_from_omdb(omdb_id)
        if title:
            titles.append(title)
    return titles


def home(request):
    trending = _hydrate_titles(TRENDING_IDS)
    popular_movies = _hydrate_titles(POPULAR_MOVIE_IDS)
    top_tv = _hydrate_titles(TOP_TV_IDS)

    recommended = []
    if request.user.is_authenticated:
        recommended = get_recommendations_for_user(request.user, limit=8)

    return render(
        request,
        "core/home.html",
        {
            "trending": trending,
            "popular_movies": popular_movies,
            "top_tv": top_tv,
            "recommended": recommended,
        },
    )


def search(request):
    query = request.GET.get("q", "").strip()
    page = int(request.GET.get("page", "1"))
    results = []
    if query:
        results = search_titles(query, page=page)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"results": results, "page": page})

    return render(request, "core/search.html", {"query": query, "results": results, "page": page})


@login_required
def activity(request):
    recent_ratings = Rating.objects.select_related("title", "user")[:20]
    return render(request, "core/activity.html", {"recent_ratings": recent_ratings})


def handler404(request, exception):
    return render(request, "404.html", status=404)


def handler500(request):
    return render(request, "500.html", status=500)
