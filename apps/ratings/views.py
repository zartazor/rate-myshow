from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.titles.models import Title
from .forms import RatingForm
from .models import Rating, Watchlist, Watched


@login_required
def rate_title(request, imdb_id):
    title = get_object_or_404(Title, omdb_id=imdb_id)
    rating = Rating.objects.filter(user=request.user, title=title).first()

    if request.method == "POST":
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.title = title
            rating.save()
            Watched.objects.get_or_create(user=request.user, title=title)
            return redirect("title_detail", imdb_id=imdb_id)
    else:
        form = RatingForm(instance=rating)

    return render(request, "ratings/rate.html", {"form": form, "title": title})


@login_required
def toggle_watchlist(request, imdb_id):
    title = get_object_or_404(Title, omdb_id=imdb_id)
    entry = Watchlist.objects.filter(user=request.user, title=title).first()
    if entry:
        entry.delete()
    else:
        Watchlist.objects.create(user=request.user, title=title)
    return redirect("title_detail", imdb_id=imdb_id)


@login_required
def watchlist(request):
    items = Watchlist.objects.filter(user=request.user).select_related("title")
    return render(request, "ratings/watchlist.html", {"items": items})


@login_required
def history(request):
    items = Watched.objects.filter(user=request.user).select_related("title")
    return render(request, "ratings/history.html", {"items": items})
