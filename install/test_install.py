import os
import csv
from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from install.database import download_database, create_database, create_tables, \
    count_rows, populate_database, restructure_db, create_users
from app.api.utils import connect, disconnect, DATA_FOLDER, DATA_FILE, DATA_DB, users


class TestInstall:
    def test_origin_data_is_downloaded(self):
        """ test that the data is downloaded from the internet
        """
        try:
            download_database()
        except Exception as e:
            assert False, f"download_database() raised {e} unexpectedly!"
        assert True

    def test_data_is_downloaded(self):
        """ test that the data is downloaded from the internet
        """
        assert os.path.exists(f'{DATA_FOLDER}/{DATA_FILE}')

    def test_database_file_is_created(self):
        """ test that the database file is created
        """
        create_database()

        assert os.path.exists(f'{DATA_FOLDER}/{DATA_DB}')

    def test_tables_exists(self):
        """ test that the tables are created
        """
        tables = []
        list_expected_tables = ['questions', 'categories', 'subjects', 'users', 'answers', 'user_answers']
        if create_tables() is True:
            conn, cursor = connect()
            cursor.execute("SELECT name FROM main.sqlite_master WHERE type='table';")

            # Fetch all results of the query
            tables = [table[0] for table in cursor.fetchall()]
        assert all(elem in tables for elem in list_expected_tables)

    def test_database_is_populated(self):
        """ test that the database is populated
        """

        if count_rows('questions') > 0 and count_rows('answers') > 0:
            assert True  # database is already populated
            return

        populate_database()
        # read original csv file and count lines
        with open(f'{DATA_FOLDER}/{DATA_FILE}', 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            len_file = sum(1 for row in reader) - 1  # remove header line

        # read database and count lines
        len_table = count_rows('questions_raw')

        assert len_file == len_table

    def test_database_is_restructured(self):
        """ test that the database is restructured
            means that answers is populated with the answers from the questions table
        """
        assert restructure_db() is True

    def test_dummy_users_are_created(self):
        """ test that the dummy users are created
        """
        if create_users() is True:
            assert True

        conn, cursor = connect()
        cursor.execute("SELECT count(*) FROM users;")
        len_table = cursor.fetchall()[0][0]

        cursor.execute("SELECT count(*) FROM users where is_admin is true;")
        len_admin = cursor.fetchall()[0][0]
        disconnect(conn, cursor)

        assert len_table == len(users) and len_admin == 1
