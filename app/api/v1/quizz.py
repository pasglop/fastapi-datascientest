from app.api.v1.models import CategorySchema, QuestionAnswerSchema, SubjectItemSchema, QuestionSchema
from app.utils import sql_data_to_list_of_dicts


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
