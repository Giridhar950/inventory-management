# Deployment Options - Shopping Mart System

Complete guide to all available deployment methods for the Shopping Mart Inventory & Billing System.

---

## ?? Choose Your Deployment Method

| Method | Best For | Difficulty | Time to Deploy | Documentation |
|--------|----------|------------|----------------|---------------|
| **Docker Compose** | Local development, testing | ? Easy | 5 minutes | [README.md](README.md) |
| **Podman Compose** | Rootless containers, RHEL/Fedora | ? Easy | 5 minutes | [PODMAN_SETUP.md](PODMAN_SETUP.md) |
| **Kubernetes** | Production, cloud, scalability | ??? Advanced | 15-30 minutes | [KUBERNETES.md](KUBERNETES.md) |
| **Manual** | Learning, custom setup | ?? Moderate | 30 minutes | [README.md](README.md) |

---

## 1?? Docker Compose (Recommended for Getting Started)

### ? Pros
- Easiest to get started
- No Kubernetes knowledge required
- Works on any OS (Windows, Mac, Linux)
- Great for local development and testing
- One-command deployment

### ? Cons
- Single host only (no clustering)
- No built-in auto-scaling
- Limited production features
- Manual high availability setup

### ?? Quick Start

```bash
# Clone and start
git clone <repo-url>
cd shopping-mart-system
chmod +x start.sh
./start.sh

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### ?? Resource Requirements
- **RAM**: 2GB minimum, 4GB recommended
- **CPU**: 2 cores minimum
- **Disk**: 5GB free space

### ?? Documentation
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Full Guide**: [README.md](README.md) - Installation Section

---

## 2?? Podman Compose (Docker Alternative)

### ? Pros
- Rootless (more secure)
- Daemonless architecture
- Fully compatible with Docker Compose files
- Native to RHEL/Fedora/CentOS
- Systemd integration

### ? Cons
- Same limitations as Docker Compose (single host)
- Less common than Docker
- Some edge cases may differ

### ?? Quick Start

```bash
# Install Podman
# Fedora/RHEL: sudo dnf install podman podman-compose
# Ubuntu: sudo apt-get install podman podman-compose

# Deploy
chmod +x start-podman.sh
./start-podman.sh

# Or use podman-compose directly
podman-compose up -d
podman-compose exec backend python init_db.py
```

### ?? Resource Requirements
- Same as Docker Compose
- Can run rootless with lower privileges

### ?? Documentation
- **Full Guide**: [PODMAN_SETUP.md](PODMAN_SETUP.md)

---

## 3?? Kubernetes (Recommended for Production)

### ? Pros
- Production-grade deployment
- Auto-scaling (HPA)
- Self-healing (automatic restarts)
- Load balancing
- Rolling updates with zero downtime
- Works on any cloud (GKE, EKS, AKS)
- Handles high availability

### ? Cons
- More complex setup
- Requires Kubernetes knowledge
- Higher resource overhead
- More moving parts to manage

### ?? Quick Start

```bash
# Prerequisites: kubectl, Kubernetes cluster, images in registry

# Deploy to development
./k8s/deploy.sh dev apply

# Deploy to production
./k8s/deploy.sh prod apply

# Access locally (port-forward)
kubectl port-forward svc/frontend-service 3000:3000 -n shopping-mart
kubectl port-forward svc/backend-service 8000:8000 -n shopping-mart
```

### ?? Resource Requirements

**Development:**
- **Nodes**: 1 node (Minikube OK)
- **RAM**: 4GB per node
- **CPU**: 2 cores per node

**Production:**
- **Nodes**: 3+ nodes (high availability)
- **RAM**: 4-8GB per node
- **CPU**: 2-4 cores per node
- **Storage**: 20GB+ for PVCs

### ?? What's Included

? **21 Kubernetes manifest files**
? **Kustomize overlays** for dev/prod
? **Horizontal Pod Autoscaler** (2-10 replicas)
? **Ingress** with SSL/TLS support
? **Persistent storage** (PostgreSQL, Redis)
? **Health checks** (liveness, readiness)
? **Resource limits** and requests
? **Security policies** (non-root, capabilities)
? **One-command deployment** script

### ?? Architecture

```
Ingress ? Frontend Service ? Frontend Pods (2-5 replicas)
       ? Backend Service  ? Backend Pods (2-10 replicas)
                          ? PostgreSQL (1 replica + PVC)
                          ? Redis (1 replica + PVC)
```

### ?? Documentation
- **Quick Start**: [KUBERNETES.md](KUBERNETES.md)
- **Full K8s Guide**: [k8s/README.md](k8s/README.md)
- **Deployment Script**: `k8s/deploy.sh`

---

## 4?? Manual Installation

### ? Pros
- Full control over every component
- No Docker/Podman required
- Great for learning
- Customize everything

### ? Cons
- Most time-consuming
- Requires manual database setup
- No containerization benefits
- More maintenance

### ?? Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

### ?? Resource Requirements
- **RAM**: 1GB minimum
- **CPU**: 1 core minimum
- **PostgreSQL 15+** installed
- **Redis 7+** installed
- **Python 3.11+** installed
- **Node.js 18+** installed

### ?? Documentation
- **Full Guide**: [README.md](README.md) - Manual Installation Section

---

## ?? Decision Matrix

### Choose **Docker Compose** if:
- ? You want to get started quickly
- ? You're developing/testing locally
- ? You need a simple setup
- ? You're on a single server
- ? You don't need high availability

### Choose **Podman Compose** if:
- ? You prefer rootless containers
- ? You're on RHEL/Fedora/CentOS
- ? You want better security (rootless)
- ? You want systemd integration
- ? Same use case as Docker Compose

### Choose **Kubernetes** if:
- ? You're deploying to production
- ? You need auto-scaling
- ? You need high availability
- ? You're using cloud providers
- ? You need zero-downtime updates
- ? You expect high traffic
- ? You need multi-node setup

### Choose **Manual Installation** if:
- ? You're learning the stack
- ? You need full customization
- ? You can't use containers
- ? You want minimal overhead
- ? You're on a restricted environment

---

## ?? Feature Comparison

| Feature | Docker Compose | Podman Compose | Kubernetes | Manual |
|---------|----------------|----------------|------------|--------|
| **Auto-scaling** | ? | ? | ? HPA | ? |
| **High Availability** | ? | ? | ? Multi-node | ? |
| **Load Balancing** | ?? Manual | ?? Manual | ? Built-in | ? |
| **Self-healing** | ?? Restart policy | ?? Restart policy | ? Automatic | ? |
| **Rolling Updates** | ? | ? | ? Zero-downtime | ? |
| **Resource Limits** | ? | ? | ? Advanced | ? |
| **Health Checks** | ? | ? | ? Advanced | ? |
| **Persistent Storage** | ? Volumes | ? Volumes | ? PVCs | ? Local |
| **Secrets Management** | ? Env vars | ? Env vars | ? K8s Secrets | ? Env vars |
| **Monitoring** | ?? Manual | ?? Manual | ? Prometheus | ?? Manual |
| **Ease of Use** | ????? | ???? | ?? | ?? |
| **Production Ready** | ?? Limited | ?? Limited | ? Yes | ?? Limited |

---

## ?? Cloud Provider Recommendations

### AWS
- **Development**: Docker Compose on EC2
- **Production**: EKS (Kubernetes) + RDS + ElastiCache

### Google Cloud
- **Development**: Docker Compose on Compute Engine
- **Production**: GKE (Kubernetes) + Cloud SQL + Memorystore

### Azure
- **Development**: Docker Compose on VM
- **Production**: AKS (Kubernetes) + Azure Database + Azure Cache

### DigitalOcean
- **Development**: Docker Compose on Droplet
- **Production**: DOKS (Kubernetes) + Managed PostgreSQL + Managed Redis

### On-Premise
- **Development**: Docker Compose or Podman Compose
- **Production**: Kubernetes (K3s, MicroK8s, or full K8s)

---

## ?? Migration Path

### From Docker Compose to Kubernetes

1. **Build and tag images**:
   ```bash
   docker build -t your-registry/backend:v1.0.0 backend/
   docker build -t your-registry/frontend:v1.0.0 frontend/
   ```

2. **Push to registry**:
   ```bash
   docker push your-registry/backend:v1.0.0
   docker push your-registry/frontend:v1.0.0
   ```

3. **Update K8s manifests**:
   Edit `k8s/overlays/prod/kustomization.yaml` with your image names

4. **Deploy to Kubernetes**:
   ```bash
   ./k8s/deploy.sh prod apply
   ```

### From Manual to Docker Compose

1. **Stop manual services**:
   ```bash
   # Stop backend, frontend, PostgreSQL, Redis
   ```

2. **Export data** (if needed):
   ```bash
   pg_dump shopping_mart > backup.sql
   ```

3. **Deploy with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

4. **Import data** (if needed):
   ```bash
   docker-compose exec postgres psql -U postgres shopping_mart < backup.sql
   ```

---

## ?? All Documentation Files

| File | Description |
|------|-------------|
| [README.md](README.md) | Main documentation, installation, usage |
| [QUICKSTART.md](QUICKSTART.md) | 5-minute quick start guide |
| [PODMAN_SETUP.md](PODMAN_SETUP.md) | Complete Podman Compose guide |
| [KUBERNETES.md](KUBERNETES.md) | Kubernetes quick reference |
| [k8s/README.md](k8s/README.md) | Detailed Kubernetes documentation |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Complete project overview |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | Production deployment checklist |
| **This file** | Comparison of all deployment methods |

---

## ?? Learning Path

**Beginner ? Intermediate ? Advanced**

1. **Start with Docker Compose** (1 hour)
   - Get familiar with the application
   - Understand the architecture
   - Test all features

2. **Try Podman Compose** (30 minutes)
   - Learn rootless containers
   - Understand security benefits
   - Compare with Docker

3. **Deploy to Kubernetes** (2-4 hours)
   - Learn K8s basics
   - Understand pods, services, deployments
   - Deploy to Minikube first
   - Then try cloud providers

4. **Production Deployment** (1 day)
   - Set up monitoring
   - Configure CI/CD
   - Implement security best practices
   - Set up backups

---

## ?? Quick Command Reference

### Docker Compose
```bash
docker-compose up -d              # Start
docker-compose logs -f            # View logs
docker-compose down               # Stop
docker-compose restart            # Restart
```

### Podman Compose
```bash
podman-compose up -d              # Start
podman-compose logs -f            # View logs
podman-compose down               # Stop
podman-compose restart            # Restart
```

### Kubernetes
```bash
./k8s/deploy.sh dev apply         # Deploy dev
./k8s/deploy.sh prod apply        # Deploy prod
kubectl get pods -n shopping-mart # Check status
kubectl logs -f deployment/backend # View logs
./k8s/deploy.sh dev delete        # Delete
```

---

## ? Success Metrics

After deployment, verify:

- ? Frontend loads at http://localhost:3000
- ? Backend API responds at http://localhost:8000
- ? API docs accessible at http://localhost:8000/api/docs
- ? Can login with default credentials
- ? Can create products
- ? Can process sales in POS
- ? Dashboard shows metrics
- ? All services healthy (docker-compose ps or kubectl get pods)

---

## ?? Need Help?

- **Quick Start Issues**: [QUICKSTART.md](QUICKSTART.md)
- **Docker Issues**: [README.md](README.md)
- **Podman Issues**: [PODMAN_SETUP.md](PODMAN_SETUP.md)
- **Kubernetes Issues**: [k8s/README.md](k8s/README.md)
- **General Questions**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

**Choose your path and start deploying! ??**
