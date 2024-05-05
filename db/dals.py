from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_, select
from typing import Union
from uuid import UUID
from db.models import User, Salary
from datetime import date
class UserDAL:
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, username: str, first_name:str, last_name:str, email: str, hashed_password: str
    ) -> User:
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            hashed_password=hashed_password
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = update(User).\
            where(and_(User.user_id == user_id, User.is_active == True)).\
            values(is_active=False).returning(User.user_id)
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.user_id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self,user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = update(User). \
            where(and_(User.user_id == user_id, User.is_active == True)). \
            values(kwargs). \
            returning(User.user_id)
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]
    async def get_user_by_username(self, username: str) -> Union[User, None]:
        query = select(User).where(User.username == username)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_salary_and_raise_date_by_username(
            self, username: str,
    ) -> Union[Salary, None]:
        query = select(Salary).join(User).where(User.username == username)
        res = await self.db_session.execute(query)
        salary_row = res.fetchone()
        if salary_row is not None:
            return salary_row[0]

class SalaryDAL:
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def create_salary(
            self, user_id: UUID, salary_amount: float, next_raise_date: date
    ) -> Salary:
        new_salary = Salary(
            user_id=user_id,
            amount=salary_amount,
            next_raise_date=next_raise_date
        )
        self.db_session.add(new_salary)
        await self.db_session.flush()
        return new_salary

