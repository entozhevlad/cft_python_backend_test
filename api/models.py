import re
import uuid
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr

LETTER_MATCH_PATTERN_USERNAME = re.compile(r"^[a-zA-Z0-9_]+$")
LETTER_MATCH_PATTERN_NAME = re.compile(r"[а-яA-Яa-zA-z\-]+$")
class TundeModel(BaseModel):
    class Config:
        orm_mode = True

class ShowUser(TundeModel):
    user_id: uuid.UUID
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str

    @validator("username")
    def validate_username(cls, values):
        if not LETTER_MATCH_PATTERN_USERNAME.match(values):
            raise HTTPException(
                status_code=422, detail="Имя пользователя должно содержать только символы латинского алфавита"
            )

        if len(values) < 3:
            raise HTTPException(
                status_code=422, detail="Имя пользователя должно содержать не менее 3 символов"
                                )

        if values.isdigit():
            raise HTTPException(
                status_code=422, detail="Имя пользователя не должно содержать только цифры"
            )
        return values
    @validator("first_name")
    def validate_first_name(cls, values):
        if not LETTER_MATCH_PATTERN_NAME.match(values):
            raise HTTPException(
                status_code=422, detail="Имя должно содержать только символы кириллицы"
                                )
        return values
    @validator("last_name")
    def validate_last_name(cls, values):
        if not LETTER_MATCH_PATTERN_NAME.match(values):
            raise HTTPException(
                status_code=422, detail="Фамилия должна содержать только символы кириллицы"
            )
        return values

class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID

class UpdatedUserResponce(BaseModel):
    updated_user_id: uuid.UUID

class UpdateUserRequest(BaseModel):
    username: Optional[constr(min_length=3)]
    first_name: Optional[constr(min_length=3)]
    last_name: Optional[constr(min_length=3)]
    email: Optional[EmailStr]

    @validator("username")
    def validate_username(cls, values):
        if not LETTER_MATCH_PATTERN_USERNAME.match(values):
            raise HTTPException(
                status_code=422, detail="Имя пользователя должно содержать только символы латинского алфавита"
            )

        if len(values) < 3:
            raise HTTPException(
                status_code=422, detail="Имя пользователя должно содержать не менее 3 символов"
                                )
 
        if values.isdigit():
            raise HTTPException(
                status_code=422, detail="Имя пользователя не должно содержать только цифры"
            )
        return values
    @validator("first_name")
    def validate_first_name(cls, values):
        if not LETTER_MATCH_PATTERN_NAME.match(values):
            raise HTTPException(
                status_code=422, detail="Имя должно содержать только символы кириллицы"
                                )
        return values
    @validator("last_name")
    def validate_last_name(cls, values):
        if not LETTER_MATCH_PATTERN_NAME.match(values):
            raise HTTPException(
                status_code=422, detail="Фамилия должна содержать только символы кириллицы"
            )
        return values

class Token(BaseModel):
    access_token: str
    token_type: str