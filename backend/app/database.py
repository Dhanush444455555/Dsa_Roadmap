import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

logger = logging.getLogger(__name__)

db_url = settings.DATABASE_URL
connect_args = {}

if "sqlite" in db_url:
    connect_args = {"check_same_thread": False}

try:
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        pool_pre_ping=True,
        pool_recycle=3600 if "mysql" in db_url else -1
    )
    # Test connection
    with engine.connect() as conn:
        logger.info(f"Connected to database successfully: {db_url.split('@')[-1] if '@' in db_url else db_url}")
except Exception as e:
    if settings.USE_SQLITE_FALLBACK and "sqlite" not in db_url:
        logger.warning(f"Could not connect to primary database ({e}). Falling back to SQLite: {settings.SQLITE_URL}")
        db_url = settings.SQLITE_URL
        connect_args = {"check_same_thread": False}
        engine = create_engine(db_url, connect_args=connect_args)
    else:
        raise e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
