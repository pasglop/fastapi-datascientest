import os
import sqlite3
import pandas as pd
import requests
from pathlib import Path
import sys

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from app.api.utils import get_project_root, connect, disconnect, QUESTION_DATABASE, DATA_FOLDER, DATA_FILE, \
    hash_password, users


def download_database():
    # download the data from the internet
    if os.path.exists(f'{DATA_FOLDER}/{DATA_FILE}'):
        return True

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    r = requests.get(QUESTION_DATABASE, allow_redirects=True)
    open(f'{DATA_FOLDER}/{DATA_FILE}', 'wb').write(r.content)


def create_database():
    """ create a database connection to a database
    """
    conn = None
    cursor = None
    try:
        conn, cursor = connect()
    except sqlite3.Error as e:
        print(e)
    finally:
        disconnect(conn, cursor)


def create_tables():
    """ create the tables
    """
    conn, cursor = connect()
    # Folder containing your SQL files
    folder_path = get_project_root() / 'install/sql'
    files = [file for file in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path, file)) and file.endswith(".sql")]
    for file in files:
        # Only process .sql files
        if file.endswith('.sql'):
            with open(os.path.join(folder_path, file), 'r') as sql_file:
                try:
                    # Execute the SQL commands
                    sql_command = sql_file.read()
                    cursor.executescript(sql_command)
                except sqlite3.Error as e:
                    if 'already exists' not in str(e):
                        print(f"An error occurred while executing the file {file}: {str(e)}")
                        return False

    # Commit the transaction and close the connection
    conn.commit()
    disconnect(conn, cursor)

    return True


def count_rows(table='questions'):
    """ check if the questions table is empty
    """
    conn, cursor = connect()
    cursor.execute(f"SELECT count(*) FROM {table};")
    len_table = cursor.fetchall()[0][0]
    disconnect(conn, cursor)
    return len_table


def populate_database():
    """ populate the database with some data
    """
    conn, cursor = connect()

    if count_rows() > 0:
        return True

    try:
        df = pd.read_csv(f'{DATA_FOLDER}/{DATA_FILE}', sep=',', encoding='utf-8', header=0)
        df.to_sql('questions_raw', conn)
    except ValueError as e:
        if 'already exists' not in str(e):
            print(f"An error occurred while populating questions table: {str(e)}")
        return True
    finally:
        disconnect(conn, cursor)

    return True


def restructure_db():
    if count_rows('questions') > 0 and count_rows('answers') > 0:
        return True

    conn, cursor = connect()
    try:
        cursor.executescript("""
        INSERT INTO main.categories(name)
        SELECT DISTINCT use FROM main.questions_raw;
        
        INSERT INTO main.subjects(name)
        SELECT DISTINCT subject FROM main.questions_raw;
        
        INSERT INTO main.questions(title, category_id, subject_id, remark) 
        SELECT question, (SELECT id FROM main.categories WHERE name = use), 
        (SELECT id FROM main.subjects WHERE name = subject), remark FROM main.questions_raw;
        
        INSERT INTO main.answers(question_id, answer_text, is_correct)
        SELECT question_id, answer, COALESCE(is_correct, 0)
        from (select (SELECT question_id FROM main.questions WHERE title = question) as question_id,
                     responseA          as answer,
                     correct LIKE '%A%' as is_correct
              FROM main.questions_raw
              UNION ALL
              select (SELECT question_id FROM main.questions WHERE title = question) as question_id,
                     responseB          as answer,
                     correct LIKE '%B%' as is_correct
              FROM main.questions_raw
              UNION ALL
              select (SELECT question_id FROM main.questions WHERE title = question) as question_id,
                     responseC          as answer,
                     correct LIKE '%C%' as is_correct
              FROM main.questions_raw
              UNION ALL
              select (SELECT question_id FROM main.questions WHERE title = question) as question_id,
                     responseD          as answer,
                     correct LIKE '%D%' as is_correct
              FROM main.questions_raw) where question_id is not null and answer is not null;
              
              DROP TABLE main.questions_raw;
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while executing the file the query: {str(e)}")

    return count_rows('questions') > 0 and count_rows('answers') > 0


def create_users():
    if count_rows('users') > 0:
        return True

    conn, cursor = connect()
    try:
        for user in users:
            cursor.execute(f"INSERT INTO main.users(user_name, user_password, is_admin, user_email) "
                           f"VALUES ('{user['name']}', '{hash_password(user['password'])}', "
                           f"{user['is_admin']}, '{user['name'] + '@email.com'}');")
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while executing the file the query: {str(e)}")

    return False


if __name__ == '__main__':
    create_database()
    download_database()
    create_database()
    create_tables()
    populate_database()
    restructure_db()
    create_users()
