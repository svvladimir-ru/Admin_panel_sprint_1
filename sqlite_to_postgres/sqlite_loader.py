import sqlite3
from schemas import *


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def load_film_work(self):
        movie = []
        for row in self.cur.execute('SELECT * FROM film_work'):
            movie.append(FilmWorkWithoutField(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                creation_date=row['creation_date'],
                certificate=row['certificate'],
                file_path=row['file_path'],
                rating=row['rating'],
                type=row['type'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            ))
        return movie

    def load_genre(self):
        genre = []
        for row in self.cur.execute('SELECT * FROM genre'):
            genre.append(GenreWithoutField(
                id=row['id'],
                name=row['name'],
                description=row['description'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            ))
        return genre

    def load_genre_film_fork(self):
        genre_film_fork = []
        for row in self.cur.execute('SELECT * FROM genre_film_work'):
            genre_film_fork.append(GenreFilmWorkWithoutField(
                id=row['id'],
                film_work_id=row['film_work_id'],
                genre_id=row['genre_id'],
                created_at=row['created_at']
            ))
        return genre_film_fork

    def load_person(self):
        person = []
        for row in self.cur.execute('SELECT * FROM person'):
            person.append(PersonWithoutField(
                id=row['id'],
                full_name=row['full_name'],
                birth_date=row['birth_date'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            ))
        return person

    def load_person_film_work(self):
        person_film_work = []
        for row in self.cur.execute('SELECT * FROM person_film_work'):
            person_film_work.append(PersonFilmWorkWithoutField(
                id=row['id'],
                film_work_id=row['film_work_id'],
                person_id=row['person_id'],
                role=row['role'],
                created_at=row['created_at']
            ))
        return person_film_work

    def load_movies(self):
        return {
            "film_work": self.load_film_work(),
            "genre": self.load_genre(),
            "genre_film_fork": self.load_genre_film_fork(),
            "person": self.load_person(),
            "person_film_work": self.load_person_film_work()
        }
