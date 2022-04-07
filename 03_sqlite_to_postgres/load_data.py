import io
from contextlib import contextmanager
import os
import sqlite3
from dataclasses import dataclass
from typing import Callable, Union

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor

import tables

AnyTable = Union[
    tables.FilmWork,
    tables.Genre,
    tables.Person,
    tables.PersonFilmWork,
    tables.GenreFilmWork
]


@dataclass(frozen=True)
class Convertor:
    sqlite_table: str
    psql_table: str
    convert: Callable[
        [dict[str, str]], AnyTable]


def load_from_sqlite(sqlite_curs: sqlite3.Cursor, pg_cursor):
    convertors = (
        Convertor(
            sqlite_table='film_work',
            psql_table='content.film_work',
            convert=create_film_work
        ),
        Convertor(
            sqlite_table='genre',
            psql_table='content.genre',
            convert=create_genre
        ),
        Convertor(
            sqlite_table='person',
            psql_table='content.person',
            convert=create_person
        ),
        Convertor(
            sqlite_table='genre_film_work',
            psql_table='content.genre_film_work',
            convert=create_genre_film_work
        ),
        Convertor(
            sqlite_table='person_film_work',
            psql_table='content.person_film_work',
            convert=create_person_film_work
        ),
    )
    result = True
    for conv in convertors:
        buff = io.StringIO()
        buff = extract(sqlite_curs, conv.sqlite_table, conv.convert, buff)
        try:
            post(pg_cursor, buff, conv.psql_table)
        except Exception as exp:
            print(f"Insertion into {conv.psql_table} error: {exp}.")
            result = False
            break
    return result


def clear_psql(cursor, psql_tables: tuple[str]) -> bool:
    is_ok = True
    for tbl in psql_tables:
        try:
            cursor.execute(
                "TRUNCATE TABLE {table} CASCADE;".format(table=tbl))
        except Exception as ex:
            print(f"Can't truncate PostgreSql Table: {tbl} error: {ex}.")
            is_ok = False
    return is_ok


def extract(cursor: sqlite3.Cursor,
            sqlite_table: str,
            convertor, out_stream: io.TextIOBase) -> io.TextIOBase:
    cursor.execute('SELECT * FROM {table};'.format(table=sqlite_table))
    for entry in cursor.fetchall():
        try:
            fw_line = convertor(dict(entry))
        except Exception as e:
            print(f'Can\'t convert entry({entry}): {e}')
        else:
            out_stream.write(fw_line)
    return out_stream


def post(pg_cursor, csv: io.TextIOBase, postgres_name: str):
    pg_cursor.execute(
        "TRUNCATE TABLE {table} CASCADE;".format(table=postgres_name))
    csv.seek(0)
    pg_cursor.copy_expert(
        "COPY {table} FROM STDIN \
        WITH CSV DELIMITER '{delim}' NULL '{null}' QUOTE '{quote}';".format(
            table=postgres_name,
            delim=tables.DELIMITER,
            null=tables.NULL_SYMBOL,
            quote=tables.QUOTE_SYMBOL),
        csv)


def create_film_work(data: dict) -> str:
    data["id_"] = data.pop("id")
    data["type_"] = data.pop("type")
    data.pop("file_path")
    return str(tables.FilmWork(**data))


def create_genre(data: dict) -> str:
    data["id_"] = data.pop("id")
    return str(tables.Genre(**data))


def create_person(data: dict) -> str:
    data["id_"] = data.pop("id")
    return str(tables.Person(**data))


def create_person_film_work(data: dict) -> str:
    data["id_"] = data.pop("id")
    return str(tables.PersonFilmWork(**data))


def create_genre_film_work(data: dict) -> str:
    data["id_"] = data.pop("id")
    return str(tables.GenreFilmWork(**data))


@contextmanager
def sqlite_conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def main():
    load_dotenv()
    dsl = {
        'dbname': os.environ.get('DB_NAME', 'movies_database'),
        'user': 'app',
        'password': '123qwe',
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': int(os.environ.get('DB_PORT', 5432)),
    }
    db_path = os.environ.get('SQL_LITE_DB_PATH', 'db.sqlite')

    with sqlite_conn_context(db_path) as sqlite, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn, \
            pg_conn.cursor() as pg_cursor:
        pg_cursor.execute('SET SESSION TIME ZONE "UTC";')
        if not load_from_sqlite(sqlite.cursor(), pg_cursor):
            pg_conn.rollback()
            print("There were some problems by tables " +
                  "truncating, please check the result in your DB viewer")


if __name__ == '__main__':
    main()
