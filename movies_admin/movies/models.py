import uuid

from django.db import models
from django.utils.translation import gettext as _


class TimeStampedMixin:
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PersonRole(models.TextChoices):
    DIRECTOR = 'director', _('директор')
    WRITER = 'writer', _('сценарист')
    ACTOR = 'actor', _('актер')


class FilmWork(TimeStampedMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.TextField()
    description = models.TextField(null=True)
    creation_date = models.DateField(null=True)
    file_path = models.FilePathField(null=True)  # либо FileField
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True)
    type = models.CharField(max_length=30)

    class Meta:
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')
        db_table = "film_work"
        managed = False


class Genre(TimeStampedMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    description = models.TextField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('genre')
        verbose_name_plural = _('genres')
        db_table = "genre"
        managed = False


class GenreFilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    film_work_id = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    genre_id = models.ForeignKey('Genre', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "film_work_genre"
        managed = False


class Person(TimeStampedMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    full_name = models.CharField(max_length=30)
    birth_date = models.TextField(null=True)

    class Meta:
        db_table = "person"
        managed = False


class PersonFilmWork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    film_work_id = models.ForeignKey('FilmWork', on_delete=models.CASCADE)
    person_id = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('роль'), max_length=20, choices=PersonRole.choices)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "person_film_work"
        managed = False
