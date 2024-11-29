import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings
from api.main import api_router


def create() -> FastAPI:
    application = FastAPI(title="FastVue", docs_url="/docs")
    application.debug = True

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有来源
        allow_methods=["*"],  # 允许所有方法
        allow_headers=["*"],  # 允许所有请求头
        allow_credentials=True,
    )

    application.include_router(api_router, prefix="/api")

    return application


# reload 模式
app = create()
if __name__ == "__main__":
    uvicorn.run(app="run:app", host="0.0.0.0", port=settings.BACKEND_PORT, reload=True)
