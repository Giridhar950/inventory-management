# Podman Compose Setup Guide

This guide shows how to run the Shopping Mart System using **Podman** and **Podman Compose** instead of Docker.

---

## ?? Podman vs Docker

Podman is a daemonless container engine that's fully compatible with Docker. The `docker-compose.yml` file works with `podman-compose` with minimal changes.

---

## ?? Prerequisites

### Install Podman and Podman Compose

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install podman podman-compose
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install podman podman-compose
```

**Arch Linux:**
```bash
sudo pacman -S podman podman-compose
```

**macOS:**
```bash
brew install podman podman-compose
```

---

## ?? Quick Start with Podman Compose

### Option 1: Using Podman Compose (Recommended)

```bash
# 1. Create environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. Start all services
podman-compose up -d

# 3. Wait for services to be ready (30 seconds)
sleep 30

# 4. Initialize database with sample data
podman-compose exec backend python init_db.py

# 5. Access the application
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Option 2: Using Podman with Docker Compose Alias

If you prefer using the `docker-compose` command syntax:

```bash
# Create an alias
alias docker-compose='podman-compose'

# Now you can use docker-compose commands
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## ?? Podman-Specific Considerations

### 1. **Rootless Mode (Recommended)**

Podman runs in rootless mode by default, which is more secure:

```bash
# All commands run as your user (no sudo needed)
podman-compose up -d
```

### 2. **SELinux Considerations**

If you're on Fedora/RHEL with SELinux enabled:

```bash
# Add :Z flag to volumes in docker-compose.yml if needed
# Already handled in the compose file
```

### 3. **Port Binding**

For rootless Podman with ports < 1024:

```bash
# If you need to bind to port 80/443, use:
sudo sysctl net.ipv4.ip_unprivileged_port_start=80

# Or use higher ports and reverse proxy
```

### 4. **Podman Socket (Optional)**

If you want full Docker CLI compatibility:

```bash
# Start Podman socket
systemctl --user start podman.socket

# Enable on boot
systemctl --user enable podman.socket

# Now you can use docker commands
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock
docker ps  # Works with Podman!
```

---

## ?? Common Podman Compose Commands

All Docker Compose commands work with Podman Compose:

```bash
# Start services
podman-compose up -d

# View logs
podman-compose logs -f
podman-compose logs -f backend
podman-compose logs -f frontend

# Stop services
podman-compose down

# Restart services
podman-compose restart

# Rebuild after code changes
podman-compose up -d --build

# View running containers
podman-compose ps

# Execute commands in containers
podman-compose exec backend python init_db.py
podman-compose exec postgres psql -U postgres -d shopping_mart

# Remove volumes (clean slate)
podman-compose down -v
```

---

## ?? Troubleshooting

### Issue: "Port already in use"

```bash
# Check what's using the port
sudo lsof -i :3000
sudo lsof -i :8000

# Or use different ports in docker-compose.yml
# Change "3000:3000" to "3001:3000"
```

### Issue: "Permission denied" on volumes

```bash
# For rootless Podman, ensure correct permissions
sudo chown -R $(id -u):$(id -g) backend/uploads
```

### Issue: Services not starting

```bash
# Check Podman system
podman info

# View detailed logs
podman-compose logs --tail=100

# Restart Podman
systemctl --user restart podman.socket
```

### Issue: "Cannot connect to database"

```bash
# Wait longer for PostgreSQL to initialize
sleep 30
podman-compose exec backend python init_db.py

# Check PostgreSQL is running
podman-compose ps
podman-compose logs postgres
```

### Issue: Frontend can't reach backend

```bash
# Check if all containers are on the same network
podman network ls
podman network inspect shopping_mart_default

# Restart services
podman-compose down
podman-compose up -d
```

---

## ?? Verification Steps

After starting with Podman Compose:

```bash
# 1. Check all containers are running
podman-compose ps

# Expected output:
# shopping_mart_frontend   running
# shopping_mart_backend    running
# shopping_mart_db         running
# shopping_mart_redis      running

# 2. Check backend health
curl http://localhost:8000/health

# Expected: {"status":"healthy"}

# 3. Check frontend
curl http://localhost:3000

# Expected: HTML content

# 4. View logs
podman-compose logs backend | tail -20
podman-compose logs frontend | tail -20
```

---

## ?? Resource Management with Podman

### View Resource Usage

```bash
# Container stats
podman stats

# System df
podman system df
```

### Cleanup

```bash
# Remove stopped containers
podman container prune

# Remove unused images
podman image prune

# Remove unused volumes
podman volume prune

# Clean everything
podman system prune -a --volumes
```

---

## ?? Migration from Docker to Podman

If you're migrating from Docker:

```bash
# 1. Stop Docker containers
docker-compose down

# 2. Start with Podman
podman-compose up -d

# 3. Initialize database (same as before)
podman-compose exec backend python init_db.py
```

**Note**: Volumes are separate between Docker and Podman, so you'll need to re-initialize the database.

---

## ?? Podman Advantages

- ? **Rootless**: More secure, runs as regular user
- ? **Daemonless**: No background daemon required
- ? **Compatible**: Works with Docker Compose files
- ? **Systemd Integration**: Native systemd support
- ? **OCI Compliant**: Standard container format
- ? **Drop-in Replacement**: Familiar Docker CLI

---

## ?? Production with Podman

### Systemd Service (Auto-start on boot)

```bash
# Generate systemd unit file
cd /workspace
podman-compose --file docker-compose.yml systemd

# Or create manually
mkdir -p ~/.config/systemd/user/
cat > ~/.config/systemd/user/shopping-mart.service << 'EOF'
[Unit]
Description=Shopping Mart System
Requires=network.target
After=network.target

[Service]
Type=simple
WorkingDirectory=/workspace
ExecStart=/usr/bin/podman-compose up
ExecStop=/usr/bin/podman-compose down
Restart=always

[Install]
WantedBy=default.target
EOF

# Enable and start
systemctl --user enable shopping-mart
systemctl --user start shopping-mart

# Check status
systemctl --user status shopping-mart
```

---

## ?? Quick Reference

| Task | Docker Compose | Podman Compose |
|------|----------------|----------------|
| Start | `docker-compose up -d` | `podman-compose up -d` |
| Stop | `docker-compose down` | `podman-compose down` |
| Logs | `docker-compose logs -f` | `podman-compose logs -f` |
| Exec | `docker-compose exec` | `podman-compose exec` |
| List | `docker ps` | `podman ps` |
| Images | `docker images` | `podman images` |

---

## ? You're Ready!

The application is fully compatible with Podman Compose. Just use `podman-compose` instead of `docker-compose` in all commands.

**Default Login Credentials:**
```
Admin:    username: admin    password: admin123
Manager:  username: manager  password: manager123
Cashier:  username: cashier  password: cashier123
```

---

## ?? Need Help?

- Review the main [README.md](README.md)
- Check [QUICKSTART.md](QUICKSTART.md)
- Podman docs: https://docs.podman.io

---

**Happy testing with Podman! ??**
