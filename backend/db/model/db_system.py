from sqlalchemy import Column, String, TIMESTAMP, Integer, func
from backend.db.model import Base


class SystemUser(Base):
    __tablename__ = 'system_user'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    status = Column(Integer, nullable=False, default=1, comment='激活 = 1，注销 = 0')
    created_time = Column(TIMESTAMP, nullable=False, server_default=func.now())
    update_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"[SystemUser]==>[id={self.id}, username='{self.username}', email='{self.email}', status={self.status})]"
