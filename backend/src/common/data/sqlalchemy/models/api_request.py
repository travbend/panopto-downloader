from common.data.sqlalchemy.models.base import Base
from typing import List
from sqlalchemy import String, Column, BigInteger, Integer, Float, DateTime

class ApiRequest(Base):
    __tablename__ = "api_request"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    request_method = Column(String(8), nullable=False)
    status_code = Column(Integer, nullable=False)
    received_at = Column(DateTime, nullable=False)
    duration_ms = Column(Float, nullable=False)
    url = Column(String(), nullable=False)
