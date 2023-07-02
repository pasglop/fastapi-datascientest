import os
import sqlite3
from sqlite3 import Error
import pandas as pd

import dotenv
import requests

dotenv.load_dotenv()

QUESTION_DATABASE = os.environ.get('QUESTION_DATABASE')


def create_connection():
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None
    try:
        conn = sqlite3.connect(':memory:')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def download_database():
    # download the data from the internet
    r = requests.get(QUESTION_DATABASE, allow_redirects=True)
    open('questions.csv', 'wb').write(r.content)


def create_database():
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None
    try:
        conn = sqlite3.connect('questions.db')
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def populate_database():
    """ populate the database with some data
    """
    df = pd.read_csv('questions.csv')

    pass


if __name__ == '__main__':
    create_connection()

    if not os.path.exists('questions.csv'):
        download_database()

    if not os.path.exists('questions.db'):
        create_database()
