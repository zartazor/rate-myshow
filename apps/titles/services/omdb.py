import os
from datetime import timedelta

import requests
from django.core.cache import cache

from apps.titles.models import Actor, Genre, Title


OMDB_API_KEY = os.getenv("OMDB_API_KEY", "d5b0159b")
BASE_URL = "http://www.omdbapi.com/"
CACHE_TTL = 60 * 60 * 12


class OmdbError(Exception):
    pass


def _rate_limit():
    cache_key = "omdb:rate"
    count = cache.get(cache_key, 0)
    if count >= 5:
        raise OmdbError("Rate limit exceeded")
    cache.set(cache_key, count + 1, timeout=1)


def _fetch(params):
    _rate_limit()
    params["apikey"] = OMDB_API_KEY
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    payload = response.json()
    if payload.get("Response") == "False":
        raise OmdbError(payload.get("Error", "Unknown OMDB error"))
    return payload


def get_title(imdb_id):
    cache_key = f"omdb:title:{imdb_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    data = _fetch({"i": imdb_id, "plot": "full"})
    cache.set(cache_key, data, timeout=CACHE_TTL)
    return data


def search_titles(query, page=1):
    cache_key = f"omdb:search:{query}:{page}"
    cached = cache.get(cache_key)
    if cached:
        return cached
    data = _fetch({"s": query, "page": page})
    results = data.get("Search", [])
    cache.set(cache_key, results, timeout=CACHE_TTL)
    return results


def upsert_title_from_omdb(imdb_id):
    try:
        data = get_title(imdb_id)
    except OmdbError:
        return None

    title, _ = Title.objects.update_or_create(
        omdb_id=imdb_id,
        defaults={
            "title": data.get("Title", ""),
            "year": data.get("Year", ""),
            "type": data.get("Type", "movie"),
            "poster": data.get("Poster", ""),
            "data": data,
        },
    )

    genres = [g.strip() for g in data.get("Genre", "").split(",") if g.strip()]
    actors = [a.strip() for a in data.get("Actors", "").split(",") if a.strip()]

    if genres:
        genre_objs = [Genre.objects.get_or_create(name=genre)[0] for genre in genres]
        title.genres.set(genre_objs)
    if actors:
        actor_objs = [Actor.objects.get_or_create(name=actor)[0] for actor in actors]
        title.actors.set(actor_objs)

    return title
