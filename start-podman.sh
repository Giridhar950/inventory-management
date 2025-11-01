#!/bin/bash

# Shopping Mart System - Podman Compose Quick Start Script

echo "??????????????????????????????????????????????????????????"
echo "?   Shopping Mart Inventory & Billing System            ?"
echo "?   Podman Compose Quick Start                           ?"
echo "??????????????????????????????????????????????????????????"
echo ""

# Check if Podman is installed
if ! command -v podman &> /dev/null; then
    echo "? Podman is not installed. Please install Podman first."
    echo ""
    echo "Installation instructions:"
    echo "  Fedora/RHEL: sudo dnf install podman podman-compose"
    echo "  Ubuntu:      sudo apt-get install podman podman-compose"
    echo "  macOS:       brew install podman podman-compose"
    echo ""
    exit 1
fi

if ! command -v podman-compose &> /dev/null; then
    echo "? Podman Compose is not installed. Please install it first."
    echo ""
    echo "Installation: pip3 install podman-compose"
    echo "Or: sudo dnf install podman-compose (Fedora/RHEL)"
    echo ""
    exit 1
fi

echo "? Podman and Podman Compose are installed"
echo ""

# Create environment files if they don't exist
if [ ! -f backend/.env ]; then
    echo "?? Creating backend/.env file..."
    cp backend/.env.example backend/.env
fi

if [ ! -f frontend/.env ]; then
    echo "?? Creating frontend/.env file..."
    cp frontend/.env.example frontend/.env
fi

echo ""
echo "?? Starting services with Podman Compose..."
podman-compose up -d

echo ""
echo "? Waiting for services to be ready (30 seconds)..."
sleep 30

echo ""
echo "???  Initializing database with sample data..."
podman-compose exec backend python init_db.py

echo ""
echo "??????????????????????????????????????????????????????????"
echo "?   ? Shopping Mart System is ready!                    ?"
echo "??????????????????????????????????????????????????????????"
echo ""
echo "?? Application URLs:"
echo "   Frontend:       http://localhost:3000"
echo "   Backend API:    http://localhost:8000"
echo "   API Docs:       http://localhost:8000/api/docs"
echo ""
echo "?? Default Login Credentials:"
echo "   Admin:"
echo "     Username: admin"
echo "     Password: admin123"
echo ""
echo "   Manager:"
echo "     Username: manager"
echo "     Password: manager123"
echo ""
echo "   Cashier:"
echo "     Username: cashier"
echo "     Password: cashier123"
echo ""
echo "?? Podman Compose Commands:"
echo "   View logs:  podman-compose logs -f"
echo "   Stop:       podman-compose down"
echo "   Restart:    podman-compose restart"
echo "   Status:     podman-compose ps"
echo ""
echo "Happy selling with Podman! ??"
