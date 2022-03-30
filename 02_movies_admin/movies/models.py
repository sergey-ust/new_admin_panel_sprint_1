import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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

    class FilmType(models.TextChoices):
        MOVIE = 'movie'
        TV_SHOW = 'tv_show'

    title = models.CharField('name', max_length=200)
    description = models.TextField('description', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    creation_date = models.DateField('creation date')
    rating = models.FloatField(
        'rating',
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    type = models.CharField(
        "type",
        max_length=10,
        choices=FilmType.choices,
        default=FilmType.MOVIE,
    )

    # If DB Constraints are needed, they could be added in Meta
    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = 'film'
        verbose_name_plural = 'films'
