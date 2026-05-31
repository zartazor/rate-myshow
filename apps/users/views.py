from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.ratings.models import Rating, Watched
from .forms import ProfileForm


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user)

    ratings_count = Rating.objects.filter(user=request.user).count()
    watched_count = Watched.objects.filter(user=request.user).count()

    return render(
        request,
        "users/profile.html",
        {
            "form": form,
            "ratings_count": ratings_count,
            "watched_count": watched_count,
        },
    )
