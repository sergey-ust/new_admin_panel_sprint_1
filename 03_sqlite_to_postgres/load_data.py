import io
from contextlib import contextmanager
import os
import sqlite3

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor

import tables


def load_from_sqlite(sqlite_curs: sqlite3.Cursor, pg_cursor):
    f_works = extract(sqlite_curs, "film_work", create_film_work)
    try:
        post(pg_cursor, f_works, "content.film_work")
    except Exception as exp:
        print(f"Can't insert Film work data: {exp}.")

    genres = extract(sqlite_curs, "genre", create_genre)
    try:
        post(pg_cursor, genres, "content.genre")
    except Exception as exp:
        print(f"Can't insert Genre data: {exp}.")

    persons = extract(sqlite_curs, "person", create_person)
    try:
        post(pg_cursor, persons, "content.person")
    except Exception as exp:
        print(f"Can't insert Person data: {exp}.")

    gf_works = extract(sqlite_curs, "genre_film_work", create_genre_film_work)
    try:
        post(pg_cursor, gf_works, "content.genre_film_work")
    except Exception as exp:
        print(f"Can't insert GenreFilmWork data: {exp}.")

    pf_works = extract(sqlite_curs, "person_film_work",
                       create_person_film_work)
    try:
        post(pg_cursor, pf_works, "content.person_film_work")
    except Exception as exp:
        print(f"Can't insert PersonFilmWork data: {exp}.")


def extract(cursor: sqlite3.Cursor,
            sqlite_table: str,
            convertor) -> io.StringIO:
    cursor.execute('SELECT * FROM {table};'.format(table=sqlite_table))
    out = io.StringIO()
    for entry in cursor.fetchall():
        try:
            fw_line = convertor(dict(entry))
        except Exception as e:
            print(f'Can\'t convert entry({entry}): {e}')
        else:
            out.write(fw_line)
    return out


def post(pg_cursor, csv: io.StringIO, postgres_name: str):
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
        load_from_sqlite(sqlite.cursor(), pg_cursor)


if __name__ == '__main__':
    main()
