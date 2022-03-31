import uuid
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_(_('genre_name')), max_length=100)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('name'), max_length=200)

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    class FilmType(models.TextChoices):
        MOVIE = 'MOVIE', _('movie')
        TV_SHOW = 'TV_SHOW', _('tv_show')

    title = models.CharField(_('film_name'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'))
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
    )
    type = models.CharField(
        _('type'),
        max_length=15,
        choices=FilmType.choices,
        default=FilmType.MOVIE,
    )
    genres = models.ManyToManyField(Genre, through='GenreFilmWork')
    person = models.ManyToManyField(Person, through='PersonFilmWork')

    # If DB Constraints are needed, they could be added in Meta
    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = _('film work')
        verbose_name_plural = _('film works')

    def __str__(self):
        return self.title + ' ({0})'.format(self.creation_date.year)


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'
        verbose_name = _('film genre')
        verbose_name_plural = _('film genres')

    def __str__(self):
        return ''


class PersonFilmWork(UUIDMixin):
    film_work = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"person_film_work'
        verbose_name = _('film person')
        verbose_name_plural = _('film persons')

    def __str__(self):
        return ''
