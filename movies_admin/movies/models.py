from django.db import models


class FilmWork(models.Model):
    """Признаюсь построил через python manage.py inspectdb > models.py
    Добавил поля в genres, persons для выполнения задачи, Добавил к полям created_created_at,
    updated_at поля auto_now_add и auto_now
    """
    id = models.UUIDField(primary_key=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateField(blank=True, null=True)
    certificate = models.TextField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    type = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    genres = models.ManyToManyField('Genre', through='GenreFilmWork')
    persons = models.ManyToManyField('Person', through='PersonFilmWork')

    class Meta:
        managed = False
        db_table = 'film_work'


class Genre(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'genre'


class GenreFilmWork(models.Model):
    id = models.UUIDField(primary_key=True)
    film_work = models.ForeignKey(FilmWork, models.DO_NOTHING)
    genre = models.ForeignKey(Genre, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'genre_film_work'
        unique_together = (('film_work', 'genre'),)


class Person(models.Model):
    id = models.UUIDField(primary_key=True)
    full_name = models.TextField()
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'person'


class PersonFilmWork(models.Model):
    id = models.UUIDField(primary_key=True)
    film_work = models.ForeignKey(FilmWork, models.DO_NOTHING)
    person = models.ForeignKey(Person, models.DO_NOTHING)
    role = models.TextField()  # This field type is a guess.
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'person_film_work'
        unique_together = (('film_work', 'person', 'role'),)
