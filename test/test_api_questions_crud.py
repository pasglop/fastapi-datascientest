import pytest
from fastapi.testclient import TestClient
from app.api.v1.api import app
from app.utils import API_URL
from fixtures import log_user, log_admin


class TestApiQuestionCrud:
    @pytest.fixture()
    def dummy_question(self):
        return {
            "title": "Quelle est la couleur du cheval blanc d'Henri IV ?",
            "answers": [
                {"answer_text": "Blanc", "is_correct": True},
                {"answer_text": "Noir"},
                {"answer_text": "Bleu"},
                {"answer_text": "Rouge"},
            ],
            "remark": "dummy question",
            "category_id": 1,
            "subject_id": 1
        }

    # test the creation of a question
    def test_create_question_complete(self, log_admin, dummy_question):
        response = log_admin[0].post(
            f"{API_URL}/questions",
            json=dummy_question,
            headers={"Authorization": f"Bearer {log_admin[1]}"})
        assert response.status_code == 200
        assert response.json()['data'] == "Question created"

    def test_create_question_incomplete(self, log_admin):
        response = log_admin[0].post(
            f"{API_URL}/questions",
            json={"question": "Quelle est la couleur du cheval blanc d'Henri IV ?"},
            headers={"Authorization": f"Bearer {log_admin[1]}"})
        assert response.status_code == 422

    def test_delete_question(self, log_admin):
        response = log_admin[0].delete(
            f"{API_URL}/questions/1",
            headers={"Authorization": f"Bearer {log_admin[1]}"})
        assert response.status_code == 200
        assert response.json()['data'] == "Question deleted"

    def test_list_categories(self, log_user):
        response = log_user[0].get(
            f"{API_URL}/categories",
            headers={"Authorization": f"Bearer {log_user[1]}"})
        json = response.json()
        assert response.status_code == 200
        assert json['data'][0][1] == 'Test de positionnement'

    def test_list_subjects(self, log_user):
        response = log_user[0].get(
            f"{API_URL}/subjects",
            headers={"Authorization": f"Bearer {log_user[1]}"})
        json = response.json()
        assert response.status_code == 200
        assert json['data'][0][1] == 'BDD'

    def test_list_questions(self, log_user):
        response = log_user[0].get(
            f"{API_URL}/questions",
            headers={"Authorization": f"Bearer {log_user[1]}"})
        json = response.json()
        assert response.status_code == 200
        assert json['data'][0][1] == 'Que signifie le sigle No-SQL ?'
