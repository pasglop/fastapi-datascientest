import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


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


class CreateAnswerSchema(BaseModel):
    answer_text: str
    is_correct: bool = False

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


class CreateQuestionSchema(BaseModel):
    title: str
    remark: str | None
    category_id: int
    subject_id: int
    answers: list[CreateAnswerSchema] | None

    class Config:
        schema_extra = {
            "example": {
                "title": "Quelle est la couleur du cheval blanc d'Henri IV ?",
                "remark": "C'est une question piège",
                "category_id": 1,
                "subject_id": 1,
                "answers": [
                    {
                        "answer_text": "Blanc",
                        "is_correct": True
                    }
                ]
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


class QuestionTableSchema(BaseModel):
    question_id: Optional[int]
    title: str
    category_id: int
    subject_id: int
    remark: str | None
