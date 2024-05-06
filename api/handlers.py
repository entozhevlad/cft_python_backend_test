from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from api.models import UserCreate, ShowUser, DeleteUserResponse, UpdatedUserResponce, UpdateUserRequest, ShowSalary
from db.session import get_db
from uuid import UUID
from logging import getLogger
from api.actions.user import _create_new_user, _update_user, _delete_user, _get_user_by_id

logger = getLogger(__name__)

user_router = APIRouter()

@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Ошибка базы данных: {err}")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с id {user_id} не найден или уже не активен.")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)

@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с id {user_id} не найден.")
    return user

@user_router.patch("/", response_model=UpdatedUserResponce)
async def update_user_by_id(user_id: UUID, body: UpdateUserRequest, db: AsyncSession = Depends(get_db)) \
        -> UpdatedUserResponce:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(status_code=400, detail="Не переданы параметры для обновления.")
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"Пользователь с id {user_id} не найден.")
    try:
        updated_user_id = await _update_user(updated_user_params=updated_user_params, user_id=user_id, session=db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Ошибка базы данных: {err}")

    return UpdatedUserResponce(updated_user_id=updated_user_id)


