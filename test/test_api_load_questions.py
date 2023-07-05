from app.api.v1.quizz import Quizz, QuestionSchema, QuestionSetSchema, QuestionAnswerSchema
from app.utils import API_URL
from fixtures import log_user


class TestQuizz:
    def test_pick_a_question(self):
        q = Quizz()
        params = QuestionSetSchema()
        assert len(q.get_question_set(params)) == 1

    def test_pick_multiple_question(self):
        q = Quizz()
        params = QuestionSetSchema(limit=10)
        assert len(q.get_question_set(params)) == 10

    def test_pick_a_question_is_QuestionSchema(self):
        q = Quizz()
        params = QuestionSetSchema()
        assert isinstance(q.get_question_set(params)[0], QuestionSchema)

    def test_pick_a_question_for_category(self):
        q = Quizz()
        params = QuestionSetSchema(category_id=1)
        assert q.get_question_set(params)[0].category.id == 1

    def test_pick_a_question_for_one_subject(self):
        q = Quizz()
        params = QuestionSetSchema(subjects=[1])
        assert q.get_question_set(params)[0].subject.id == 1

    def test_pick_a_question_for_multiple_subject(self):
        q = Quizz()
        params = QuestionSetSchema(subjects=[1, 2, 3])
        assert q.get_question_set(params)[0].subject.id in [1, 2, 3]

    def test_pick_a_question_for_multiple_subjects_and_one_category(self):
        q = Quizz()
        params = QuestionSetSchema(category_id=1, subjects=[1, 2, 3])
        res = q.get_question_set(params)[0]
        assert res.subject.id in [1, 2, 3]
        assert res.category.id == 1

    def test_pick_a_questions_and_answers(self):
        q = Quizz()
        params = QuestionSetSchema()
        res = q.get_question_set(params)[0]
        assert isinstance(res, QuestionSchema)
        assert isinstance(res.answers, list)
        assert res.answers[0].question_id == res.question_id
        assert isinstance(res.answers[0], QuestionAnswerSchema)

    def test_call_Api_to_get_a_quizz(self, log_user):
        response = log_user[0].post(
            f"{API_URL}/quizz",
            json={"limit": 10},
            headers={"Authorization": f"Bearer {log_user[1]}"})
        json = response.json()
        quizz_res = json['data']
        assert response.status_code == 200
        check_type = QuestionSchema(**quizz_res[0])
        assert isinstance(check_type, QuestionSchema)

