from contextlib import contextmanager
from dataclasses import dataclass
import io
import logging
import os
import sqlite3
from typing import Callable, Union

from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import DictCursor

import tables
from tables import SqliteTables

AnyTable = Union[
    tables.FilmWork,
    tables.Genre,
    tables.Person,
    tables.PersonFilmWork,
    tables.GenreFilmWork
]

logging.basicConfig(format="%(asctime)s[%(name)s]: %(message)s", level="INFO")
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Convertor:
    sqlite_table: str
    psql_table: str
    convert: Callable[[dict], AnyTable]


def load_from_sqlite(sqlite_curs: sqlite3.Cursor, pg_cursor):
    convertors = (
        Convertor(
            sqlite_table='film_work',
            psql_table='content.film_work',
            convert=lambda data: tables.FilmWork.create_from_sqlite(
                SqliteTables.FilmWork(**data))
        ),
        Convertor(
            sqlite_table='genre',
            psql_table='content.genre',
            convert=lambda data: tables.Genre.create_from_sqlite(
                SqliteTables.Genre(**data))
        ),
        Convertor(
            sqlite_table='person',
            psql_table='content.person',
            convert=lambda data: tables.Person.create_from_sqlite(
                SqliteTables.Person(**data))
        ),
        Convertor(
            sqlite_table='genre_film_work',
            psql_table='content.genre_film_work',
            convert=lambda data: tables.GenreFilmWork.create_from_sqlite(
                SqliteTables.GenreFilmWork(**data))
        ),
        Convertor(
            sqlite_table='person_film_work',
            psql_table='content.person_film_work',
            convert=lambda data: tables.PersonFilmWork.create_from_sqlite(
                SqliteTables.PersonFilmWork(**data))
        ),
    )
    result = True
    for conv in convertors:
        buff = io.StringIO()
        buff = extract(sqlite_curs, conv.sqlite_table, conv.convert, buff)
        try:
            post(pg_cursor, buff, conv.psql_table)
        except Exception as exp:
            logger.error(f'Insertion into {conv.psql_table} error: {exp}.')
            result = False
            break
        else:
            logger.debug(f'{conv.sqlite_table} copied into {conv.psql_table}')
    return result


def extract(cursor: sqlite3.Cursor,
            sqlite_table: str,
            convertor: Callable[[dict], str],
            out_stream: io.TextIOBase) -> io.TextIOBase:
    cursor.execute('SELECT * FROM {table};'.format(table=sqlite_table))
    for entry in cursor.fetchall():
        try:
            fw_line = str(convertor(dict(entry)))
        except Exception as e:
            logger.error(f'Can\'t convert entry({entry}): {e}')
        else:
            out_stream.write(fw_line)
    return out_stream


def extract_part(cursor: sqlite3.Cursor,
                 table_name: str,
                 limit: int,
                 offset: int = 0) -> list:
    cursor.execute(
        'SELECT * FROM {table} LIMIT {limit} OFFSET {offset};'.format(
            table=table_name,
            limit=limit,
            offset=offset
        )
    )

    return cursor.fetchall()


def post(pg_cursor, csv: io.TextIOBase, postgres_name: str):
    pg_cursor.execute(
        'TRUNCATE TABLE {table} CASCADE;'.format(table=postgres_name))
    csv.seek(0)
    pg_cursor.copy_expert(
        "COPY {table} FROM STDIN \
        WITH CSV DELIMITER '{delim}' NULL '{null}' QUOTE '{quote}';".format(
            table=postgres_name,
            delim=tables.DELIMITER,
            null=tables.NULL_SYMBOL,
            quote=tables.QUOTE_SYMBOL),
        csv)


@contextmanager
def sqlite_conn_context(db_path: str):
    """ Attention!

        We couldn't use 'sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES'
        for connection, Our db contains wrong formatted datetime fields:
        e.g: 'filmwork' 6th row field 'updated_at'
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def main():
    load_dotenv()
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': int(os.environ.get('DB_PORT', 5432)),
    }
    db_path = os.environ.get('SQL_LITE_DB_PATH', 'db.sqlite')
    psycopg2.extras.register_uuid()

    with sqlite_conn_context(db_path) as sqlite, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn, \
            pg_conn.cursor() as pg_cursor:
        pg_cursor.execute('SET SESSION TIME ZONE "UTC";')
        if not load_from_sqlite(sqlite.cursor(), pg_cursor):
            pg_conn.rollback()
            logger.error('There were some problems by tables. ' +
                         'Please check the work result in your DB viewer')
        else:
            logger.info(f'Database coping finished successful')


if __name__ == '__main__':
    main()
