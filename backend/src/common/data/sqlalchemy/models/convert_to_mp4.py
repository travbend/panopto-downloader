from common.data.sqlalchemy.models.base import Base
from common.data.sqlalchemy.utils import utcnow
from sqlalchemy import String, Column, func, BigInteger, DateTime, UUID, Boolean, Index

class ConvertMp4Task(Base):
    __tablename__ = "convert_mp4_task"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    key = Column(UUID, unique=True, nullable=False, index=True)
    status = Column(String(16), nullable=False)
    created_at = Column(DateTime, server_default=utcnow())
    updated_at = Column(DateTime, server_default=utcnow(), onupdate=utcnow())
    is_cleaned = Column(Boolean, nullable=False, server_default='FALSE')
    
    __table_args__ = (
        Index('idx_convert_mp4_task_cleaned_updated_key', 'is_cleaned', 'updated_at', 'key', unique=True),
    )
