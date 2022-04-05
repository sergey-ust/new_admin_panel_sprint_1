import io
from contextlib import contextmanager
import os
import sqlite3

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from tables import FilmWork, Genre, Person, PersonFilmWork, \
    GenreFilmWork


def load_from_sqlite(sqlite_curs: sqlite3.Cursor, pg_cursor):
    f_works = extract_film_work(sqlite_curs)
    try:
        post_film_work(pg_cursor, f_works)
    except Exception as exp:
        print(f"Can't insert Film work data: {exp}.")

    genres = extract_genre(sqlite_curs)
    try:
        post_genre(pg_cursor, genres)
    except Exception as exp:
        print(f"Can't insert Genre data: {exp}.")

    persons = extract_person(sqlite_curs)
    try:
        post_person(pg_cursor, persons)
    except Exception as exp:
        print(f"Can't insert Person data: {exp}.")

    gf_works = extract_genre_film_work(sqlite_curs)
    try:
        post_genre_film_work(pg_cursor, gf_works)
    except Exception as exp:
        print(f"Can't insert GenreFilmWork data: {exp}.")

    pf_works = extract_person_film_work(sqlite_curs)
    try:
        post_person_film_work(pg_cursor, pf_works)
    except Exception as exp:
        print(f"Can't insert PersonFilmWork data: {exp}.")


@contextmanager
def sqlite_conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def extract_film_work(cursor: sqlite3.Cursor) -> io.StringIO:
    cursor.execute('SELECT * FROM film_work;')
    out = io.StringIO()

    for entry in cursor.fetchall():
        out_data = dict(entry)
        out_data["id_"] = out_data.pop("id")
        out_data["type_"] = out_data.pop("type")
        out_data.pop("file_path")
        try:
            fw_line = str(FilmWork(**out_data))
        except Exception as e:
            print(f'Can\'t convert entry({entry}): {e}')
        else:
            out.write(fw_line)
    return out


def post_film_work(pg_cursor, csv: io.StringIO):
    pg_cursor.execute("TRUNCATE TABLE content.film_work CASCADE;")
    csv.seek(0)
    pg_cursor.copy_expert(
        "COPY content.film_work FROM STDIN \
        WITH CSV DELIMITER ',' NULL 'NULL' QUOTE '\x16';",
        csv)


def extract_genre(cursor: sqlite3.Cursor) -> io.StringIO:
    cursor.execute('SELECT * FROM genre;')
    out = io.StringIO()
    for d in cursor.fetchall():
        entry = dict(d)
        entry["id_"] = entry.pop("id")
        try:
            line = str(Genre(**entry))
        except Exception as e:
            print(f'Can\'t convert entry({entry}): {e}')
        else:
            out.write(line)
    return out


def post_genre(pg_cursor, csv: io.StringIO):
    pg_cursor.execute("TRUNCATE TABLE content.genre CASCADE;")
    csv.seek(0)
    pg_cursor.copy_expert(
        "COPY content.genre FROM STDIN \
        WITH CSV DELIMITER ',' NULL 'NULL' QUOTE '\x16';",
        csv)


def extract_person(cursor: sqlite3.Cursor):
    cursor.execute('SELECT * FROM person;')
    out = io.StringIO()
    for d in cursor.fetchall():
        entry = dict(d)
        entry["id_"] = entry.pop("id")
        try:
            line = str(Person(**entry))
        except Exception as e:
            print(f'Can\'t convert entry({entry}): {e}')
        else:
            out.write(line)
    return out


def post_person(pg_cursor, csv: io.StringIO):
    pg_cursor.execute("TRUNCATE TABLE content.person CASCADE;")
    csv.seek(0)
    pg_cursor.copy_expert(
        "COPY content.person FROM STDIN \
        WITH CSV DELIMITER ',' NULL 'NULL' QUOTE '\x16';",
        csv)


def extract_person_film_work(cursor: sqlite3.Cursor):
    cursor.execute('SELECT * FROM person_film_work;')
    out = io.StringIO()
    for d in cursor.fetchall():
        entry = dict(d)
        entry["id_"] = entry.pop("id")
        try:
            line = str(PersonFilmWork(**entry))
        except Exception as e:
            print(f'Can\'t convert entry({entry}): {e}')
        else:
            out.write(line)
    return out


def post_person_film_work(pg_cursor, csv: io.StringIO):
    pg_cursor.execute("TRUNCATE TABLE content.person_film_work;")
    csv.seek(0)
    pg_cursor.copy_expert(
        "COPY content.person_film_work FROM STDIN \
        WITH CSV DELIMITER ',' NULL 'NULL' QUOTE '\x16';",
        csv)


def extract_genre_film_work(cursor: sqlite3.Cursor):
    cursor.execute('SELECT * FROM genre_film_work;')
    out = io.StringIO()
    for d in cursor.fetchall():
        entry = dict(d)
        entry["id_"] = entry.pop("id")
        try:
            line = str(GenreFilmWork(**entry))
        except Exception as e:
            print(f'Can\'t convert entry({entry}): {e}')
        else:
            out.write(line)
    return out


def post_genre_film_work(pg_cursor, csv: io.StringIO):
    pg_cursor.execute("TRUNCATE TABLE content.genre_film_work;")
    csv.seek(0)
    pg_cursor.copy_expert(
        "COPY content.genre_film_work FROM STDIN \
        WITH CSV DELIMITER ',' NULL 'NULL' QUOTE '\x16';",
        csv)


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
