from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    weight: int


# class UserCredentials(User):
#    password: str
#    confirm_password: str


class UserRead(User):
    id: int


class UserRegisterCreds(User):
    password: str
    confirm_password: str


class UserCreate(User):
    hashed_password: bytes


class UserLogin(BaseModel):
    username: str
    password: str


class UserToken(BaseModel):
    token: str
    user_id: int
