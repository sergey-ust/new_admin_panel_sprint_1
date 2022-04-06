from dataclasses import dataclass
from datetime import date, datetime
import uuid

MAX_UNIX_DATE = '2038-01-19'
UNIX_DATE_EMPTY_MARK = MAX_UNIX_DATE
QUOTE_SYMBOL = '\x16'
NULL_SYMBOL = 'NULL'
DELIMITER = ','


@dataclass()
class FilmWork:
    """PostreSQL 'filmwork' Table."""

    _TITLE_MAX_LEN = 200
    _TYPE_MAX_LEN = 15

    id: uuid.UUID
    title: str
    description: str
    creation_date: date
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime

    def __init__(
            self, id_: str, title: str, description: str,
            creation_date: str, rating: str, type_: str,
            created_at: str, updated_at: str
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
        #  FixMe timestamp in table will contain convertation to my time(+3h)
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
            title=QUOTE_SYMBOL + self.title + QUOTE_SYMBOL,
            description=QUOTE_SYMBOL + self.description + QUOTE_SYMBOL,
            creation_date=self.creation_date.isoformat(),
            rating=self.rating if self.rating else NULL_SYMBOL,
            type_=QUOTE_SYMBOL + self.type + QUOTE_SYMBOL,
        )


@dataclass()
class Genre:
    """PostreSQL 'genre' Table."""

    _NAME_MAX_LEN = 100
    _TYPE_MAX_LEN = 15

    id: uuid.UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    def __init__(
            self, id_: str, name: str, description: str,
            created_at: str, updated_at: str
    ):
        self.id = uuid.UUID(id_)
        self.name = name[: self._NAME_MAX_LEN]
        self.description = description if description else ''

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
            name=QUOTE_SYMBOL + self.name + QUOTE_SYMBOL,
            description=QUOTE_SYMBOL + self.description + QUOTE_SYMBOL,
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

    def __init__(self, id_: str, full_name: str, created_at: str,
                 updated_at: str):
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
            name=QUOTE_SYMBOL + self.full_name + QUOTE_SYMBOL,
        )


@dataclass()
class PersonFilmWork:
    """PostreSQL 'person_filmwork' Table."""

    id: uuid.UUID
    role: str
    created: datetime
    film_work_id: uuid.UUID
    person_id: uuid.UUID

    def __init__(self, id_: str, role: str, created_at: str, film_work_id: str,
                 person_id: str):
        self.id = uuid.UUID(id_)
        self.film_work_id = uuid.UUID(film_work_id)
        self.person_id = uuid.UUID(person_id)
        self.role = role if role else NULL_SYMBOL

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
            role=QUOTE_SYMBOL + self.role + QUOTE_SYMBOL,
        )


@dataclass()
class GenreFilmWork:
    """PostreSQL 'genre_filmwork' Table."""

    id: uuid.UUID
    created: datetime
    film_work_id: uuid.UUID
    genre_id: uuid.UUID

    def __init__(self, id_: str, created_at: str, film_work_id: str,
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
