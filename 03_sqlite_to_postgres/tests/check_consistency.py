from dataclasses import dataclass
import os
import sqlite3
from typing import Callable

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor
import pytest

import load_data
import tables


@pytest.fixture(scope='module')
def activate_env():
    load_dotenv()


@pytest.fixture()
def psql_connect():
    dsl = {
        'dbname': os.environ.get('DB_NAME', 'movies_database'),
        'user': 'app',
        'password': '123qwe',
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': int(os.environ.get('DB_PORT', 5432)),
    }
    psycopg2.extras.register_uuid()
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn, \
            pg_conn.cursor() as pg_cursor:
        pg_cursor.execute('SET SESSION TIME ZONE "UTC";')
        yield pg_cursor


@pytest.fixture()
def sqlite_connect():
    try:
        db_path = os.environ.get('SQL_LITE_DB_PATH', '../db.sqlite')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        yield cursor
    finally:
        cursor.close()
        conn.close()


def get_size(sql_cursor, table_name: str) -> int:
    sql_cursor.execute(
        "SELECT COUNT(*) FROM {table};".format(table=table_name))
    return sql_cursor.fetchone()[0]


def test_sizes(psql_connect, sqlite_connect):
    sqlite_curs = sqlite_connect
    pg_curs = psql_connect

    tables_ = (
        ('content.film_work', 'film_work'),
        ('content.person', 'person'),
        ('content.genre', 'genre'),
        ('content.genre_film_work', 'genre_film_work'),
        ('content.person_film_work', 'person_film_work'),
    )
    for tbl in tables_:
        assert get_size(pg_curs, tbl[0]) == get_size(sqlite_curs, tbl[1])


@dataclass(frozen=True)
class Convertor:
    table_name: str
    create_class: Callable[[dict], load_data.AnyTable]


@dataclass(frozen=True)
class MainConvertor:
    postgresql: Convertor
    sqlite: Convertor


def _get_convertors() -> list[MainConvertor]:
    return [
        MainConvertor(
            sqlite=Convertor(
                table_name='film_work',
                create_class=lambda d: tables.FilmWork.create_from_sqlite(
                    tables.SqliteTables.FilmWork(**d)
                ),
            ),
            postgresql=Convertor(
                table_name='content.film_work',
                create_class=lambda d: tables.FilmWork(**d),
            ),
        ),
        MainConvertor(
            sqlite=Convertor(
                table_name='genre',
                create_class=lambda d: tables.Genre.create_from_sqlite(
                    tables.SqliteTables.Genre(**d)
                ),
            ),
            postgresql=Convertor(
                table_name='content.genre',
                create_class=lambda d: tables.Genre(**d),
            ),
        ),
        MainConvertor(
            sqlite=Convertor(
                table_name='person',
                create_class=lambda d: tables.Person.create_from_sqlite(
                    tables.SqliteTables.Person(**d)
                ),
            ),
            postgresql=Convertor(
                table_name='content.person',
                create_class=lambda d: tables.Person(**d),
            ),
        ),
        MainConvertor(
            sqlite=Convertor(
                table_name='genre_film_work',
                create_class=lambda d: tables.GenreFilmWork.create_from_sqlite(
                    tables.SqliteTables.GenreFilmWork(**d)
                ),
            ),
            postgresql=Convertor(
                table_name='content.genre_film_work',
                create_class=lambda d: tables.GenreFilmWork(**d),
            ),
        ),
        MainConvertor(
            sqlite=Convertor(
                table_name='person_film_work',
                create_class=lambda d:
                tables.PersonFilmWork.create_from_sqlite(
                    tables.SqliteTables.PersonFilmWork(**d)
                ),
            ),
            postgresql=Convertor(
                table_name='content.person_film_work',
                create_class=lambda d: tables.PersonFilmWork(**d),
            ),
        ),
    ]


_LINES_PER_TIME_EXTRACTION = 400


def test_equality(psql_connect, sqlite_connect):
    sqlite_curs = sqlite_connect
    pg_curs = psql_connect

    for conv in _get_convertors():
        offset = 0
        size = _LINES_PER_TIME_EXTRACTION
        while True:
            lite_data = load_data.extract_part(sqlite_curs,
                                               conv.sqlite.table_name,
                                               size,
                                               offset)
            post_data = load_data.extract_part(pg_curs,
                                               conv.postgresql.table_name,
                                               size,
                                               offset)
            cnt = len(lite_data)
            for i in range(cnt):
                assert conv.postgresql.create_class(
                    dict(post_data[i])
                ) == conv.sqlite.create_class(dict(lite_data[i]))

            offset += cnt
            if cnt < size:
                break
