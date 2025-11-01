from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models.base import engine, Base
from app.api.v1.auth import routes as auth_routes
from app.api.v1.products import routes as product_routes
from app.api.v1.inventory import routes as inventory_routes
from app.api.v1.sales import routes as sales_routes
from app.api.v1.customers import routes as customer_routes
from app.api.v1.users import routes as user_routes
from app.api.v1.analytics import routes as analytics_routes

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Advanced Shopping Mart Inventory & Billing System API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(product_routes.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(inventory_routes.router, prefix="/api/v1/inventory", tags=["Inventory"])
app.include_router(sales_routes.router, prefix="/api/v1/sales", tags=["Sales"])
app.include_router(customer_routes.router, prefix="/api/v1/customers", tags=["Customers"])
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(analytics_routes.router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.get("/")
def root():
    return {
        "message": "Shopping Mart Inventory & Billing System API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
