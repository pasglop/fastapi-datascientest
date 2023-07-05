import os
import sqlite3
from hashlib import sha1
from pathlib import Path
from sqlite3 import Error
import dotenv
from pydantic.fields import ModelField, SHAPE_LIST, SHAPE_SET, SHAPE_TUPLE
from typing import Any, ClassVar

ITERABLE_SHAPES = {...}

dotenv.load_dotenv()


def get_project_root() -> Path:
    return Path(__file__).parent.parent


QUESTION_DATABASE = os.environ.get('QUESTION_DATABASE')
DATA_FOLDER = get_project_root() / os.environ.get('DATA_FOLDER')
DATA_FILE = os.environ.get('DATA_FILE')
DATA_DB = os.environ.get('DATA_DB')

SALT_PASSWORD = os.environ.get('SALT_PASSWORD')

JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')

API_URL = os.environ.get('API_URL')


def connect():
    """ create a database connection to a database that resides
        in the memory
    """
    cursor = None
    conn = None
    try:
        conn = sqlite3.connect(f'{DATA_FOLDER}/{DATA_DB}')
    except Error as e:
        print(e)

    if conn:
        cursor = conn.cursor()

    return conn, cursor


def disconnect(conn, cursor):
    """ disconnect from the database
    """
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def sql_data_to_list_of_dicts(select_query):
    """Returns data from an SQL query as a list of dicts."""
    con = None
    try:
        con = sqlite3.connect(f'{DATA_FOLDER}/{DATA_DB}')
        con.row_factory = sqlite3.Row
        things = con.execute(select_query).fetchall()
        unpacked = [{k: item[k] for k in item.keys()} for item in things]
        return unpacked
    except Exception as e:
        print(f"Failed to execute. Query: {select_query}\n with error:\n{e}")
        return []
    finally:
        con.close()


def split_str(v: Any, field: ModelField) -> Any:
    res_array = []
    if isinstance(v, str) and field.shape in ITERABLE_SHAPES:
        values = v.split(",")
        for item in values:
            item = item.strip()
            if item.isdigit():
                res_array.append(int(item))
            else:
                res_array.append(item)
    elif isinstance(v, str) and v.isdigit():
        res_array.append(int(v))
    else:
        res_array.append(int(v))

    if field.shape == SHAPE_LIST:
        return list(res_array)
    elif field.shape == SHAPE_SET:
        return set(res_array)
    elif field.shape == SHAPE_TUPLE:
        return tuple(res_array)


def hash_password(password):
    """ hash a password for storing
    """
    return sha1((SALT_PASSWORD + password).encode()).hexdigest()


users = [
    {'name': 'alice', 'password': 'wonderland', 'is_admin': False},
    {'name': 'bob', 'password': 'builder', 'is_admin': False},
    {'name': 'clementine', 'password': 'mandarine', 'is_admin': False},
    {'name': 'admin', 'password': '4dm1N', 'is_admin': True}
]
