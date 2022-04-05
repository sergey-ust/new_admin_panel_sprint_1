from contextlib import contextmanager
import os
import sqlite3

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from tables import FilmWork, Genre, Person, PersonFilmWork, \
    GenreFilmWork


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    # postgres_saver = PostgresSaver(pg_conn)
    # sqlite_loader = SQLiteLoader(connection)

    # data = sqlite_loader.load_movies()
    # postgres_saver.save_all_data(data)


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def extract_film_work(db_path: str):
    with conn_context(db_path) as conn, open("film_work.csv", "w") as csv_file:
        curs = conn.cursor()
        curs.execute('SELECT * FROM film_work;')
        data = curs.fetchall()
        for d in data:
            out_data = dict(d)
            out_data["id_"] = out_data.pop("id")
            out_data["type_"] = out_data.pop("type")
            out_data.pop("file_path")
            try:
                csv_file.write(str(FilmWork(**out_data)))
            except Exception as e:
                print("Can't convert entry: {}".format(e))


def post_film_work(**kwargs):
    with psycopg2.connect(**kwargs, cursor_factory=DictCursor) as pg_conn, \
            pg_conn.cursor() as pg_cursor:
        pg_cursor.execute("TRUNCATE TABLE content.person_film_work;")
        pg_cursor.execute("TRUNCATE TABLE content.genre_film_work;")
        pg_cursor.execute("TRUNCATE TABLE content.film_work CASCADE;")
        with open("film_work.csv", "r") as csv_file:
            pg_cursor.copy_expert(
                "COPY content.film_work \
                FROM STDIN WITH CSV DELIMITER '|' QUOTE '\u00016';",
                csv_file)


def extract_genre(db_path: str):
    with conn_context(db_path) as conn, open("genre.csv", "w") as csv_file:
        curs = conn.cursor()
        curs.execute('SELECT * FROM genre;')
        data = curs.fetchall()
        for d in data:
            out_data = dict(d)
            out_data["id_"] = out_data.pop("id")
            try:
                csv_file.write(str(Genre(**out_data)))
            except Exception as e:
                print("Can't convert entry: {}".format(e))


def post_genre(**kwargs):
    with psycopg2.connect(**kwargs, cursor_factory=DictCursor) as pg_conn, \
            pg_conn.cursor() as pg_cursor:
        pg_cursor.execute("TRUNCATE TABLE content.genre_film_work;")
        pg_cursor.execute("TRUNCATE TABLE content.genre CASCADE;")
        with open("genre.csv", "r") as csv_file:
            pg_cursor.copy_expert(
                "COPY content.genre \
                FROM STDIN WITH CSV DELIMITER '|' QUOTE '\u00016';",
                csv_file)


def extract_person(db_path: str):
    with conn_context(db_path) as conn, open("person.csv", "w") as csv_file:
        curs = conn.cursor()
        curs.execute('SELECT * FROM person;')
        data = curs.fetchall()
        for d in data:
            out_data = dict(d)
            out_data["id_"] = out_data.pop("id")
            try:
                csv_file.write(str(Person(**out_data)))
            except Exception as e:
                print("Can't convert entry: {}".format(e))


def extract_person_film_work(db_path: str):
    with conn_context(db_path) as conn, open("person_film_work.csv",
                                             "w") as csv_file:
        curs = conn.cursor()
        curs.execute('SELECT * FROM person_film_work;')
        data = curs.fetchall()
        for d in data:
            out_data = dict(d)
            out_data["id_"] = out_data.pop("id")
            try:
                csv_file.write(str(PersonFilmWork(**out_data)))
            except Exception as e:
                print("Can't convert entry: {}".format(e))


def extract_genre_film_work(db_path: str):
    with conn_context(db_path) as conn, open("genre_film_work.csv",
                                             "w") as csv_file:
        curs = conn.cursor()
        curs.execute('SELECT * FROM genre_film_work;')
        data = curs.fetchall()
        for d in data:
            out_data = dict(d)
            out_data["id_"] = out_data.pop("id")
            try:
                csv_file.write(str(GenreFilmWork(**out_data)))
            except Exception as e:
                print("Can't convert entry: {}".format(e))


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

    extract_film_work(db_path)
    post_film_work(**dsl)


if __name__ == '__main__':
    main()
