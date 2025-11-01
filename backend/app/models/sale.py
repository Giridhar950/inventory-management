from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .base import Base


class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    UPI = "upi"
    WALLET = "wallet"
    CHECK = "check"


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
    total_amount = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0)
    tax_amount = Column(Float, default=0)
    final_amount = Column(Float, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    store_id = Column(Integer, ForeignKey("stores.store_id"), nullable=False)
    receipt_number = Column(String(50), unique=True, nullable=False, index=True)

    # Relationships
    customer = relationship("Customer", back_populates="sales")
    user = relationship("User", back_populates="sales")
    store = relationship("Store", back_populates="sales")
    line_items = relationship("SaleLineItem", back_populates="sale", cascade="all, delete-orphan")


class SaleLineItem(Base):
    __tablename__ = "sale_line_items"

    line_item_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount = Column(Float, default=0)
    total = Column(Float, nullable=False)

    # Relationships
    sale = relationship("Sale", back_populates="line_items")
    product = relationship("Product", back_populates="sale_line_items")
