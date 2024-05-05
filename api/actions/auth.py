from sqlalchemy.ext.asyncio import AsyncSession
from db.dals import UserDAL
from db.models import User
from typing import Union
from hashing import Hasher
from fastapi.security import OAuth2PasswordBearer
from api.models import ShowSalary

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")
async def _get_user_by_username_for_auth(username:str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_username(
                username=username,
            )
async def _get_user_salary(username: str, session):
    async with session.begin():
        user_dal = UserDAL(session)
        salary = await user_dal.get_salary_and_raise_date_by_username(
            username=username,
        )
        if salary is not None:
            return ShowSalary(
                salary_amount=salary.amount,
                next_raise_date=salary.next_raise_date
            )

async def authentificate_user(username: str, password: str, db: AsyncSession) -> Union[User, None]:
    user = await _get_user_by_username_for_auth(username=username, db=db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


