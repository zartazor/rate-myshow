from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .services.recommender import get_recommendations_for_user


@login_required
def recommended(request):
    titles = get_recommendations_for_user(request.user, limit=16)
    return render(request, "recommendations/list.html", {"titles": titles})
