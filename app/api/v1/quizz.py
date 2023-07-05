from typing import List

from pydantic import BaseModel
from pydantic.fields import Field
from app.utils import sql_data_to_list_of_dicts


class CategorySchema(BaseModel):
    id: int = Field(...)
    name: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "General"
            }
        }


class SubjectsSchema(BaseModel):
    id: int = Field(...)
    name: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "BDD"
            }
        }


class QuestionAnswerSchema(BaseModel):
    answer_id: int
    question_id: int
    answer_text: str
    is_correct: bool

    class Config:
        schema_extra = {
            "example": {
                "answer_id": 1,
                "question_id": 1,
                "answer_text": "Blanc",
                "is_correct": True
            }
        }


class SubjectItemSchema(BaseModel):
    id: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": 1
            }
        }


class QuestionSchema(BaseModel):
    question_id: int
    title: str
    remark: str | None
    category: CategorySchema
    subject: SubjectItemSchema
    answers: list[QuestionAnswerSchema] | None

    class Config:
        schema_extra = {
            "example": {
                "question_id": 1,
                "title": "Quelle est la couleur du cheval blanc d'Henri IV ?",
                "remark": "C'est une question piège",
                "category": {
                    "id": 1,
                    "name": "General"
                },
                "subject": {
                    "id": 1,
                    "name": "BDD"
                }
            }
        }


class SubjectListSchema(BaseModel):
    id: List[SubjectItemSchema] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            }
        }


class QuestionSetSchema(BaseModel):
    category: int | None
    subjects: List[int] | None
    limit: int = 1

    class Config:
        schema_extra = {
            "example": {
                "category_id": 1,
                "subject_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "limit": 10
            }
        }


class Quizz:
    def __init__(self):
        self.questions = None

    def get_question_set(self, QuestionSetSchema) -> list[QuestionSchema]:
        category = QuestionSetSchema.category
        subjects = QuestionSetSchema.subjects
        limit = QuestionSetSchema.limit
        if subjects is None:
            subjects = []
        query = "SELECT " \
                "question_id, title, " \
                "'{\"id\":\"' || category_id || '\", \"name\": \"' || categories.name || '\"}' as category, " \
                "'{\"id\":\"' || subject_id || '\", \"name\": \"' || categories.name || '\"}' as subject, " \
                "remark, created_at, updated_at " \
                "FROM questions " \
                "LEFT JOIN categories ON questions.category_id = categories.id " \
                "LEFT JOIN subjects ON questions.subject_id = subjects.id"
        query_params = []
        if category:
            query_params.append(f"category_id = {category}")
        if len(subjects) > 0:
            query_params.append(f"subject_id in ({','.join([str(i) for i in subjects])})")
        if len(query_params) > 0:
            query += " WHERE " + " AND ".join(query_params)
        query += f" LIMIT {limit}"
        res = sql_data_to_list_of_dicts(query)
        for question in res:
            question["category"] = CategorySchema.parse_raw(question["category"])
            question["subject"] = SubjectItemSchema.parse_raw(question["subject"])
            question["answers"] = self.get_answers(question["question_id"])
        self.questions = [QuestionSchema(**x) for x in res]
        return self.questions

    def get_answers(self, question_id: int) -> list[QuestionAnswerSchema]:
        query = f"SELECT answer_id, answer_text, is_correct, {question_id} as question_id " \
                f"FROM answers WHERE question_id = {question_id}"
        res = sql_data_to_list_of_dicts(query)
        return [QuestionAnswerSchema(**x) for x in res]
