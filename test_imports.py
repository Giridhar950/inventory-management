#!/usr/bin/env python3
"""
Test script to verify all imports work correctly
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("Testing Python imports...")
print("=" * 60)

try:
    print("? Testing config...")
    from app.config import settings
    print(f"  App Name: {settings.APP_NAME}")
    
    print("\n? Testing models...")
    from app.models.base import Base, engine
    from app.models.user import User, UserRole
    from app.models.store import Store
    from app.models.product import Product
    from app.models.supplier import Supplier
    from app.models.inventory import Inventory
    from app.models.transaction import Transaction, TransactionType
    from app.models.sale import Sale, SaleLineItem, PaymentMethod
    from app.models.customer import Customer
    from app.models.audit_log import AuditLog
    print("  All models imported successfully")
    
    print("\n? Testing schemas...")
    from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
    from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
    from app.schemas.inventory import InventoryResponse, InventoryAdjustment
    from app.schemas.sale import SaleCreate, SaleResponse
    from app.schemas.customer import CustomerCreate, CustomerResponse
    from app.schemas.supplier import SupplierCreate, SupplierResponse
    print("  All schemas imported successfully")
    
    print("\n? Testing utilities...")
    from app.utils.auth import verify_password, get_password_hash
    from app.utils.qr_code import generate_qr_code_data, decode_qr_code
    print("  All utilities imported successfully")
    
    print("\n? Testing middleware...")
    from app.middleware.auth import get_current_user, require_role
    print("  All middleware imported successfully")
    
    print("\n? Testing main app...")
    from app.main import app
    print("  Main app imported successfully")
    
    print("\n" + "=" * 60)
    print("? ALL IMPORTS SUCCESSFUL!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n? ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
