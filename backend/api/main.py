from fastapi import APIRouter
from backend.api.routes import hello, system_user


api_router = APIRouter()
api_router.include_router(hello.router, prefix="/hello", tags=["Test Hello World"])
api_router.include_router(system_user.router, prefix="/system_user", tags=["System User"])