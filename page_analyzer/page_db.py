from psycopg2 import connect, sql, extras
from dotenv import load_dotenv
from datetime import date
from contextlib import suppress
from page_analyzer.analizer import get_analize
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
def get_id_by_url(url, conn, cursor):
    query = sql.SQL("SELECT * FROM {table} WHERE {key} = %s").format(
        table=sql.Identifier('urls'),
        key=sql.Identifier('name')
    )
    cursor.execute(query, (url,))
    result = cursor.fetchone()
    if result:
        return result['id']


@conection_url
def get_data_by_id(id, conn, cursor):
    query = sql.SQL("SELECT * FROM {table} WHERE {key} = %s").format(
        table=sql.Identifier('urls'),
        key=sql.Identifier('id')
    )
    cursor.execute(query, (id,))
    result = cursor.fetchone()
    return result


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
            check = get_last_check(cursor, item.get('id'))
            item['last_check'] = check.get('created_at')
            item['status_code'] = check.get('status_code')
            print(check)
        result.append(item)
    return result


@conection_url
def url_check(url_id, conn, cursor):
    url = get_data_by_id(url_id)['name']
    check = get_analize(url)
    creat_at = date.today()
    query = sql.SQL(
        "INSERT INTO {table} "
        "(url_id, created_at, status_code, h1, title, description)"
        "VALUES (%s, %s, %s, %s, %s, %s)"
        "RETURNING id"
    ).format(
        table=sql.Identifier('url_checks'),
    )
    cursor.execute(
        query, (
            url_id,
            creat_at,
            check.get('status_code'),
            check.get('h1'),
            check.get('title'),
            check.get('description')
        )
    )
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
        "SELECT {creat_at},{status_code} from {table}"
        "WHERE {item} = %s "
        "ORDER BY {id} DESC LIMIT 1"
    ).format(
        creat_at=sql.Identifier('created_at'),
        status_code=sql.Identifier('status_code'),
        table=sql.Identifier('url_checks'),
        item=sql.Identifier('url_id'),
        id=sql.Identifier('id'),
    )
    cursor.execute(query, (id_url,))
    result = cursor.fetchone()
    if result is None:
        raise FileNotFoundError
    return result
