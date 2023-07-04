from app.api.v1.quizz import CategorySchema, SubjectsSchema
from app.utils import disconnect, connect, split_str, sql_data_to_list_of_dicts
from pydantic import BaseModel, Field, validator
from typing import List


class Question:
    def __init__(self):
        self.conn, self.cursor = connect()

    def get_categories(self):
        self.cursor.execute("SELECT * FROM categories")
        categories = self.cursor.fetchall()

        return categories

    def insert_category(self, data: CategorySchema):
        self.cursor.execute(f"INSERT INTO categories(name) VALUES('{data.name}')")
        self.conn.commit()

        return data

    def get_subjects(self):
        self.cursor.execute("SELECT * FROM subjects")
        subjects = self.cursor.fetchall()

        return subjects

    def insert_subject(self, data: SubjectsSchema):
        self.cursor.execute(f"INSERT INTO subjects(name) VALUES('{data.name}')")
        self.conn.commit()

        return data

    def list_questions(self):
        self.cursor.execute("SELECT * FROM questions")
        questions = self.cursor.fetchall()

        return questions
