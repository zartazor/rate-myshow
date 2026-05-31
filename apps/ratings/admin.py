from django.contrib import admin

from .models import Rating, Watchlist, Watched


admin.site.register(Rating)
admin.site.register(Watchlist)
admin.site.register(Watched)
