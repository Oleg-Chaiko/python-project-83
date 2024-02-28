from psycopg2 import connect, sql, extras
from dotenv import load_dotenv
from datetime import date
import os


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def conection_url(func):
    def wraper(*args):
        with connect(DATABASE_URL) as conn:
            with conn.cursor(cursor_factory=extras.DictCursor) as cursor:
                return func(*args, conn, cursor)
    return wraper


@conection_url
def add_url(url, conn, cursor):
    creat_at = date.today()
    query = sql.SQL(
        "INSERT INTO {table} (name, created_at) VALUES (%s, %s)"'RETURNING id'
    ).format(
        table=sql.Identifier('urls'),
    )
    cursor.execute(query, (url, creat_at))

    result = cursor.fetchone()
    conn.commit()
    return result[0]


@conection_url
def get_data_by_url(url, conn, cursor):
    query = sql.SQL("SELECT * FROM {table} WHERE {key} = %s").format(
        table=sql.Identifier('urls'),
        key=sql.Identifier('name')
    )
    cursor.execute(query, (url,))
    result = cursor.fetchall()
    if result:
        return result[0][0]


@conection_url
def get_data_by_id(id, conn, cursor):
    query = sql.SQL("SELECT * FROM {table} WHERE {key} = %s").format(
        table=sql.Identifier('urls'),
        key=sql.Identifier('id')
    )
    cursor.execute(query, (id,))
    result = cursor.fetchall()
    return result[0]


@conection_url
def get_all_urls(conn, cursor):
    cursor.execute(
        sql.SQL("SELECT * FROM {table}").format(
            table=sql.Identifier('urls')
        )
    )
    result = cursor.fetchall()
    return result


print(get_data_by_url('github.com'))