from fastapi import FastAPI, Body, Depends
from app.api.v1.auth import signJWT
from app.api.v1.auth_bearer import JWTBearer
from app.api.v1.questions import Question
from app.api.v1.quizz import Quizz, QuestionSetSchema
from app.api.v1.user import UserSchema, UserLoginSchema, check_user, check_admin

app = FastAPI()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"msg": "Hello World"}


@app.get("/status", tags=["root"])
async def api_status() -> dict:
    return {"status": "OK"}


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }


@app.post("/admin/login", tags=["admin"])
async def admin_login(user: UserLoginSchema = Body(...)):
    if check_admin(user):
        user.is_admin = True
        return signJWT(user.email, user.is_admin)
    return {
        "error": "Wrong login details!"
    }


@app.get("/categories", dependencies=[Depends(JWTBearer())], tags=["questions"])
async def list_categories():
    q = Question()
    return {
        "data": q.get_categories()
    }


@app.get("/subjects", dependencies=[Depends(JWTBearer())], tags=["questions"])
async def list_subjects():
    q = Question()
    return {
        "data": q.get_subjects()
    }


@app.get("/questions", dependencies=[Depends(JWTBearer())], tags=["questions"])
async def list_questions():
    q = Question()
    return {
        "data": q.list_questions()
    }


@app.post("/quizz", dependencies=[Depends(JWTBearer())], tags=["quizz"])
async def generate_quizz(p: QuestionSetSchema):
    q = Quizz()
    quizz = q.get_question_set(p)
    return {
        "data": quizz
    }


@app.post("/questions", dependencies=[Depends(JWTBearer(admin=True))], tags=["questions"])
async def create_question(data: QuestionSetSchema = Body(...)):
    q = Question()
    q.create_question(data)
    return {
        "data": "Question created"
    }
