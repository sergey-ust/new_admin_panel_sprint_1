import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class TimeStampedMixin(models.Model):
    created = models.DateTimeField('created', auto_now_add=True)
    modified = models.DateTimeField('modified', auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField('name', max_length=100)
    description = models.TextField('description', blank=True)

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = 'genre'
        verbose_name_plural = 'genres'



class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmType(models.TextChoices):
        MOVIE = 'movie'
        TV_SHOW = 'tv_show'

    title = models.CharField('name', max_length=200)
    description = models.TextField('description', blank=True)
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
