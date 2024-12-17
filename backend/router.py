from fastapi import APIRouter
from api.routers import hello, system_user, system_auth


api_router = APIRouter()
api_router.include_router(hello.router, prefix="/hello", tags=["Test Hello World"])
api_router.include_router(system_auth.router, prefix="/system_auth", tags=["System Auth"])
api_router.include_router(system_user.router, prefix="/system_user", tags=["System User"])
