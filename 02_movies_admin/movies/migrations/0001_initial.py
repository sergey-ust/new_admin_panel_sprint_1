# Generated by Django 4.0.3 on 2022-04-08 21:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilmWork',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, verbose_name='film_name')),
                ('description', models.TextField(verbose_name='description')),
                ('creation_date', models.DateField(verbose_name='creation date')),
                ('rating', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100.0)], verbose_name='rating')),
                ('type', models.CharField(choices=[('MOVIE', 'movie'), ('TV_SHOW', 'tv_show')], default='MOVIE', max_length=15, verbose_name='type')),
            ],
            options={
                'verbose_name': 'film work',
                'verbose_name_plural': 'film works',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='genre_name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=200, verbose_name='name')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('ACTOR', 'actor'), ('DIRECTOR', 'director'), ('WRITER', 'writer')], max_length=15, null=True, verbose_name='role')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('film_work', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='film work')),
                ('person', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='movies.person', verbose_name='person')),
            ],
            options={
                'verbose_name': 'film person',
                'verbose_name_plural': 'film persons',
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.CreateModel(
            name='GenreFilmWork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('film_work', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='movies.filmwork', verbose_name='film work')),
                ('genre', models.ForeignKey(db_index=False, on_delete=django.db.models.deletion.CASCADE, to='movies.genre', verbose_name='genre')),
            ],
            options={
                'verbose_name': 'film genre',
                'verbose_name_plural': 'film genres',
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(through='movies.GenreFilmWork', to='movies.genre'),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='person',
            field=models.ManyToManyField(through='movies.PersonFilmWork', to='movies.person'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work'], name='person_film_work_film_work_id'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['person'], name='person_film_work_person_id'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['film_work'], name='genre_film_work_film_work_id'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['genre'], name='genre_film_work_genre_id'),
        ),
        migrations.AddConstraint(
            model_name='genrefilmwork',
            constraint=models.UniqueConstraint(fields=('film_work', 'genre'), name='unique_film_genre'),
        ),
    ]
