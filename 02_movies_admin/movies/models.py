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
