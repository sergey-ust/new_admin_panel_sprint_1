from dataclasses import dataclass
from datetime import date, datetime, timezone
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


def str_to_datetime(line: str) -> datetime:
    if line:
        return datetime.strptime(line + ':00',
                                 '%Y-%m-%d %H:%M:%S.%f%z')
    return datetime.datetime.utcnow()


class SqliteTables:
    """ Attention.
        Tables should have 'date' and 'datetime' types, but our db contains
         wrong formatted datetime fields.
         e.g.: 'filmwork' 6th row field 'updated_at'
    """

    @dataclass(frozen=True)
    class FilmWork:
        id: str
        title: str
        description: Str_None
        creation_date: Str_None
        file_path: Str_None
        rating: Str_None
        type: str
        created_at: Str_None
        updated_at: Str_None

    @dataclass(frozen=True)
    class Genre:
        id: str
        name: str
        description: Str_None
        created_at: Str_None
        updated_at: Str_None

    @dataclass(frozen=True)
    class Person:
        id: str
        full_name: str
        created_at: Str_None
        updated_at: Str_None

    @dataclass(frozen=True)
    class GenreFilmWork:
        id: str
        created_at: Str_None
        film_work_id: str
        genre_id: str

    @dataclass(frozen=True)
    class PersonFilmWork:
        id: str
        role: str
        created_at: Str_None
        film_work_id: str
        person_id: str


@dataclass(frozen=True)
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
    created: datetime
    modified: datetime

    @staticmethod
    def create_from_sqlite(lite_table: SqliteTables.FilmWork):
        descr = lite_table.description if lite_table.description else ''
        creation = date.fromisoformat(
            lite_table.creation_date if lite_table.creation_date
            else UNIX_DATE_EMPTY_MARK
        )
        try:
            _rating = float(lite_table.rating)
        except Exception:
            _rating = None

        created_at = str_to_datetime(lite_table.created_at).replace(
            tzinfo=timezone.utc)
        updated_at = str_to_datetime(lite_table.updated_at).replace(
            tzinfo=timezone.utc)

        return FilmWork(
            id=uuid.UUID(lite_table.id),
            title=lite_table.title[: FilmWork._TITLE_MAX_LEN],
            description=descr,
            creation_date=creation,
            rating=lite_table.rating,
            type=lite_table.type[:FilmWork._TYPE_MAX_LEN],
            created=created_at,
            modified=updated_at
        )

    # FixMe: Replace all QUOTE_SYMBOL symbols
    def __str__(self) -> str:
        return '{created},{modified},{id_},{title},'.format(
            created=self.created.isoformat(),
            modified=self.modified.isoformat(),
            id_=self.id,
            title=quotes(self.title)
        ) + '{description},{creation_date},{rating},{type_}\n'.format(
            description=quotes(self.description),
            creation_date=self.creation_date.isoformat(),
            rating=self.rating if self.rating else NULL_SYMBOL,
            type_=quotes(self.type),
        )


@dataclass(frozen=True)
class Genre:
    """PostreSQL 'genre' Table."""

    _NAME_MAX_LEN = 100
    _TYPE_MAX_LEN = 15

    id: uuid.UUID
    name: str
    description: Str_None
    created: datetime
    modified: datetime

    @staticmethod
    def create_from_sqlite(lite_table: SqliteTables.Genre):
        created_at = str_to_datetime(lite_table.created_at).replace(
            tzinfo=timezone.utc)
        updated_at = str_to_datetime(lite_table.updated_at).replace(
            tzinfo=timezone.utc)

        return Genre(
            id=uuid.UUID(lite_table.id),
            name=lite_table.name[: Genre._NAME_MAX_LEN],
            description=lite_table.description,
            created=created_at,
            modified=updated_at
        )

    # FixMe: Replace all QUOTE_SYMBOL symbols
    def __str__(self) -> str:
        return '{created},{modified},{id_},{name},{description}\n'.format(
            created=self.created.isoformat(),
            modified=self.modified.isoformat(),
            id_=self.id,
            name=quotes(self.name),
            description=quotes(self.description) if self.description
            else NULL_SYMBOL,
        )



@dataclass(frozen=True)
class Person:
    """PostreSQL 'person' Table."""

    _NAME_MAX_LEN = 200
    _TYPE_MAX_LEN = 15

    id: uuid.UUID
    full_name: str
    created: datetime
    modified: datetime

    @staticmethod
    def create_from_sqlite(lite_table: SqliteTables.Person):
        created_at = str_to_datetime(lite_table.created_at).replace(
            tzinfo=timezone.utc)
        updated_at = str_to_datetime(lite_table.updated_at).replace(
            tzinfo=timezone.utc)

        return Person(
            id=uuid.UUID(lite_table.id),
            full_name=lite_table.full_name[: Person._NAME_MAX_LEN],
            created=created_at,
            modified=updated_at
        )

    # FixMe: Replace all QUOTE_SYMBOL symbols
    def __str__(self) -> str:
        return '{created},{modified},{id_},{name}\n'.format(
            created=self.created.isoformat(),
            modified=self.modified.isoformat(),
            id_=self.id,
            name=quotes(self.full_name),
        )


@dataclass(frozen=True)
class PersonFilmWork:
    """PostreSQL 'person_filmwork' Table."""

    id: uuid.UUID
    role: Str_None
    created: datetime
    film_work_id: uuid.UUID
    person_id: uuid.UUID

    @staticmethod
    def create_from_sqlite(lite_table: SqliteTables.PersonFilmWork):
        created_at = str_to_datetime(lite_table.created_at).replace(
            tzinfo=timezone.utc)

        return PersonFilmWork(
            id=uuid.UUID(lite_table.id),
            role=lite_table.role,
            created=created_at,
            film_work_id=uuid.UUID(lite_table.film_work_id),
            person_id=uuid.UUID(lite_table.person_id)
        )

    # FixMe: Replace all QUOTE_SYMBOL symbols
    def __str__(self) -> str:
        return '{id_},{role},{created},{film_id},{person_id}\n'.format(
            created=self.created.isoformat(),
            id_=self.id,
            film_id=self.film_work_id,
            person_id=self.person_id,
            role=quotes(self.role),
        )


@dataclass(frozen=True)
class GenreFilmWork:
    """PostreSQL 'genre_filmwork' Table."""

    id: uuid.UUID
    created: datetime
    film_work_id: uuid.UUID
    genre_id: uuid.UUID

    @staticmethod
    def create_from_sqlite(lite_table: SqliteTables.GenreFilmWork):
        created_at = str_to_datetime(lite_table.created_at).replace(
            tzinfo=timezone.utc)

        return GenreFilmWork(
            id=uuid.UUID(lite_table.id),
            created=created_at,
            film_work_id=uuid.UUID(lite_table.film_work_id),
            genre_id=uuid.UUID(lite_table.genre_id)
        )

    # FixMe: Replace all QUOTE_SYMBOL symbols
    def __str__(self) -> str:
        return '{id_},{created},{film_id},{genre_id}\n'.format(
            created=self.created.isoformat(),
            id_=self.id,
            film_id=self.film_work_id,
            genre_id=self.genre_id,
        )
