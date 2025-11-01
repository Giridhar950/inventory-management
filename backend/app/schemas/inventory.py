from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class InventoryBase(BaseModel):
    product_id: int
    store_id: int
    quantity: float
    reorder_level: float = 10
    expiry_date: Optional[date] = None


class InventoryAdjustment(BaseModel):
    product_id: int
    store_id: int
    quantity_change: float
    reason: str
    notes: Optional[str] = None


class InventoryResponse(InventoryBase):
    inventory_id: int
    last_updated: datetime

    class Config:
        from_attributes = True


class InventoryWithProduct(InventoryResponse):
    product_name: str
    product_sku: str
    product_price: float
