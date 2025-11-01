# Kubernetes Deployment Guide

This directory contains Kubernetes manifests for deploying the Shopping Mart System to a Kubernetes cluster.

---

## ?? Directory Structure

```
k8s/
??? base/                          # Base Kubernetes manifests
?   ??? namespace.yaml             # Namespace definition
?   ??? configmap.yaml             # Configuration
?   ??? secret.yaml                # Secrets
?   ??? postgres-pvc.yaml          # PostgreSQL storage
?   ??? redis-pvc.yaml             # Redis storage
?   ??? postgres-deployment.yaml   # PostgreSQL deployment & service
?   ??? redis-deployment.yaml      # Redis deployment & service
?   ??? backend-deployment.yaml    # Backend API deployment & service
?   ??? frontend-deployment.yaml   # Frontend deployment & service
?   ??? ingress.yaml               # Ingress for external access
?   ??? hpa.yaml                   # Horizontal Pod Autoscaler
?   ??? job-init-db.yaml           # Database initialization job
?   ??? kustomization.yaml         # Kustomize configuration
??? overlays/
?   ??? dev/                       # Development environment
?   ?   ??? kustomization.yaml
?   ?   ??? replica-patch.yaml     # Lower replicas for dev
?   ?   ??? resource-patch.yaml    # Lower resources for dev
?   ??? prod/                      # Production environment
?       ??? kustomization.yaml
?       ??? replica-patch.yaml     # Higher replicas for prod
?       ??? security-patch.yaml    # Security policies
??? deploy.sh                      # Deployment script
??? README.md                      # This file
```

---

## ?? Quick Start

### Prerequisites

1. **Kubernetes cluster** (1.19+)
   - Minikube (local)
   - GKE, EKS, AKS (cloud)
   - K3s, MicroK8s (lightweight)

2. **kubectl** installed and configured
   ```bash
   kubectl version --client
   kubectl cluster-info
   ```

3. **Docker images** built and pushed
   ```bash
   # Build images
   cd backend && docker build -t shopping-mart-backend:latest .
   cd frontend && docker build -t shopping-mart-frontend:latest .
   
   # Tag and push to registry (replace with your registry)
   docker tag shopping-mart-backend:latest your-registry/shopping-mart-backend:v1.0.0
   docker tag shopping-mart-frontend:latest your-registry/shopping-mart-frontend:v1.0.0
   docker push your-registry/shopping-mart-backend:v1.0.0
   docker push your-registry/shopping-mart-frontend:v1.0.0
   ```

### Option 1: Using the Deployment Script (Recommended)

```bash
# Deploy to development
./k8s/deploy.sh dev apply

# Deploy to production
./k8s/deploy.sh prod apply

# Delete from development
./k8s/deploy.sh dev delete
```

### Option 2: Using kubectl with Kustomize

```bash
# Deploy to development
kubectl apply -k k8s/overlays/dev

# Deploy to production
kubectl apply -k k8s/overlays/prod

# Delete
kubectl delete -k k8s/overlays/dev
```

### Option 3: Manual kubectl apply

```bash
# Apply base manifests
kubectl apply -f k8s/base/

# Or apply individually
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/configmap.yaml
kubectl apply -f k8s/base/secret.yaml
# ... etc
```

---

## ?? Configuration

### 1. Update Secrets

**IMPORTANT**: Before deploying to production, update secrets:

```bash
# Edit k8s/base/secret.yaml
# Change POSTGRES_PASSWORD and SECRET_KEY

# Or create secret manually
kubectl create secret generic shopping-mart-secrets \
  --from-literal=POSTGRES_PASSWORD='your-secure-password' \
  --from-literal=SECRET_KEY='your-secret-key-min-32-chars' \
  -n shopping-mart
```

### 2. Update Image Registry

Edit `k8s/overlays/prod/kustomization.yaml`:

```yaml
images:
  - name: shopping-mart-backend
    newName: your-registry.io/shopping-mart-backend
    newTag: v1.0.0
  - name: shopping-mart-frontend
    newName: your-registry.io/shopping-mart-frontend
    newTag: v1.0.0
```

### 3. Configure Ingress

Edit `k8s/base/ingress.yaml`:

```yaml
spec:
  tls:
  - hosts:
    - your-domain.com
    - api.your-domain.com
    secretName: shopping-mart-tls
  rules:
  - host: your-domain.com
    # ... frontend rules
  - host: api.your-domain.com
    # ... backend rules
```

### 4. Storage Class

Update storage class in PVC files if needed:

```yaml
# k8s/base/postgres-pvc.yaml
spec:
  storageClassName: standard  # Change to your storage class
```

Common storage classes:
- **GKE**: `standard`, `standard-rwo`
- **EKS**: `gp2`, `gp3`
- **AKS**: `default`, `managed-premium`
- **Minikube**: `standard`

---

## ?? Verification

### Check Deployment Status

```bash
# Get all resources
kubectl get all -n shopping-mart

# Check pods
kubectl get pods -n shopping-mart

# Check services
kubectl get svc -n shopping-mart

# Check ingress
kubectl get ingress -n shopping-mart

# Check persistent volumes
kubectl get pvc -n shopping-mart
```

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/backend -n shopping-mart

# Frontend logs
kubectl logs -f deployment/frontend -n shopping-mart

# PostgreSQL logs
kubectl logs -f deployment/postgres -n shopping-mart

# All logs
kubectl logs -f -l app=shopping-mart -n shopping-mart
```

### Database Initialization

```bash
# Check init job status
kubectl get jobs -n shopping-mart

# View init job logs
kubectl logs job/init-database -n shopping-mart

# Re-run init job if needed
kubectl delete job init-database -n shopping-mart
kubectl apply -f k8s/base/job-init-db.yaml
```

---

## ?? Accessing the Application

### Option 1: Ingress (Production)

After configuring DNS and ingress:
- Frontend: https://your-domain.com
- Backend API: https://api.your-domain.com
- API Docs: https://api.your-domain.com/api/docs

### Option 2: Port Forwarding (Development)

```bash
# Frontend
kubectl port-forward svc/frontend-service 3000:3000 -n shopping-mart

# Backend
kubectl port-forward svc/backend-service 8000:8000 -n shopping-mart

# PostgreSQL (for debugging)
kubectl port-forward svc/postgres-service 5432:5432 -n shopping-mart

# Redis (for debugging)
kubectl port-forward svc/redis-service 6379:6379 -n shopping-mart
```

Then access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

### Option 3: LoadBalancer (Cloud)

Change service type to LoadBalancer:

```yaml
# In deployment files
spec:
  type: LoadBalancer  # Instead of ClusterIP
```

Get external IP:
```bash
kubectl get svc -n shopping-mart
```

---

## ?? Scaling

### Manual Scaling

```bash
# Scale backend
kubectl scale deployment backend --replicas=5 -n shopping-mart

# Scale frontend
kubectl scale deployment frontend --replicas=3 -n shopping-mart
```

### Auto-Scaling (HPA)

Horizontal Pod Autoscaler is configured in `k8s/base/hpa.yaml`:

```bash
# Check HPA status
kubectl get hpa -n shopping-mart

# Describe HPA
kubectl describe hpa backend-hpa -n shopping-mart
```

HPA automatically scales based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)

---

## ?? Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n shopping-mart

# Describe pod
kubectl describe pod <pod-name> -n shopping-mart

# Check events
kubectl get events -n shopping-mart --sort-by='.lastTimestamp'
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
kubectl get pods -l component=database -n shopping-mart

# Test connection
kubectl exec -it deployment/postgres -n shopping-mart -- psql -U postgres -d shopping_mart

# Check backend can reach postgres
kubectl exec -it deployment/backend -n shopping-mart -- nc -zv postgres-service 5432
```

### Image Pull Errors

```bash
# Check image pull secrets
kubectl get secrets -n shopping-mart

# Create image pull secret if needed
kubectl create secret docker-registry regcred \
  --docker-server=your-registry.io \
  --docker-username=your-username \
  --docker-password=your-password \
  -n shopping-mart

# Add to deployment
spec:
  template:
    spec:
      imagePullSecrets:
      - name: regcred
```

### Storage Issues

```bash
# Check PVCs
kubectl get pvc -n shopping-mart

# Describe PVC
kubectl describe pvc postgres-pvc -n shopping-mart

# Check storage class
kubectl get storageclass
```

### Ingress Not Working

```bash
# Check ingress controller is installed
kubectl get pods -n ingress-nginx

# Install nginx ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Check ingress
kubectl describe ingress shopping-mart-ingress -n shopping-mart

# View ingress controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller
```

---

## ?? Security Best Practices

### 1. Use Secrets Management

Consider using external secrets managers:
- **HashiCorp Vault**
- **AWS Secrets Manager**
- **Azure Key Vault**
- **GCP Secret Manager**

### 2. Network Policies

Create network policies to restrict pod communication:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
  namespace: shopping-mart
spec:
  podSelector:
    matchLabels:
      component: backend
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          component: frontend
    ports:
    - protocol: TCP
      port: 8000
```

### 3. Pod Security Policies

Already configured in `k8s/overlays/prod/security-patch.yaml`:
- Run as non-root
- Drop all capabilities
- Read-only root filesystem (where possible)

### 4. RBAC

Create service accounts with minimal permissions:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: shopping-mart-sa
  namespace: shopping-mart
```

---

## ?? Monitoring

### Metrics

Install metrics server:
```bash
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
```

View metrics:
```bash
# Node metrics
kubectl top nodes

# Pod metrics
kubectl top pods -n shopping-mart
```

### Logging

View logs:
```bash
# Stream logs
kubectl logs -f deployment/backend -n shopping-mart

# Last 100 lines
kubectl logs --tail=100 deployment/backend -n shopping-mart

# Logs from all replicas
kubectl logs -l component=backend -n shopping-mart
```

### Health Checks

Configured liveness and readiness probes:
- Backend: `GET /health`
- Frontend: `GET /`
- PostgreSQL: `pg_isready`
- Redis: `redis-cli ping`

---

## ?? CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build and push images
      run: |
        docker build -t your-registry/backend:${{ github.sha }} backend/
        docker build -t your-registry/frontend:${{ github.sha }} frontend/
        docker push your-registry/backend:${{ github.sha }}
        docker push your-registry/frontend:${{ github.sha }}
    
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/backend backend=your-registry/backend:${{ github.sha }} -n shopping-mart
        kubectl set image deployment/frontend frontend=your-registry/frontend:${{ github.sha }} -n shopping-mart
```

---

## ?? Cleanup

### Delete Everything

```bash
# Using script
./k8s/deploy.sh dev delete

# Using kubectl
kubectl delete namespace shopping-mart

# Or delete specific resources
kubectl delete -k k8s/overlays/dev
```

### Preserve Data

To keep persistent data, don't delete PVCs:

```bash
kubectl delete deployment,service,ingress -n shopping-mart --all
# PVCs remain intact
```

---

## ?? Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Kustomize Documentation](https://kustomize.io/)
- [Ingress NGINX](https://kubernetes.github.io/ingress-nginx/)
- [Cert Manager](https://cert-manager.io/)
- [Metrics Server](https://github.com/kubernetes-sigs/metrics-server)

---

## ?? Production Checklist

Before deploying to production:

- [ ] Update all secrets
- [ ] Configure proper storage class
- [ ] Set up ingress with SSL/TLS
- [ ] Configure DNS records
- [ ] Set resource limits appropriately
- [ ] Enable HPA
- [ ] Set up monitoring and logging
- [ ] Configure backups for PostgreSQL
- [ ] Test disaster recovery
- [ ] Set up CI/CD pipeline
- [ ] Configure network policies
- [ ] Review security policies
- [ ] Set up alerts

---

**Ready to deploy to Kubernetes! ??**
