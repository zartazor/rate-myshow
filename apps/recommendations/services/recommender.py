import numpy as np
from django.core.cache import cache
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from apps.ratings.models import Rating
from apps.titles.models import Title


def _title_corpus(titles):
    corpus = []
    for title in titles:
        genres = " ".join([g.name for g in title.genres.all()])
        actors = " ".join([a.name for a in title.actors.all()])
        corpus.append(f"{genres} {actors}".strip())
    return corpus


def _content_based(user, limit=8):
    rated_titles = list(Title.objects.filter(rating__user=user).distinct())
    all_titles = list(Title.objects.all().prefetch_related("genres", "actors"))

    if not rated_titles or not all_titles:
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    matrix = vectorizer.fit_transform(_title_corpus(all_titles))

    index_map = {title.id: idx for idx, title in enumerate(all_titles)}
    rated_indices = [index_map.get(t.id) for t in rated_titles if t.id in index_map]
    if not rated_indices:
        return []

    user_vector = np.asarray(matrix[rated_indices].mean(axis=0))
    scores = cosine_similarity(user_vector, matrix).flatten()

    ranked = sorted(zip(all_titles, scores), key=lambda pair: pair[1], reverse=True)
    rated_set = {title.id for title in rated_titles}
    recommendations = [title for title, _ in ranked if title.id not in rated_set][:limit]
    return recommendations


def _collaborative(user, limit=8):
    ratings = Rating.objects.select_related("title", "user")
    if not ratings:
        return []

    users = list({r.user_id for r in ratings})
    titles = list({r.title_id for r in ratings})

    user_index = {uid: idx for idx, uid in enumerate(users)}
    title_index = {tid: idx for idx, tid in enumerate(titles)}

    matrix = np.zeros((len(users), len(titles)))
    for rating in ratings:
        matrix[user_index[rating.user_id], title_index[rating.title_id]] = float(rating.score)

    if user.id not in user_index:
        return []

    similarities = cosine_similarity([matrix[user_index[user.id]]], matrix).flatten()
    similar_users = np.argsort(similarities)[::-1][1:5]

    recommended = set()
    for idx in similar_users:
        user_ratings = matrix[idx]
        for t_idx, score in enumerate(user_ratings):
            if score >= 8 and matrix[user_index[user.id], t_idx] == 0:
                recommended.add(titles[t_idx])

    title_map = {title.id: title for title in Title.objects.filter(id__in=recommended)}
    return list(title_map.values())[:limit]


def get_recommendations_for_user(user, limit=8):
    cache_key = f"recs:user:{user.id}:{limit}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    content = _content_based(user, limit=limit)
    collab = _collaborative(user, limit=limit)
    combined = []
    seen = set()
    for title in content + collab:
        if title.id not in seen:
            combined.append(title)
            seen.add(title.id)

    results = combined[:limit]
    cache.set(cache_key, results, timeout=300)
    return results
