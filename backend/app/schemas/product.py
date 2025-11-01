from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    sku: str
    barcode: Optional[str] = None
    price: float
    cost: float
    category: Optional[str] = None
    description: Optional[str] = None
    supplier_id: Optional[int] = None
    image_url: Optional[str] = None
    unit_of_measure: str = "pieces"


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    supplier_id: Optional[int] = None
    image_url: Optional[str] = None
    unit_of_measure: Optional[str] = None


class ProductResponse(ProductBase):
    product_id: int
    qr_code: Optional[str]

    class Config:
        from_attributes = True
