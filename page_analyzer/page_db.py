from psycopg2 import connect, sql, extras
from dotenv import load_dotenv
from datetime import date
from contextlib import suppress
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
    result = []
    cursor.execute("SELECT id, name FROM urls ORDER BY id DESC;")
    array = cursor.fetchall()
    for val in array:
        with suppress(FileNotFoundError):
            item = {'id': val[0],
                    'name': val[1],
                    'last_check': "",
                    'status_code': ""
                    }
            last_check = get_last_check(cursor, item.get('id'))
            print(last_check)
            item['last_check'] = last_check
        result.append(item)
    return result


@conection_url
def url_check(url_id, conn, cursor):
    creat_at = date.today()
    query = sql.SQL(
        "INSERT INTO {table} (url_id, created_at) VALUES (%s, %s)"'RETURNING id'
    ).format(
        table=sql.Identifier('url_checks'),
    )
    cursor.execute(query, (url_id, creat_at))
    conn.commit()

@conection_url
def get_checks(url_id, conn, cursor):
    query = sql.SQL(
        "SELECT * FROM {table}"
        "WHERE {value_3} = %s"
        "ORDER BY {id} DESC;"
    ).format(
        id=sql.Identifier('id'),
        value_3=sql.Identifier('url_id'),
        table=sql.Identifier('url_checks')
    )
    cursor.execute(query, (url_id,))
    array = cursor.fetchall()
    return array


def get_last_check(cursor, id_url):
    query = sql.SQL(
        "SELECT {creat_at} from {table}"
        "WHERE {item} = %s "
        "ORDER BY {id} DESC LIMIT 1"
    ).format(
        creat_at=sql.Identifier('created_at'),
        table=sql.Identifier('url_checks'),
        item=sql.Identifier('url_id'),
        id=sql.Identifier('id'),
    )
    cursor.execute(query, (id_url,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return ''


