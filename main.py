from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.routing import APIRouter
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import settings
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re
from pydantic import BaseModel, EmailStr, validator

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)
asyn_session = sessionmaker(engine, expire_on_commit=False,class_=AsyncSession)


Base =  declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

class UserDAL:
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, username: str, first_name:str, last_name:str, email: str
    ) -> User:
        new_user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

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

app = FastAPI(title="cft-backend")

user_router = APIRouter()


async def _create_new_user(body: UserCreate) -> ShowUser:
    async with asyn_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                username=body.username,
                first_name=body.first_name,
                last_name=body.last_name,
                email=body.email
            )
            return ShowUser(
                user_id=user.user_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                is_active=user.is_active
            )

@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate) -> ShowUser:
    return await _create_new_user(body)

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", porst=8000)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
