from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Scan(Base):
    __tablename__ = "scans"
    id = Column(String, primary_key=True)
    url = Column(String)
    status = Column(String)
    created_at = Column(Integer)

class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True)
    scan_id = Column(String, ForeignKey("scans.id"))
    page_url = Column(String)
    rule_code = Column(String)
    description = Column(Text)
    term_detected = Column(Text, nullable=True)
    suggestion = Column(Text)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
