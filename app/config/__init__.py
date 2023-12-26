import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()


class Base(DeclarativeBase):
    pass


class Engine:
    __engine = None

    def __new__(cls) -> "Engine":
        if cls.__engine is not None:
            return cls.__engine

        database_url = "mysql+pymysql://{}:{}@{}:{}/{}".format(
            os.getenv("DB_USER"),
            os.getenv("DB_PASS"),
            os.getenv("DB_HOST"),
            os.getenv("DB_PORT"),
            os.getenv("DB_NAME")
        )
        cls.__engine = create_engine(database_url)
        Base.metadata.create_all(bind=cls.__engine)
        return cls.__engine


class SessionLocal(sessionmaker):
    def __new__(cls) -> Session:
        session = sessionmaker(autoflush=False, bind=Engine())
        return session()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    except Exception as _:
        db.rollback()
    finally:
        db.close()
