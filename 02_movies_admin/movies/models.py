"""ORM models for film work application."""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

_PERSON_NAME_MAX_LEN = 200
_FILM_NAME_MAX_LEN = 200
_FILM_TYPE_NAME_MAX_LEN = 15


class TimeStampedMixin(models.Model):
    """Base class for models with created/modified timestamps."""

    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        """ORM meta data."""

        abstract = True


class UUIDMixin(models.Model):
    """Base class for models with Django generated UUID(Primary key)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        """ORM meta data."""

        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """ORM model for "genre" table."""

    name = models.CharField(_(_('genre_name')), max_length=100, unique=True)
    description = models.TextField(_('description'), null=True, blank=True)

    class Meta:
        """ORM meta data."""

        db_table = 'content"."genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self) -> str:
        """Genre name."""
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    """ORM model for "person' table."""

    full_name = models.CharField(_('name'), max_length=_PERSON_NAME_MAX_LEN)

    class Meta:
        """ORM meta data."""

        db_table = 'content\".\"person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self) -> str:
        """Person full name."""
        return self.full_name


class _FilmType(models.TextChoices):
    MOVIE = 'MOVIE', _('movie')
    TV_SHOW = 'TV_SHOW', _('tv_show')


class FilmWork(UUIDMixin, TimeStampedMixin):
    """ORM model for "film_work" table."""

    title = models.CharField(_('film_name'), max_length=_FILM_NAME_MAX_LEN)
    description = models.TextField(_('description'))
    creation_date = models.DateField(_('creation date'))
    rating = models.FloatField(
        _('rating'),
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100.0)],
    )
    type = models.CharField(
        _('type'),
        max_length=_FILM_TYPE_NAME_MAX_LEN,
        choices=_FilmType.choices,
        default=_FilmType.MOVIE,
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    person = models.ManyToManyField(Person, through='PersonFilmWork')

    # If DB Constraints are needed, they could be added in Meta
    class Meta:
        """ORM meta data."""

        db_table = 'content"."film_work'
        verbose_name = _('film work')
        verbose_name_plural = _('film works')

    def __str__(self) -> str:
        """Convert to name + creation date."""
        return self.title + ' ({0})'.format(self.creation_date.year)


class GenreFilmWork(UUIDMixin):
    """Stuff object to connect "FilmWork" with "Genre"."""

    film_work = models.ForeignKey(
        'FilmWork', on_delete=models.CASCADE, verbose_name=_('film work'),
    )
    genre = models.ForeignKey(
        'Genre', on_delete=models.CASCADE, verbose_name=_('genre'),
    )
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        """ORM meta data."""

        db_table = 'content"."genre_film_work'
        unique_together = ('film_work', 'genre')
        verbose_name = _('film genre')
        verbose_name_plural = _('film genres')

    def __str__(self) -> str:
        """No printable information."""
        return ''


class PersonFilmWork(UUIDMixin):
    """Stuff object to connect "FilmWork" with "Person"."""

    film_work = models.ForeignKey(
        'FilmWork', on_delete=models.CASCADE, verbose_name=_('film work'),
    )
    person = models.ForeignKey(
        'Person', on_delete=models.CASCADE, verbose_name=_('person'),
    )
    role = models.TextField(_('role'), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """ORM meta data."""

        db_table = 'content"."person_film_work'
        verbose_name = _('film person')
        verbose_name_plural = _('film persons')

    def __str__(self) -> str:
        """No printable information."""
        return ''
