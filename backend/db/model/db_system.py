from sqlalchemy import Column, String, TIMESTAMP, Integer, func
from db.model import Base


class SystemUser(Base):
    __tablename__ = 'system_user'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username = Column(String(32), nullable=False, unique=True, comment='用户名')
    password = Column(String(64), nullable=False, comment='用户密码')
    email = Column(String(64), nullable=False, unique=True, comment='电子邮件')
    status = Column(Integer, nullable=False, default=1, comment='激活 = 1，注销 = 0')
    created_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment='创建时间')
    update_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now(), comment='更新时间')

    def __repr__(self):
        return f"[SystemUser]==>[id={self.id}, username='{self.username}', email='{self.email}', status={self.status})]"
