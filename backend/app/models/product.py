from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    barcode = Column(String(100), unique=True, nullable=True, index=True)
    qr_code = Column(String(255), unique=True, nullable=True, index=True)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    description = Column(Text, nullable=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=True)
    image_url = Column(String(500), nullable=True)
    unit_of_measure = Column(String(50), default="pieces")

    # Relationships
    supplier = relationship("Supplier", back_populates="products")
    inventory = relationship("Inventory", back_populates="product")
    transactions = relationship("Transaction", back_populates="product")
    sale_line_items = relationship("SaleLineItem", back_populates="product")
