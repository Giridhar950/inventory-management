# Shopping Mart Inventory & Billing System

A comprehensive, production-grade shopping mart inventory management system with integrated Point of Sale (POS) billing, QR code scanning, and real-time analytics. Built with FastAPI (Python) backend and React frontend.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.109-green.svg)

---

## ?? Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Security](#security)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## ? Features

### Core Functionality

#### 1. **Inventory Management**
- Real-time stock tracking across multiple locations
- Low stock alerts with configurable reorder levels
- Expiry date management with FIFO recommendations
- Automated purchase order generation
- Bulk product import via CSV
- QR code generation for all products
- Stock adjustment with audit trail

#### 2. **Point of Sale (POS) System**
- Fast checkout with barcode/QR code scanning
- Multiple payment methods (Cash, Card, UPI, Wallet)
- Real-time cart management
- Discount and promotion application
- Receipt generation (PDF and thermal printer support)
- Return and refund processing
- Customer lookup and loyalty integration

#### 3. **Analytics & Reporting**
- Real-time sales dashboard
- Daily/weekly/monthly sales trends
- Top-selling products analysis
- Inventory turnover metrics
- Customer insights and spending patterns
- Profit/loss analysis
- Custom date range reports
- Export to Excel/PDF

#### 4. **User Management**
- Role-based access control (Admin, Manager, Cashier, Stock Keeper)
- JWT authentication with refresh tokens
- Activity logging and audit trails
- User session management
- Password security with bcrypt hashing

#### 5. **Customer Management**
- Customer database with purchase history
- Loyalty points system
- Personalized offers and promotions
- Customer spending analytics

### Technical Features

- **QR Code Integration**: Automatic QR code generation for products
- **Real-time Updates**: Live inventory and sales data
- **Offline Support**: Works without internet, syncs when online
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Security**: HTTPS, JWT tokens, password hashing, SQL injection prevention
- **Performance**: < 500ms API response time, optimized database queries
- **Scalability**: Horizontal scaling support, Redis caching

---

## ?? Technology Stack

### Backend
- **Framework**: FastAPI 0.109 (Python 3.11)
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Caching**: Redis 7
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt (passlib)
- **QR Code**: qrcode library with PIL
- **API Documentation**: OpenAPI/Swagger (auto-generated)

### Frontend
- **Framework**: React 18.2
- **State Management**: Redux Toolkit
- **UI Library**: Material-UI (MUI) 5
- **Routing**: React Router 6
- **HTTP Client**: Axios
- **Charts**: Recharts
- **QR Scanning**: html5-qrcode
- **Build Tool**: Vite

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Uvicorn (ASGI)
- **Reverse Proxy**: Nginx (production)
- **Version Control**: Git

---

## ?? System Architecture

```
???????????????????????????????????????????????????????????
?                     Frontend (React)                     ?
?  ????????????????????????????????????????????????????? ?
?  ?   POS    ?Inventory ? Products ? Analytics/Reports? ?
?  ????????????????????????????????????????????????????? ?
?                  Redux Store + React Router             ?
???????????????????????????????????????????????????????????
                            ? HTTP/HTTPS (REST API)
???????????????????????????????????????????????????????????
?                  Backend (FastAPI)                       ?
?  ?????????????????????????????????????????????????????? ?
?  ?         API Endpoints (v1)                         ? ?
?  ?  /auth /products /inventory /sales /analytics      ? ?
?  ?????????????????????????????????????????????????????? ?
?  ????????????????????????????????????????????????????  ?
?  ? Auth       ? Business     ? QR Code              ?  ?
?  ? Middleware ? Logic Layer  ? Generation           ?  ?
?  ????????????????????????????????????????????????????  ?
???????????????????????????????????????????????????????????
                            ?
         ???????????????????????????????????????
         ?                                      ?
???????????????????                   ???????????????????
?  PostgreSQL DB  ?                   ?   Redis Cache   ?
?  (Primary Data) ?                   ?  (Sessions)     ?
???????????????????                   ???????????????????
```

---

## ?? Getting Started

### Prerequisites

- **Docker & Docker Compose** (recommended) OR
- **Python 3.11+** and **Node.js 18+**
- **PostgreSQL 15+** (if not using Docker)
- **Redis** (if not using Docker)

### Quick Start with Docker (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd shopping-mart-system
```

2. **Create environment files**
```bash
# Backend
cp backend/.env.example backend/.env

# Frontend
cp frontend/.env.example frontend/.env
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Initialize the database with sample data**
```bash
docker-compose exec backend python init_db.py
```

5. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs

6. **Login with default credentials**
```
Admin:
  Username: admin
  Password: admin123

Manager:
  Username: manager
  Password: manager123

Cashier:
  Username: cashier
  Password: cashier123
```

---

## ?? Installation

### Option 1: Docker (Recommended)

**Advantages**: Easiest setup, no local dependencies, consistent environment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

### Option 2: Manual Installation

#### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

4. **Start PostgreSQL and Redis**
```bash
# Install and start PostgreSQL (port 5432)
# Install and start Redis (port 6379)
```

5. **Initialize database**
```bash
python init_db.py
```

6. **Run the backend**
```bash
uvicorn app.main:app --reload --port 8000
```

#### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env if backend URL is different
```

3. **Run the frontend**
```bash
npm run dev
```

The application will be available at http://localhost:3000

---

## ?? Usage

### For Cashiers (POS Operations)

1. **Login** with cashier credentials
2. Navigate to **POS** module
3. Search products by name, SKU, or scan barcode/QR code
4. Add items to cart, adjust quantities
5. Apply discounts if authorized
6. Select payment method
7. Complete checkout to generate receipt
8. Print or email receipt to customer

### For Store Managers

1. **Dashboard**: View real-time sales, inventory alerts
2. **Inventory**: 
   - Monitor stock levels
   - Adjust inventory with reason codes
   - View low stock and expiry alerts
3. **Products**: Add, edit, or remove products
4. **Sales History**: View past transactions
5. **Analytics**: Generate reports, view trends

### For Administrators

- Full access to all modules
- User management (create/edit/delete users)
- System configuration
- Advanced reporting and analytics
- Multi-store management (if applicable)

---

## ?? API Documentation

### Interactive API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Key Endpoints

#### Authentication
```
POST   /api/v1/auth/login          - User login
POST   /api/v1/auth/register       - Register new user
```

#### Products
```
GET    /api/v1/products            - List all products
POST   /api/v1/products            - Create product
GET    /api/v1/products/{id}       - Get product details
PUT    /api/v1/products/{id}       - Update product
DELETE /api/v1/products/{id}       - Delete product
GET    /api/v1/products/barcode/{barcode} - Find by barcode/QR
```

#### Inventory
```
GET    /api/v1/inventory           - Get inventory
GET    /api/v1/inventory/low-stock - Low stock items
GET    /api/v1/inventory/expiry-risk - Items near expiry
POST   /api/v1/inventory/adjust    - Adjust stock levels
```

#### Sales
```
POST   /api/v1/sales               - Create sale
GET    /api/v1/sales               - List sales
GET    /api/v1/sales/{id}          - Get sale details
```

#### Analytics
```
GET    /api/v1/analytics/sales-summary     - Sales metrics
GET    /api/v1/analytics/top-products      - Best sellers
GET    /api/v1/analytics/inventory-metrics - Inventory stats
GET    /api/v1/analytics/daily-sales       - Daily trends
```

### Authentication

All API requests (except login/register) require a JWT token:

```bash
# Get token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Use token in requests
curl http://localhost:8000/api/v1/products \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## ?? Database Schema

### Core Tables

- **users**: User accounts with roles
- **stores**: Store locations
- **products**: Product catalog
- **suppliers**: Supplier information
- **inventory**: Stock levels per store
- **sales**: Transaction records
- **sale_line_items**: Individual items in sales
- **customers**: Customer profiles
- **transactions**: Stock movements
- **audit_logs**: System activity logs

### Key Relationships

```
stores ??? users (many-to-one)
        ?? inventory (one-to-many)
        ?? sales (one-to-many)

products ??? inventory (one-to-many)
          ?? transactions (one-to-many)
          ?? sale_line_items (one-to-many)
          ?? supplier (many-to-one)

sales ??? sale_line_items (one-to-many)
       ?? customer (many-to-one)
       ?? user (many-to-one)
```

---

## ?? Security

### Implemented Security Measures

1. **Authentication & Authorization**
   - JWT tokens with 30-minute expiry
   - Refresh tokens for extended sessions
   - Role-based access control (RBAC)
   - Password hashing with bcrypt (10 rounds)

2. **API Security**
   - CORS protection
   - SQL injection prevention (SQLAlchemy ORM)
   - Input validation with Pydantic
   - Rate limiting (production)
   - HTTPS enforcement (production)

3. **Data Protection**
   - Password hashing (never stored in plain text)
   - Secure session management
   - Environment variable configuration
   - Database connection encryption

### Security Best Practices

**?? IMPORTANT: Before deploying to production:**

1. Change all default passwords
2. Update `SECRET_KEY` in `.env` to a strong random string
3. Enable HTTPS/TLS
4. Configure firewall rules
5. Enable database encryption at rest
6. Set up regular backups
7. Implement rate limiting
8. Enable audit logging
9. Review and restrict CORS origins
10. Keep dependencies updated

---

## ?? Deployment

### Production Deployment Steps

#### 1. Update Environment Variables

```bash
# backend/.env
DATABASE_URL=postgresql://user:password@prod-host:5432/shopping_mart
REDIS_URL=redis://prod-redis-host:6379/0
SECRET_KEY=generate-a-strong-random-secret-key-here
DEBUG=False
ALLOWED_ORIGINS=https://yourdomain.com

# frontend/.env
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
```

#### 2. Build for Production

```bash
# Frontend
cd frontend
npm run build

# Backend is production-ready as-is
```

#### 3. Deploy with Docker

```bash
# Update docker-compose.yml for production
# Add nginx reverse proxy
docker-compose -f docker-compose.prod.yml up -d
```

#### 4. Cloud Deployment Options

**AWS**:
- EC2 for compute
- RDS for PostgreSQL
- ElastiCache for Redis
- S3 for file storage
- CloudFront for CDN

**Azure**:
- App Service for backend
- Azure Database for PostgreSQL
- Azure Cache for Redis
- Blob Storage
- CDN

**Google Cloud**:
- Cloud Run for containers
- Cloud SQL for PostgreSQL
- Memorystore for Redis
- Cloud Storage
- Cloud CDN

#### 5. Set Up Monitoring

- Configure application logging (Sentry, Datadog)
- Set up uptime monitoring
- Enable database backups
- Configure alerts for critical errors

---

## ?? Testing

### Backend Tests

```bash
cd backend
pytest                          # Run all tests
pytest tests/test_auth.py       # Run specific test file
pytest --cov=app                # With coverage report
```

### Frontend Tests

```bash
cd frontend
npm run test                    # Run tests
npm run test:coverage           # With coverage
```

---

## ?? Performance Optimization

### Backend
- Database connection pooling
- Redis caching for frequently accessed data
- Async operations with FastAPI
- Database query optimization with proper indexes
- Pagination for large datasets

### Frontend
- Code splitting with lazy loading
- Redux state optimization
- Image optimization
- Debouncing for search inputs
- Virtual scrolling for large lists

---

## ?? Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Coding Standards

- **Python**: Follow PEP 8, use type hints
- **JavaScript**: Use ESLint configuration
- **Commit Messages**: Use conventional commits format
- **Documentation**: Update README for new features

---

## ?? License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ?? Authors

- **Development Team** - Initial work

---

## ?? Acknowledgments

- FastAPI for the amazing Python framework
- React and Redux teams for the frontend tools
- Material-UI for the component library
- PostgreSQL and Redis communities

---

## ?? Support

For issues and questions:
- Open an issue on GitHub
- Email: support@shoppingmart.com
- Documentation: http://localhost:8000/api/docs

---

## ?? Roadmap

### Phase 2 Features (Planned)
- [ ] Mobile app (iOS/Android)
- [ ] AI-powered demand forecasting
- [ ] Multi-store synchronization
- [ ] Accounting software integration (QuickBooks, Tally)
- [ ] Email/SMS notifications
- [ ] Advanced reporting (custom reports builder)
- [ ] Barcode label printing
- [ ] Supplier portal
- [ ] Customer mobile app for loyalty program
- [ ] Voice-activated POS

---

## ?? Screenshots

### Dashboard
Real-time overview of sales, inventory, and alerts

### POS System
Fast checkout with barcode scanning

### Inventory Management
Track stock levels and manage products

### Analytics
Comprehensive sales and inventory reports

---

**Made with ?? for retail businesses worldwide**
