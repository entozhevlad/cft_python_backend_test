import re
import uuid
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, constr
from datetime import date

LETTER_MATCH_PATTERN_USERNAME = re.compile(r"^[a-zA-Z0-9_]+$")
LETTER_MATCH_PATTERN_NAME = re.compile(r"[а-яA-Яa-zA-z\-]+$")
class TunedModel(BaseModel):
    class Config:
        orm_mode = True

class ShowUser(TunedModel):
    user_id: uuid.UUID
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool

class ShowSalary(TunedModel):
    salary_amount: float
    next_raise_date: Optional[date]

class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    salary_amount: float
    @field_validator("username")
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
    @field_validator("first_name")
    def validate_first_name(cls, values):
        if not LETTER_MATCH_PATTERN_NAME.match(values):
            raise HTTPException(
                status_code=422, detail="Имя должно содержать только символы кириллицы или латницы"
                                )
        return values
    @field_validator("last_name")
    def validate_last_name(cls, values):
        if not LETTER_MATCH_PATTERN_NAME.match(values):
            raise HTTPException(
                status_code=422, detail="Фамилия должна содержать только символы кириллицы или латиницы"
            )
        return values

    @field_validator("salary_amount")
    def validate_salary(cls, value):
        if value <= 0:
            raise ValueError("Сумма должна быть больше нуля")
        if not re.match(r"^\d+(\.\d{1,2})?$", str(value)):
            raise ValueError("Неверный формат зарплаты")
        return value

class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID

class UpdatedUserResponce(BaseModel):
    updated_user_id: uuid.UUID

class UpdateUserRequest(BaseModel):
    username: Optional[constr(min_length=3)]
    first_name: Optional[constr(min_length=3)]
    last_name: Optional[constr(min_length=3)]
    email: Optional[EmailStr]

    @field_validator("username")
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
    @field_validator("first_name")
    def validate_first_name(cls, values):
        if not LETTER_MATCH_PATTERN_NAME.match(values):
            raise HTTPException(
                status_code=422, detail="Имя должно содержать только символы кириллицы"
                                )
        return values
    @field_validator("last_name")
    def validate_last_name(cls, values):
        if not LETTER_MATCH_PATTERN_NAME.match(values):
            raise HTTPException(
                status_code=422, detail="Фамилия должна содержать только символы кириллицы"
            )
        return values

class Token(BaseModel):
    access_token: str
    token_type: str