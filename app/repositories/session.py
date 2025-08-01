from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Add at the bottom of session.py for debugging
print(f"Database URI: {settings.SQLALCHEMY_DATABASE_URI}")
