from common.data.sqlalchemy.models.base import Base
from sqlalchemy import String, Column, func, BigInteger, DateTime, UUID

class ConvertMp4Task(Base):
    __tablename__ = "convert_mp4_task"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(UUID, unique=True, nullable=False, index=True)
    status = Column(String(16), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), index=True)
