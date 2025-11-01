from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(100), nullable=True)
    loyalty_points = Column(Float, default=0)
    total_spent = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sales = relationship("Sale", back_populates="customer")
