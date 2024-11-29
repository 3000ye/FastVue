from sqlalchemy import Column, String, TIMESTAMP, Integer, func
from backend.db.model import Base


class Test(Base):
    __tablename__ = 'tests'  # 这里定义了数据库表名

    id = Column(Integer, primary_key=True, index=True)  # 主键，自动增长
    username = Column(String(32), unique=True, index=True)  # 唯一且索引的字段
    email = Column(String(32), unique=True, index=True)  # 唯一且索引的字段
    full_name = Column(String(32))  # 可选字段
    created_at = Column(TIMESTAMP, server_default=func.now())  # 创建时间，默认值为当前时间
