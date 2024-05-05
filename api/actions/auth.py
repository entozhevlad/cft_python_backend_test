from sqlalchemy.ext.asyncio import AsyncSession
from db.dals import UserDAL
from db.models import User
from typing import Union
from hashing import Hasher
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")
async def _get_user_by_username_for_auth(username:str, db: AsyncSession):
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_username(
                username=username,
            )
async def authentificate_user(username: str, password: str, db: AsyncSession) -> Union[User, None]:
    user = await _get_user_by_username_for_auth(username=username, db=db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


