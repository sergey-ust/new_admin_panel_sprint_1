import os
import sqlite3

from dotenv import load_dotenv
import pytest
import psycopg2
from psycopg2.extras import DictCursor


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

    tables = (
        ("content.film_work", "film_work"),
        ("content.person", "person"),
        ("content.genre", "genre"),
        ('content.genre_film_work', 'genre_film_work'),
        ('content.person_film_work', 'person_film_work'),
    )
    for tbl in tables:
        assert get_size(pg_curs, tbl[0]) == get_size(sqlite_curs, tbl[1])
