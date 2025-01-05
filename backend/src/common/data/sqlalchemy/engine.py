from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from common.config import settings

engine = create_async_engine(settings.sqlalchemy_connection_string)
sync_maker = sessionmaker(bind=engine)
session_maker = async_sessionmaker(sync_session_class=sync_maker)