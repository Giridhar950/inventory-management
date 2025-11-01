from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, index=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"), nullable=False, index=True)
    quantity = Column(Float, nullable=False, default=0)
    reorder_level = Column(Float, nullable=False, default=10)
    expiry_date = Column(Date, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="inventory")
    store = relationship("Store", back_populates="inventory")
