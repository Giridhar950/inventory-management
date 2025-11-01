from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.models.base import get_db
from app.models.sale import Sale, SaleLineItem
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.customer import Customer
from app.models.user import User, UserRole
from app.middleware.auth import get_current_user, require_role

router = APIRouter()


@router.get("/sales-summary")
def get_sales_summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get sales summary statistics"""
    query = db.query(Sale)
    
    # Default to last 30 days if no dates provided
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=30)
    if not end_date:
        end_date = datetime.utcnow()
    
    query = query.filter(Sale.date >= start_date, Sale.date <= end_date)
    
    # Filter by store if not admin
    if current_user.role != UserRole.ADMIN and current_user.store_id:
        query = query.filter(Sale.store_id == current_user.store_id)
    
    sales = query.all()
    
    total_sales = sum(sale.final_amount for sale in sales)
    total_transactions = len(sales)
    avg_transaction_value = total_sales / total_transactions if total_transactions > 0 else 0
    total_discount = sum(sale.discount_amount for sale in sales)
    
    return {
        "total_sales": round(total_sales, 2),
        "total_transactions": total_transactions,
        "average_transaction_value": round(avg_transaction_value, 2),
        "total_discount": round(total_discount, 2),
        "period": {
            "start_date": start_date,
            "end_date": end_date
        }
    }


@router.get("/top-products")
def get_top_products(
    limit: int = 10,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get top selling products"""
    query = db.query(
        Product.product_id,
        Product.name,
        Product.sku,
        func.sum(SaleLineItem.quantity).label("total_quantity"),
        func.sum(SaleLineItem.total).label("total_revenue")
    ).join(SaleLineItem, Product.product_id == SaleLineItem.product_id
    ).join(Sale, SaleLineItem.sale_id == Sale.sale_id)
    
    if start_date:
        query = query.filter(Sale.date >= start_date)
    if end_date:
        query = query.filter(Sale.date <= end_date)
    
    if current_user.role != UserRole.ADMIN and current_user.store_id:
        query = query.filter(Sale.store_id == current_user.store_id)
    
    top_products = query.group_by(
        Product.product_id, Product.name, Product.sku
    ).order_by(desc("total_quantity")).limit(limit).all()
    
    return [
        {
            "product_id": p.product_id,
            "product_name": p.name,
            "sku": p.sku,
            "total_quantity_sold": float(p.total_quantity),
            "total_revenue": round(float(p.total_revenue), 2)
        }
        for p in top_products
    ]


@router.get("/inventory-metrics")
def get_inventory_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get inventory metrics"""
    query = db.query(Inventory).join(Product, Inventory.product_id == Product.product_id)
    
    if current_user.role != UserRole.ADMIN and current_user.store_id:
        query = query.filter(Inventory.store_id == current_user.store_id)
    
    inventory_items = query.all()
    
    total_items = len(inventory_items)
    low_stock_count = sum(1 for item in inventory_items if item.quantity <= item.reorder_level)
    out_of_stock_count = sum(1 for item in inventory_items if item.quantity == 0)
    
    # Calculate total inventory value
    total_value = 0
    for item in inventory_items:
        product = db.query(Product).filter(Product.product_id == item.product_id).first()
        if product:
            total_value += item.quantity * product.cost
    
    return {
        "total_items": total_items,
        "low_stock_items": low_stock_count,
        "out_of_stock_items": out_of_stock_count,
        "total_inventory_value": round(total_value, 2)
    }


@router.get("/daily-sales")
def get_daily_sales(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get daily sales for the last N days"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(
        func.date(Sale.date).label("sale_date"),
        func.sum(Sale.final_amount).label("total_sales"),
        func.count(Sale.sale_id).label("transaction_count")
    ).filter(Sale.date >= start_date)
    
    if current_user.role != UserRole.ADMIN and current_user.store_id:
        query = query.filter(Sale.store_id == current_user.store_id)
    
    daily_sales = query.group_by(func.date(Sale.date)).order_by("sale_date").all()
    
    return [
        {
            "date": str(day.sale_date),
            "total_sales": round(float(day.total_sales), 2),
            "transaction_count": day.transaction_count
        }
        for day in daily_sales
    ]


@router.get("/customer-insights")
def get_customer_insights(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.MANAGER]))
):
    """Get top customers by spending"""
    top_customers = db.query(Customer).order_by(
        desc(Customer.total_spent)
    ).limit(limit).all()
    
    return [
        {
            "customer_id": c.customer_id,
            "name": c.name,
            "phone": c.phone,
            "total_spent": round(c.total_spent, 2),
            "loyalty_points": c.loyalty_points
        }
        for c in top_customers
    ]
