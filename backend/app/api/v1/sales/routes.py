from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.base import get_db
from app.models.sale import Sale, SaleLineItem
from app.models.inventory import Inventory
from app.models.customer import Customer
from app.models.user import User, UserRole
from app.schemas.sale import SaleCreate, SaleResponse
from app.middleware.auth import get_current_user
import uuid

router = APIRouter()


def generate_receipt_number() -> str:
    """Generate unique receipt number"""
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    unique_id = str(uuid.uuid4())[:8].upper()
    return f"RCP-{timestamp}-{unique_id}"


@router.post("", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new sale transaction"""
    try:
        # Calculate totals
        total_amount = sum(item.quantity * item.unit_price for item in sale_data.line_items)
        discount_amount = sale_data.discount_amount
        tax_amount = (total_amount - discount_amount) * (sale_data.tax_rate / 100)
        final_amount = total_amount - discount_amount + tax_amount
        
        # Create sale
        receipt_number = generate_receipt_number()
        
        db_sale = Sale(
            customer_id=sale_data.customer_id,
            total_amount=total_amount,
            discount_amount=discount_amount,
            tax_amount=tax_amount,
            final_amount=final_amount,
            payment_method=sale_data.payment_method,
            user_id=current_user.user_id,
            store_id=current_user.store_id or 1,  # Default to store 1 if not set
            receipt_number=receipt_number
        )
        
        db.add(db_sale)
        db.flush()  # Get sale_id without committing
        
        # Create line items and update inventory
        for item in sale_data.line_items:
            line_total = item.quantity * item.unit_price - item.discount
            
            line_item = SaleLineItem(
                sale_id=db_sale.sale_id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                discount=item.discount,
                total=line_total
            )
            db.add(line_item)
            
            # Update inventory
            inventory = db.query(Inventory).filter(
                Inventory.product_id == item.product_id,
                Inventory.store_id == current_user.store_id or 1
            ).first()
            
            if inventory:
                if inventory.quantity < item.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Insufficient stock for product ID {item.product_id}"
                    )
                inventory.quantity -= item.quantity
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product ID {item.product_id} not found in inventory"
                )
        
        # Update customer loyalty points and total spent
        if sale_data.customer_id:
            customer = db.query(Customer).filter(Customer.customer_id == sale_data.customer_id).first()
            if customer:
                customer.total_spent += final_amount
                customer.loyalty_points += int(final_amount / 10)  # 1 point per $10 spent
        
        db.commit()
        db.refresh(db_sale)
        
        return db_sale
    
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create sale: {str(e)}"
        )


@router.get("", response_model=List[SaleResponse])
def get_sales(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get sales history with optional date filtering"""
    query = db.query(Sale)
    
    # Filter by store if user is not admin
    if current_user.role != UserRole.ADMIN and current_user.store_id:
        query = query.filter(Sale.store_id == current_user.store_id)
    
    if start_date:
        query = query.filter(Sale.date >= start_date)
    
    if end_date:
        query = query.filter(Sale.date <= end_date)
    
    sales = query.order_by(Sale.date.desc()).offset(skip).limit(limit).all()
    return sales


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single sale by ID"""
    sale = db.query(Sale).filter(Sale.sale_id == sale_id).first()
    
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    
    # Check permissions
    if current_user.role != UserRole.ADMIN and sale.store_id != current_user.store_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return sale
