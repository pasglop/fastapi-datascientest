from fastapi.testclient import TestClient
from app.api.v1.api import app
from app.api.v1.quizz import Quizz, QuestionSchema, QuestionSetSchema

client = TestClient(app)

API_URL = "http://localhost:8081"


class TestQuizz:
    def test_pick_a_question(self):
        q = Quizz()
        params = QuestionSetSchema()
        assert len(q.get_question(params)) == 1

    def test_pick_multiple_question(self):
        q = Quizz()
        params = QuestionSetSchema(limit=10)
        assert len(q.get_question(params)) == 10

    def test_pick_a_question_is_QuestionSchema(self):
        q = Quizz()
        params = QuestionSetSchema()
        assert isinstance(q.get_question(params)[0], QuestionSchema)

    def test_pick_a_question_for_category(self):
        q = Quizz()
        params = QuestionSetSchema(category_id=1)
        assert q.get_question(params)[0].category.id == 1

    def test_pick_a_question_for_one_subject(self):
        q = Quizz()
        params = QuestionSetSchema(subjects=[1])
        assert q.get_question(params)[0].subject.id == 1

    def test_pick_a_question_for_multiple_subject(self):
        q = Quizz()
        params = QuestionSetSchema(subjects=[1, 2, 3])
        assert q.get_question(params)[0].subject.id in [1, 2, 3]

    def test_pick_a_question_for_multiple_subjects_and_one_category(self):
        q = Quizz()
        params = QuestionSetSchema(category_id=1, subjects=[1, 2, 3])
        res = q.get_question(params)[0]
        assert res.subject.id in [1, 2, 3]
        assert res.category.id == 1

    def test_pick_a_questions_and_answers(self):
        q = Quizz()
        params = QuestionSetSchema()
        res = q.get_question(params)[0]
        assert isinstance(res, QuestionSchema)
        assert isinstance(res.answers, list)
        assert res.answers[0].question_id == res.question_id

    def test_save_user_answers(self):
        assert False

    def test_get_user_answers(self):
        assert False

    def test_get_user_score(self):
        assert False

    def test_add_question(self):
        assert False

    def test_edit_question(self):
        assert False

    def test_delete_question(self):
        assert False
