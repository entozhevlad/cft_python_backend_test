from api.models import UserCreate, ShowUser, ShowSalary
from db.dals import UserDAL, SalaryDAL
from typing import Union
from uuid import UUID
from hashing import Hasher
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError 
from fastapi import HTTPException


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    try:
        async with session.begin():
            user_dal = UserDAL(session)
            salary_dal = SalaryDAL(session)

            # Попытка создания пользователя
            user = await user_dal.create_user(
                username=body.username,
                first_name=body.first_name,
                last_name=body.last_name,
                email=body.email,
                hashed_password=Hasher.get_password_hash(body.password),
            )

            # Создание записи о зарплате
            await salary_dal.create_salary(
                user_id=user.user_id,
                salary_amount=body.salary_amount,
                next_raise_date=date.today() + timedelta(days=365)
            )

            return ShowUser(
                user_id=user.user_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_active=user.is_active
            )

    except IntegrityError as e:
        # Откат транзакции в случае ошибки
        await session.rollback()

        # Проверяем, связана ли ошибка с уникальностью email
        if isinstance(e.orig, UniqueViolationError) and 'users_email_key' in str(e.orig):
            raise HTTPException(
                status_code=409,
                detail="Email уже зарегистрирован. Пожалуйста, используйте другой email."
            )

        # Обработка других ошибок базы данных
        raise HTTPException(
            status_code=500,
            detail="Произошла ошибка при создании пользователя."
        )

async def _update_user(updated_user_params: dict, user_id: UUID, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id,
            **updated_user_params
        )
        return updated_user_id

async def _delete_user(user_id, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id,
        )
        return deleted_user_id
async def _get_user_by_id(user_id, session) -> Union[ShowUser, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return ShowUser(
                user_id=user.user_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_active=user.is_active,
            )

