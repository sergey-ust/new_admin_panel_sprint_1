from contextlib import contextmanager
from dataclasses import dataclass
import datetime
import os
import sqlite3
import uuid

from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor


@dataclass()
class FilmWork:
    """PostreSQL 'filmwork' Table."""

    _TITLE_MAX_LEN = 200
    _TYPE_MAX_LEN = 15

    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.date
    rating: float
    type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    # timestamp max value is 2038 year

    def __init__(
            self, id_: str, title: str, description: str,
            creation_date: str, rating: float, type_: str,
            created_at: datetime.datetime, updated_at: datetime.datetime
    ):
        self.id = uuid.UUID(id_)
        self.title = title[: self._TITLE_MAX_LEN]
        self.description = description if description else ''
        self.creation_date = datetime.date.fromisoformat(
            creation_date if creation_date else '2038-01-19')
        self.rating = rating
        self.type = type_[:self._TYPE_MAX_LEN]
        self.created_at = \
            created_at if created_at else datetime.datetime.utcnow()
        self.created_at = \
            updated_at if updated_at else datetime.datetime.utcnow()


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


if __name__ == '__main__':
    load_dotenv()
    # dsl = {
    #     'dbname': 'movies_database',
    #     'user': 'app',
    #     'password': '123qwe',
    #     'host': '127.0.0.1',
    #     'port': 5432
    # }
    # with sqlite3.connect('db.sqlite') as sqlite_conn,\
    #         psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
    #     load_from_sqlite(sqlite_conn, pg_conn)

    db_path = os.environ.get('SQL_LITE_DB_PATH', 'db.sqlite')
    with conn_context(db_path) as conn:
        curs = conn.cursor()
        curs.execute('SELECT * FROM film_work;')
        data = curs.fetchall()
        for d in data:
            d["id_"] = d.pop("id")
            d["type_"] = d.pop("type")
            d.pop("filepath")
            try:
                FilmWork(**d)
            except Exception as e:
                print("Can't convert entry: {}".format(e))
