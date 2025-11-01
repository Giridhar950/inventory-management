from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from app.models.base import get_db
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.user import User, UserRole
from app.schemas.inventory import InventoryResponse, InventoryAdjustment, InventoryWithProduct
from app.middleware.auth import get_current_user, require_role

router = APIRouter()


@router.get("", response_model=List[InventoryWithProduct])
def get_inventory(
    store_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get inventory for a store"""
    query = db.query(
        Inventory,
        Product.name.label("product_name"),
        Product.sku.label("product_sku"),
        Product.price.label("product_price")
    ).join(Product, Inventory.product_id == Product.product_id)
    
    if store_id:
        query = query.filter(Inventory.store_id == store_id)
    elif current_user.store_id:
        query = query.filter(Inventory.store_id == current_user.store_id)
    
    results = query.all()
    
    inventory_list = []
    for inv, prod_name, prod_sku, prod_price in results:
        item = InventoryWithProduct(
            inventory_id=inv.inventory_id,
            product_id=inv.product_id,
            store_id=inv.store_id,
            quantity=inv.quantity,
            reorder_level=inv.reorder_level,
            expiry_date=inv.expiry_date,
            last_updated=inv.last_updated,
            product_name=prod_name,
            product_sku=prod_sku,
            product_price=prod_price
        )
        inventory_list.append(item)
    
    return inventory_list


@router.get("/low-stock", response_model=List[InventoryWithProduct])
def get_low_stock_items(
    store_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get items with stock below reorder level"""
    query = db.query(
        Inventory,
        Product.name.label("product_name"),
        Product.sku.label("product_sku"),
        Product.price.label("product_price")
    ).join(Product, Inventory.product_id == Product.product_id).filter(
        Inventory.quantity <= Inventory.reorder_level
    )
    
    if store_id:
        query = query.filter(Inventory.store_id == store_id)
    elif current_user.store_id:
        query = query.filter(Inventory.store_id == current_user.store_id)
    
    results = query.all()
    
    inventory_list = []
    for inv, prod_name, prod_sku, prod_price in results:
        item = InventoryWithProduct(
            inventory_id=inv.inventory_id,
            product_id=inv.product_id,
            store_id=inv.store_id,
            quantity=inv.quantity,
            reorder_level=inv.reorder_level,
            expiry_date=inv.expiry_date,
            last_updated=inv.last_updated,
            product_name=prod_name,
            product_sku=prod_sku,
            product_price=prod_price
        )
        inventory_list.append(item)
    
    return inventory_list


@router.get("/expiry-risk", response_model=List[InventoryWithProduct])
def get_expiry_risk_items(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get items expiring within specified days"""
    expiry_date_threshold = date.today() + timedelta(days=days)
    
    query = db.query(
        Inventory,
        Product.name.label("product_name"),
        Product.sku.label("product_sku"),
        Product.price.label("product_price")
    ).join(Product, Inventory.product_id == Product.product_id).filter(
        Inventory.expiry_date.isnot(None),
        Inventory.expiry_date <= expiry_date_threshold
    )
    
    if current_user.store_id:
        query = query.filter(Inventory.store_id == current_user.store_id)
    
    results = query.all()
    
    inventory_list = []
    for inv, prod_name, prod_sku, prod_price in results:
        item = InventoryWithProduct(
            inventory_id=inv.inventory_id,
            product_id=inv.product_id,
            store_id=inv.store_id,
            quantity=inv.quantity,
            reorder_level=inv.reorder_level,
            expiry_date=inv.expiry_date,
            last_updated=inv.last_updated,
            product_name=prod_name,
            product_sku=prod_sku,
            product_price=prod_price
        )
        inventory_list.append(item)
    
    return inventory_list


@router.post("/adjust", response_model=InventoryResponse)
def adjust_inventory(
    adjustment: InventoryAdjustment,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER, UserRole.STOCK_KEEPER]))
):
    """Adjust inventory quantity"""
    inventory = db.query(Inventory).filter(
        Inventory.product_id == adjustment.product_id,
        Inventory.store_id == adjustment.store_id
    ).first()
    
    if not inventory:
        # Create new inventory record if it doesn't exist
        inventory = Inventory(
            product_id=adjustment.product_id,
            store_id=adjustment.store_id,
            quantity=adjustment.quantity_change
        )
        db.add(inventory)
    else:
        inventory.quantity += adjustment.quantity_change
        
        # Ensure quantity doesn't go negative
        if inventory.quantity < 0:
            inventory.quantity = 0
    
    db.commit()
    db.refresh(inventory)
    
    return inventory
