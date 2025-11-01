from pydantic import BaseModel, EmailStr
from typing import Optional


class SupplierBase(BaseModel):
    name: str
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    payment_terms: Optional[str] = None
    location: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    payment_terms: Optional[str] = None
    location: Optional[str] = None


class SupplierResponse(SupplierBase):
    supplier_id: int

    class Config:
        from_attributes = True
