from django.contrib import admin

from .models import Actor, Genre, Title


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("title", "year", "type")
    search_fields = ("title", "omdb_id")
    list_filter = ("type",)


admin.site.register(Genre)
admin.site.register(Actor)
