from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    OMDB_TYPES = (
        ("movie", "Movie"),
        ("series", "Series"),
    )

    omdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=20, blank=True)
    type = models.CharField(max_length=20, choices=OMDB_TYPES)
    poster = models.URLField(blank=True)
    data = models.JSONField(default=dict)
    cached_at = models.DateTimeField(auto_now=True)

    genres = models.ManyToManyField(Genre, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)

    def __str__(self):
        return f"{self.title} ({self.year})"
