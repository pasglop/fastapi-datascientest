from fastapi import FastAPI, Body
from app.api.v1.auth import signJWT
from app.api.v1.questions import Question
from app.api.v1.user import UserSchema, UserLoginSchema, check_user, check_admin

app = FastAPI()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"msg": "Hello World"}


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
        return signJWT(user.email, user.is_admin)
    return {
        "error": "Wrong login details!"
    }


@app.get("/categories", tags=["questions"])
async def list_categories():
    q = Question()
    return {
        "data": q.get_categories()
    }

@app.get("/subjects", tags=["questions"])
async def list_subjects():
    q = Question()
    return {
        "data": q.get_subjects()
    }


@app.get("/questions", tags=["questions"])
async def list_questions():
    q = Question()
    return {
        "data": q.list_questions()
    }
