from pydantic import BaseModel, Field, EmailStr

from ..utils import connect, hash_password


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    is_admin: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "alice",
                "email": "alice@email.com",
                "password": "wonderland"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    is_admin: bool = False # This field is not required

    class Config:
        schema_extra = {
            "example": {
                "email": "admin@email.com",
                "password": "4dm1N"
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
