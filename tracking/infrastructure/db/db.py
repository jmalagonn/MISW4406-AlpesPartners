from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import settings
from .db_models import Base

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
)

@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def init_db():
    # Crear esquemas necesarios para CQRS
    with engine.connect() as connection:
        from sqlalchemy import text
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS read;"))
        connection.execute(text("GRANT ALL PRIVILEGES ON SCHEMA read TO CURRENT_USER;"))
        connection.commit()
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
