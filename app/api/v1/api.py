from urllib.request import Request

from fastapi import FastAPI, Body, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from .auth import signJWT
from .auth_bearer import JWTBearer
from .questions import Question
from .quizz import Quizz
from .models import QuestionSchema, QuestionSetSchema, CreateQuestionSchema
from .user import UserLoginSchema, check_user, check_admin

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


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
async def create_question(data: CreateQuestionSchema = Body(...)):
    q = Question()
    q.create_question(data)
    return {
        "data": "Question created"
    }


@app.delete("/questions/{id}", dependencies=[Depends(JWTBearer(admin=True))], tags=["questions"])
async def delete_question(id: int):
    q = Question()
    q.delete_question(id)
    q.delete_answers(id)
    return {
        "data": "Question deleted"
    }
