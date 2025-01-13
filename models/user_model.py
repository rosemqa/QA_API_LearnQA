from pydantic.v1 import BaseModel


class UserLoginModel(BaseModel):
    user_id: int


class DeleteUserModel(BaseModel):
    success: str


class GetAuthUserModel(BaseModel):
    id: str
    username: str
    email: str
    firstName: str
    lastName: str


class GetUserModel(BaseModel):
    username: str


class CreateUserModel(BaseModel):
    id: str


class AuthedModel(BaseModel):
    user_id: int
