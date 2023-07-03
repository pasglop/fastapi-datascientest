import os
import sqlite3
from hashlib import sha1
from pathlib import Path
from sqlite3 import Error
import dotenv

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
