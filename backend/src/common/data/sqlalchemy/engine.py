from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.config import settings

engine = create_engine(settings.sqlalchemy_connection_string)
session_maker = sessionmaker(engine)