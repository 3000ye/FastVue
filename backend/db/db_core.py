from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.config import settings
from db.model import Base


class DbSession:
    def __init__(self, url) -> None:
        # 创建引擎和会话
        _engine = create_engine(url, pool_size=100, pool_recycle=7200)
        _Session = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
        # 创建表
        Base.metadata.create_all(_engine)

        self.session = _Session()

    def __enter__(self):
        return self.session

    def __exit__(self, *args, **kwargs):
        self.session.close()


def get_db() -> Session:
    with DbSession(settings.MYSQL_URL) as session:
        try:
            yield session
        finally:
            session.close()
