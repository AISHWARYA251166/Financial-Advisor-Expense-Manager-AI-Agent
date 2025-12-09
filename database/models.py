# database/models.py
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False, default=0.0)
    merchant = Column(String(256), nullable=True)
    category = Column(String(128), nullable=True, index=True)
    date = Column(String(32), nullable=True, index=True)  # store as YYYY-MM-DD text
    paymentMethod = Column(String(64), nullable=True)
    source = Column(String(64), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class GuruDoc(Base):
    __tablename__ = "guru_docs"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(256), nullable=False)
    content = Column(Text, nullable=True)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(128), nullable=False, unique=True)
    amount = Column(Float, nullable=False, default=0.0)
