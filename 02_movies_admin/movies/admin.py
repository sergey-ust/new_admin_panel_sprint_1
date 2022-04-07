"""Admin panel models."""

from django.contrib import admin

from movies import models as mov_model


@admin.register(mov_model.Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin model for ORM model "Genre"."""


@admin.register(mov_model.Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin model for ORM model "Person"."""
    ordering = ['full_name']
    search_fields = ['full_name']


class _GenreFilmWorkInline(admin.TabularInline):
    model = mov_model.GenreFilmWork


class _PersonFilmWorkInline(admin.TabularInline):
    model = mov_model.PersonFilmWork
    autocomplete_fields = ['person']


@admin.register(mov_model.FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    """Admin model for ORM model "FilmWork"."""

    inlines = (_GenreFilmWorkInline, _PersonFilmWorkInline)
    list_display = ('title', 'type', 'creation_date', 'rating')
    list_filter = ('type',)
    search_fields = ('title', 'description')
