import datetime
import sqlite3

from app.api.v1.models import CategorySchema, SubjectsSchema, QuestionSchema, QuestionTableSchema, CreateQuestionSchema, \
    CreateAnswerSchema
from app.utils import connect


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

    def create_question(self, data: CreateQuestionSchema):
        # then insert question
        question_id = self.insert_question(data)
        # then insert answers
        for answer in data.answers:
            self.insert_answer(answer, question_id)
        return question_id

    def insert_question(self, data: CreateQuestionSchema):
        question_id = None
        try:
            insert_query = """
            INSERT INTO questions(title, category_id, subject_id, remark, updated_at)
            VALUES(?, ?, ?, ?, ?)
            RETURNING question_id
            """
            self.cursor.execute(insert_query,
                                (data.title, data.category_id, data.subject_id, data.remark, datetime.datetime.now()))
            question_id = self.cursor.fetchone()[0]
        except sqlite3.Error as e:
            self.conn.rollback()
            raise e

        self.conn.commit()
        return question_id

    def insert_answer(self, answers: CreateAnswerSchema, question_id):
        try:
            insert_query = """
            INSERT INTO answers(answer_text, is_correct, question_id, updated_at)
            VALUES(?, ?, ?, ?)
            """
            self.cursor.execute(insert_query, (answers.answer_text, answers.is_correct,
                                               question_id, datetime.datetime.now()))
        except sqlite3.Error as e:
            self.conn.rollback()
            raise e

        self.conn.commit()
        return answers

    def delete_question(self, id: int):
        try:
            delete_query = f"""
            DELETE FROM questions WHERE question_id = {id}
            """
            self.cursor.execute(delete_query)
        except sqlite3.Error as e:
            self.conn.rollback()
            raise e

        self.conn.commit()
        return id

    def delete_answers(self, id: int):
        try:
            delete_query = f"""
            DELETE FROM answers WHERE question_id = {id}
            """
            self.cursor.execute(delete_query)
        except sqlite3.Error as e:
            self.conn.rollback()
            raise e

        self.conn.commit()
        return id
