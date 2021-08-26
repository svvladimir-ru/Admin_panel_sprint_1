import uuid
from datetime import datetime
from dataclasses import dataclass, field


@dataclass(frozen=True)
class FilmWorkWithoutField:
    title: str
    description: str
    creation_date: datetime
    certificate: str
    file_path: str
    type: str
    created_at: datetime
    updated_at: datetime
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class GenreWithoutField:
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class GenreFilmWorkWithoutField:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class PersonWithoutField:
    full_name: str is not None
    birth_date: datetime
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class PersonFilmWorkWithoutField:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: list
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class MovieWithoutField:
    __slots__ = ('title', 'description')
    title: str
    description: str


movie = MovieWithoutField(title='AAA', description='BBB')

print(i for i in movie.__annotations__)
