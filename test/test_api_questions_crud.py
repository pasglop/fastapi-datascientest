from fastapi.testclient import TestClient
from app.api.v1.api import app
from app.api.v1.quizz import Question, QuestionSchema

client = TestClient(app)

API_URL = "http://localhost:8081"


class TestApiQuestionCrud:
    def test_list_categories(self):
        response = client.get(f"{API_URL}/categories")
        json = response.json()
        assert response.status_code == 200
        assert json['data'][0][1] == 'Test de positionnement'

    def test_list_subjects(self):
        response = client.get(f"{API_URL}/subjects")
        json = response.json()
        assert response.status_code == 200
        assert json['data'][0][1] == 'BDD'

    def test_list_questions(self):
        response = client.get(f"{API_URL}/questions")
        json = response.json()
        assert response.status_code == 200
        assert json['data'][0][1] == 'Que signifie le sigle No-SQL ?'

