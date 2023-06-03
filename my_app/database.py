from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession



DATABASE_URL = "sqlite:///./openai_app.db"

engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False , bind=engine)

Base = declarative_base()