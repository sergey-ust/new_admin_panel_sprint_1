from dataclasses import dataclass
from datetime import date, datetime
import uuid
from typing import Union

MAX_UNIX_DATE = '2038-01-19'
UNIX_DATE_EMPTY_MARK = MAX_UNIX_DATE
QUOTE_SYMBOL = '\x16'
NULL_SYMBOL = 'NULL'
DELIMITER = ','

Str_None = Union[str, None]


def quotes(line: str) -> str:
    return QUOTE_SYMBOL + line + QUOTE_SYMBOL


@dataclass()
class FilmWork:
    """PostreSQL 'filmwork' Table."""

    _TITLE_MAX_LEN = 200
    _TYPE_MAX_LEN = 15

    id: uuid.UUID
    title: str
    description: str
    creation_date: date
    rating: Union[float, None]
    type: str
    created_at: datetime
    updated_at: datetime

    def __init__(
            self, id_: str, title: str, description: Str_None,
            creation_date: Str_None, rating: str, type_: str,
            created_at: Str_None, updated_at: Str_None
    ):
        self.id = uuid.UUID(id_)
        self.title = title[: self._TITLE_MAX_LEN]
        self.description = description if description else ''
        self.creation_date = date.fromisoformat(
            creation_date if creation_date else UNIX_DATE_EMPTY_MARK)
        try:
            self.rating = float(rating)
        except Exception:
            self.rating = None
        self.type = type_[:self._TYPE_MAX_LEN]
        if created_at:
            self.created_at = datetime.strptime(created_at + ':00',
                                                '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            self.created_at = datetime.datetime.utcnow()
        if updated_at:
            self.updated_at = datetime.strptime(updated_at + ':00',
                                                '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            self.updated_at = datetime.datetime.utcnow()

    # FixMe: Replace all QUOTE_SYMBOL symbols
    def __str__(self) -> str:
        return '{created},{modified},{id_},{title},\
        {description},{creation_date},{rating},{type_}\n'.format(
            created=self.created_at.isoformat(),
            modified=self.updated_at.isoformat(),
            id_=self.id,
            title=quotes(self.title),
            description=quotes(self.description),
            creation_date=self.creation_date.isoformat(),
            rating=self.rating if self.rating else NULL_SYMBOL,
            type_=quotes(self.type),
        )


@dataclass()
class Genre:
    """PostreSQL 'genre' Table."""

    _NAME_MAX_LEN = 100
    _TYPE_MAX_LEN = 15

    id: uuid.UUID
    name: str
    description: Str_None
    created_at: datetime
    updated_at: datetime

    def __init__(
            self, id_: str, name: str, description: Str_None,
            created_at: Str_None, updated_at: Str_None
    ):
        self.id = uuid.UUID(id_)
        self.name = name[: self._NAME_MAX_LEN]
        self.description = description

        if created_at:
            self.created_at = datetime.strptime(created_at + ':00',
                                                '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            self.created_at = datetime.datetime.utcnow()
        if updated_at:
            self.updated_at = datetime.strptime(updated_at + ':00',
                                                '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            self.updated_at = datetime.datetime.utcnow()

    # FixMe: Replace all QUOTE_SYMBOL symbols
    def __str__(self) -> str:
        return '{created},{modified},{id_},{name},{description}\n'.format(
            created=self.created_at.isoformat(),
            modified=self.updated_at.isoformat(),
            id_=self.id,
            name=quotes(self.name),
            description=quotes(self.description) if self.description
            else NULL_SYMBOL,
        )


@dataclass()
class Person:
    """PostreSQL 'person' Table."""

    _NAME_MAX_LEN = 200
    _TYPE_MAX_LEN = 15

    id: uuid.UUID
    full_name: str
    created_at: datetime
    updated_at: datetime

    def __init__(self, id_: str, full_name: str, created_at: Str_None,
                 updated_at: Str_None):
        self.id = uuid.UUID(id_)
        self.full_name = full_name[: self._NAME_MAX_LEN]

        if created_at:
            self.created_at = datetime.strptime(created_at + ':00',
                                                '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            self.created_at = datetime.datetime.utcnow()
        if updated_at:
            self.updated_at = datetime.strptime(updated_at + ':00',
                                                '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            self.updated_at = datetime.datetime.utcnow()

    # FixMe: Replace all QUOTE_SYMBOL symbols
    def __str__(self) -> str:
        return '{created},{modified},{id_},{name}\n'.format(
            created=self.created_at.isoformat(),
            modified=self.updated_at.isoformat(),
            id_=self.id,
            name=quotes(self.full_name),
        )


@dataclass()
class PersonFilmWork:
    """PostreSQL 'person_filmwork' Table."""

    id: uuid.UUID
    role: Str_None
    created: datetime
    film_work_id: uuid.UUID
    person_id: uuid.UUID

    def __init__(self, id_: str, role: str, created_at: Str_None,
                 film_work_id: str, person_id: str):
        self.id = uuid.UUID(id_)
        self.film_work_id = uuid.UUID(film_work_id)
        self.person_id = uuid.UUID(person_id)
        self.role = role

        if created_at:
            self.created = datetime.strptime(created_at + ':00',
                                             '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            self.created = datetime.datetime.utcnow()

    # FixMe: Replace all QUOTE_SYMBOL symbols
    def __str__(self) -> str:
        return '{id_},{role},{created},{film_id},{person_id}\n'.format(
            created=self.created.isoformat(),
            id_=self.id,
            film_id=self.film_work_id,
            person_id=self.person_id,
            role=quotes(self.role),
        )


@dataclass()
class GenreFilmWork:
    """PostreSQL 'genre_filmwork' Table."""

    id: uuid.UUID
    created: datetime
    film_work_id: uuid.UUID
    genre_id: uuid.UUID

    def __init__(self, id_: str, created_at: Str_None, film_work_id: str,
                 genre_id: str):
        self.id = uuid.UUID(id_)
        self.film_work_id = uuid.UUID(film_work_id)
        self.genre_id = uuid.UUID(genre_id)

        if created_at:
            self.created = datetime.strptime(created_at + ':00',
                                             '%Y-%m-%d %H:%M:%S.%f%z')
        else:
            self.created = datetime.datetime.utcnow()

    # FixMe: Replace all QUOTE_SYMBOL symbols
    def __str__(self) -> str:
        return '{id_},{created},{film_id},{genre_id}\n'.format(
            created=self.created.isoformat(),
            id_=self.id,
            film_id=self.film_work_id,
            genre_id=self.genre_id,
        )
