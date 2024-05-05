from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import Token
from db.models import User
from db.session import get_db
from datetime import timedelta
import settings
from jose import jwt, JWTError
from security import create_access_token
login_router = APIRouter()
from api.actions.auth import authentificate_user, _get_user_by_username_for_auth, oauth2_scheme


login_router = APIRouter()

@login_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await authentificate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNATHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub":user.username, "other_custom_data":[1,2,3,4]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type" : "bearer"}



async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentinals_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Не удалось проверить данные",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        print("username/email extracted is ", username)
        if username is None:
            raise  credentinals_exception
    except JWTError:
        raise credentinals_exception
    user = await _get_user_by_username_for_auth(username=username, db=db)
    if user is None:
        raise credentinals_exception
    return user

@login_router.get("/test_auth_endpoint")
async def sample_endpoint_under_jwt(current_user: User = Depends(get_current_user_from_token),):
    return {"Success": True, "current_user": current_user}
