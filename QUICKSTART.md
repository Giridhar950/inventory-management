# Quick Start Guide

Get the Shopping Mart System running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- 4GB RAM minimum
- 5GB free disk space

## Steps

### 1. Clone and Navigate

```bash
git clone <repository-url>
cd shopping-mart-system
```

### 2. Run Quick Start Script

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows (PowerShell):**
```powershell
docker-compose up -d
docker-compose exec backend python init_db.py
```

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/api/docs
- **Backend**: http://localhost:8000

### 4. Login

Use any of these credentials:

**Admin Account:**
- Username: `admin`
- Password: `admin123`
- Full system access

**Manager Account:**
- Username: `manager`
- Password: `manager123`
- Inventory, products, sales, analytics

**Cashier Account:**
- Username: `cashier`
- Password: `cashier123`
- POS operations only

## What's Included?

The database is pre-populated with:
- 3 user accounts (admin, manager, cashier)
- 1 store
- 5 sample products with inventory
- 1 supplier
- QR codes for all products

## First Steps

### As a Cashier:
1. Login and go to **POS**
2. Search for "Coca Cola"
3. Add to cart
4. Complete checkout

### As a Manager:
1. Login and view **Dashboard**
2. Check **Inventory** for low stock items
3. Add a new product in **Products**
4. View **Analytics** for insights

### As an Admin:
1. All features available
2. Create new users in **Users** section
3. Configure system settings
4. View audit logs

## Common Commands

```bash
# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Restart services
docker-compose restart

# Rebuild after code changes
docker-compose up -d --build

# Access backend container
docker-compose exec backend bash

# Access database
docker-compose exec postgres psql -U postgres -d shopping_mart
```

## Troubleshooting

### Port Already in Use?

Edit `docker-compose.yml` to change ports:
- Frontend: Change `3000:3000` to `3001:3000`
- Backend: Change `8000:8000` to `8001:8000`

### Database Connection Error?

```bash
docker-compose down
docker-compose up -d
# Wait 10 seconds
docker-compose exec backend python init_db.py
```

### Can't Login?

Reset the database:
```bash
docker-compose down -v
docker-compose up -d
docker-compose exec backend python init_db.py
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [API Documentation](http://localhost:8000/api/docs)
- Customize `.env` files for your environment
- Add your own products and start selling!

## Need Help?

- Check the [README.md](README.md) for comprehensive documentation
- Open an issue on GitHub
- Review API docs at http://localhost:8000/api/docs

---

**Ready to go! Start exploring your new Shopping Mart System! ??**
