import uuid
from django.db import models


class Genre(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('name', max_length=100)
    description = models.TextField('description', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = 'genre'
        verbose_name_plural = 'genres'


class FilmWork(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('name', max_length=200)
    description = models.TextField('description', blank=True)
    creation_date = models.DateField()
    rating = models.FloatField()
    type = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = 'film'
        verbose_name_plural = 'films'
