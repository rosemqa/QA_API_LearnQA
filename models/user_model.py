from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserLoginModel(BaseModel):
    user_id: int


class LoginHeadersModel(BaseModel):
    token: str = Field(alias='x-csrf-token')


class LoginCookiesModel(BaseModel):
    auth_sid: str


class SuccessModel(BaseModel):
    success: str


class ErrorModel(BaseModel):
    error: str


class GetAuthUserModel(BaseModel):
    id: str
    username: str
    email: str
    firstName: str
    lastName: str


class GetUserModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

    username: str


class CreateUserModel(BaseModel):
    id: str


class AuthedModel(BaseModel):
    user_id: int
