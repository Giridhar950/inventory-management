from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    name: str
    phone: str
    email: Optional[EmailStr] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class CustomerResponse(CustomerBase):
    customer_id: int
    loyalty_points: float
    total_spent: float
    created_at: datetime

    class Config:
        from_attributes = True
