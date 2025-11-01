from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    contact_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    payment_terms = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)

    # Relationships
    products = relationship("Product", back_populates="supplier")
