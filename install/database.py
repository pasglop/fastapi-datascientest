import os
from pathlib import Path
import sqlite3
from sqlite3 import Error
import pandas as pd

import dotenv
import requests

from src.utils import get_project_root

dotenv.load_dotenv()

QUESTION_DATABASE = os.environ.get('QUESTION_DATABASE')
DATA_FOLDER = os.environ.get('DATA_FOLDER')


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
    data_folder = get_project_root() / DATA_FOLDER
    data_file = 'questions.csv'
    if os.path.exists(f'{data_folder}/{data_file}'):
        return True

    os.mkdir(data_folder)
    r = requests.get(QUESTION_DATABASE, allow_redirects=True)
    open(f'{data_folder}/{data_file}', 'wb').write(r.content)


def create_database():
    """ create a database connection to a database that resides
        in the memory
    """
    conn = None
    try:
        conn = sqlite3.connect('./data/questions.db')
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
