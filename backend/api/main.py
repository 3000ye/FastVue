from fastapi import APIRouter
from backend.api.routes import hello, test


api_router = APIRouter()
api_router.include_router(hello.router, prefix="/hello", tags=["Test Hello World"])
api_router.include_router(test.router, prefix="/test", tags=["Test"])
