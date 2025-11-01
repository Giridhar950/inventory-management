from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .base import Base


class TransactionType(str, enum.Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    TRANSFER = "transfer"


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    type = Column(SQLEnum(TransactionType), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    notes = Column(Text, nullable=True)
    reference_id = Column(Integer, nullable=True)  # Reference to sale_id or other transaction

    # Relationships
    product = relationship("Product", back_populates="transactions")
