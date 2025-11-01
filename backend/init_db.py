"""
Initialize the database with sample data
Run this script after starting the application to create initial users and data
"""
from sqlalchemy.orm import Session
from app.models.base import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.store import Store
from app.models.product import Product
from app.models.supplier import Supplier
from app.models.inventory import Inventory
from app.utils.auth import get_password_hash
from app.utils.qr_code import generate_qr_code_data

def init_db():
    """Initialize database with sample data"""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already initialized")
            return
        
        # Create default store
        store = Store(
            name="Main Store",
            location="123 Main Street",
        )
        db.add(store)
        db.flush()
        
        # Create admin user
        admin = User(
            username="admin",
            email="admin@shoppingmart.com",
            password_hash=get_password_hash("admin123"),
            role=UserRole.ADMIN,
            store_id=store.store_id
        )
        db.add(admin)
        
        # Create manager user
        manager = User(
            username="manager",
            email="manager@shoppingmart.com",
            password_hash=get_password_hash("manager123"),
            role=UserRole.MANAGER,
            store_id=store.store_id
        )
        db.add(manager)
        
        # Create cashier user
        cashier = User(
            username="cashier",
            email="cashier@shoppingmart.com",
            password_hash=get_password_hash("cashier123"),
            role=UserRole.CASHIER,
            store_id=store.store_id
        )
        db.add(cashier)
        
        # Create sample supplier
        supplier = Supplier(
            name="ABC Distributors",
            contact_name="John Doe",
            phone="555-1234",
            email="contact@abcdist.com",
            payment_terms="Net 30"
        )
        db.add(supplier)
        db.flush()
        
        # Create sample products
        products = [
            {
                "name": "Coca Cola 330ml",
                "sku": "COCA-330",
                "barcode": "1234567890123",
                "price": 1.99,
                "cost": 1.20,
                "category": "Beverages",
                "supplier_id": supplier.supplier_id,
            },
            {
                "name": "Lay's Chips Original",
                "sku": "LAYS-ORG",
                "barcode": "2345678901234",
                "price": 2.49,
                "cost": 1.50,
                "category": "Snacks",
                "supplier_id": supplier.supplier_id,
            },
            {
                "name": "Fresh Milk 1L",
                "sku": "MILK-1L",
                "barcode": "3456789012345",
                "price": 3.99,
                "cost": 2.80,
                "category": "Dairy",
                "supplier_id": supplier.supplier_id,
            },
            {
                "name": "White Bread",
                "sku": "BREAD-WHT",
                "barcode": "4567890123456",
                "price": 2.99,
                "cost": 1.80,
                "category": "Bakery",
                "supplier_id": supplier.supplier_id,
            },
            {
                "name": "Bananas per kg",
                "sku": "BAN-KG",
                "barcode": "5678901234567",
                "price": 1.49,
                "cost": 0.80,
                "category": "Fruits",
                "supplier_id": supplier.supplier_id,
                "unit_of_measure": "kg",
            },
        ]
        
        for prod_data in products:
            product = Product(**prod_data)
            db.add(product)
            db.flush()
            
            # Generate QR code
            product.qr_code = generate_qr_code_data(
                product.product_id,
                product.name,
                product.sku
            )
            
            # Add inventory
            inventory = Inventory(
                product_id=product.product_id,
                store_id=store.store_id,
                quantity=100,
                reorder_level=20
            )
            db.add(inventory)
        
        db.commit()
        print("Database initialized successfully!")
        print("\nDefault users created:")
        print("- Admin: username='admin', password='admin123'")
        print("- Manager: username='manager', password='manager123'")
        print("- Cashier: username='cashier', password='cashier123'")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
