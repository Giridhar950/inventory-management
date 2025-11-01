from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.sale import PaymentMethod


class SaleLineItemCreate(BaseModel):
    product_id: int
    quantity: float
    unit_price: float
    discount: float = 0


class SaleLineItemResponse(SaleLineItemCreate):
    line_item_id: int
    total: float

    class Config:
        from_attributes = True


class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    payment_method: PaymentMethod
    line_items: List[SaleLineItemCreate]
    discount_amount: float = 0
    tax_rate: float = 0  # Tax rate as percentage


class SaleResponse(BaseModel):
    sale_id: int
    customer_id: Optional[int]
    total_amount: float
    discount_amount: float
    tax_amount: float
    final_amount: float
    payment_method: PaymentMethod
    date: datetime
    user_id: int
    store_id: int
    receipt_number: str
    line_items: List[SaleLineItemResponse]

    class Config:
        from_attributes = True
