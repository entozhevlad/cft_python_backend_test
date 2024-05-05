from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from api.handlers import user_router
from api.login_handler import login_router


app = FastAPI(title="cft-backend")


main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])


app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

