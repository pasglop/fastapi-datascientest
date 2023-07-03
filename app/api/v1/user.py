from pydantic import BaseModel, Field, EmailStr

from app.utils import connect, hash_password


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    is_admin: bool = False

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Toto TITI",
                "email": "toto@email.com",
                "password": "weakpassword",
                "is_admin": False
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    is_admin: bool = False

    class Config:
        schema_extra = {
            "example": {
                "email": "toto@email.com",
                "password": "weakpassword",
                "is_admin": False
            }
        }


def check_user(data: UserLoginSchema, is_admin=False):
    conn, cursor = connect()
    cursor.execute(f"select * "
                   f"from main.users "
                   f"where user_email = '{data.email}' "
                   f"AND user_password = '{hash_password(data.password)}' "
                   f"{'AND is_admin = 1' if is_admin else ''}")
    return cursor.fetchone() is not None


def check_admin(data: UserLoginSchema):
    return check_user(data, is_admin=True)
