from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Text, DateTime, create_engine, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = "data/app.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=True)
    brand = Column(String(256), nullable=True)
    barcode = Column(String(64), unique=True, nullable=True)
    printed_weight_g = Column(Float, nullable=True)
    volume_ml = Column(Float, nullable=True)
    pack_count = Column(Integer, nullable=True)
    category_text = Column(String(256), nullable=True)
    image_path = Column(String(512), nullable=False)
    image_phash = Column(String(64), nullable=True, index=True)
    raw_ocr_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ProductKey(Base):
    __tablename__ = "product_keys"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False)
    norm_key = Column(String(512), nullable=False, unique=True)  # e.g. "brand:name" normalized

def init_db():
    Base.metadata.create_all(bind=engine)
