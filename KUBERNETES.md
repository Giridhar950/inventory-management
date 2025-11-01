# Kubernetes Deployment - Quick Reference

Complete Kubernetes manifests for deploying the Shopping Mart System to any Kubernetes cluster.

---

## ? What's Included

### ?? Kubernetes Manifests (20 files)

```
k8s/
??? base/                          # Base manifests
?   ??? namespace.yaml             # Namespace
?   ??? configmap.yaml             # Configuration
?   ??? secret.yaml                # Secrets (change in prod!)
?   ??? postgres-pvc.yaml          # 10Gi PostgreSQL storage
?   ??? redis-pvc.yaml             # 5Gi Redis storage
?   ??? postgres-deployment.yaml   # PostgreSQL + Service
?   ??? redis-deployment.yaml      # Redis + Service
?   ??? backend-deployment.yaml    # Backend API + Service
?   ??? frontend-deployment.yaml   # Frontend + Service
?   ??? ingress.yaml               # Ingress (2 options)
?   ??? hpa.yaml                   # Auto-scaling
?   ??? job-init-db.yaml           # DB initialization
?   ??? kustomization.yaml         # Kustomize config
??? overlays/
?   ??? dev/                       # Development config
?   ?   ??? kustomization.yaml     # Dev overrides
?   ?   ??? replica-patch.yaml     # 1 replica each
?   ?   ??? resource-patch.yaml    # Lower resources
?   ??? prod/                      # Production config
?       ??? kustomization.yaml     # Prod overrides
?       ??? replica-patch.yaml     # 3 replicas each
?       ??? security-patch.yaml    # Security policies
??? deploy.sh                      # Deployment script
??? README.md                      # Full documentation
```

---

## ?? Quick Deploy

### Prerequisites

1. **Kubernetes cluster** (Minikube, GKE, EKS, AKS, etc.)
2. **kubectl** installed and configured
3. **Docker images** built and pushed to registry

### Step 1: Build and Push Images

```bash
# Build images
docker build -t shopping-mart-backend:latest backend/
docker build -t shopping-mart-frontend:latest frontend/

# For Minikube (skip pushing)
eval $(minikube docker-env)
docker build -t shopping-mart-backend:latest backend/
docker build -t shopping-mart-frontend:latest frontend/

# For cloud registry
docker tag shopping-mart-backend:latest your-registry/shopping-mart-backend:v1.0.0
docker tag shopping-mart-frontend:latest your-registry/shopping-mart-frontend:v1.0.0
docker push your-registry/shopping-mart-backend:v1.0.0
docker push your-registry/shopping-mart-frontend:v1.0.0
```

### Step 2: Deploy to Kubernetes

```bash
# Option A: Using the deployment script (easiest)
chmod +x k8s/deploy.sh
./k8s/deploy.sh dev apply

# Option B: Using kubectl with kustomize
kubectl apply -k k8s/overlays/dev

# Option C: Manual deployment
kubectl apply -f k8s/base/
```

### Step 3: Access the Application

```bash
# Port forward to access locally
kubectl port-forward svc/frontend-service 3000:3000 -n shopping-mart
kubectl port-forward svc/backend-service 8000:8000 -n shopping-mart

# Or get LoadBalancer IP (if configured)
kubectl get svc -n shopping-mart

# Or via Ingress (after DNS setup)
# https://shopping-mart.example.com
```

---

## ?? Architecture

### Deployment Architecture

```
???????????????????????????????????????????????????????????
?                    Kubernetes Cluster                    ?
?                                                          ?
?  ?????????????????????????????????????????????????????? ?
?  ?              Ingress Controller                     ? ?
?  ?  (shopping-mart.com, api.shopping-mart.com)       ? ?
?  ?????????????????????????????????????????????????????? ?
?              ?                      ?                    ?
?  ??????????????????????? ??????????????????????       ?
?  ?  Frontend Service   ? ?  Backend Service    ?       ?
?  ?  (ClusterIP:3000)   ? ?  (ClusterIP:8000)   ?       ?
?  ??????????????????????? ??????????????????????       ?
?              ?                      ?                    ?
?  ??????????????????????? ??????????????????????       ?
?  ?  Frontend Pods (?2) ? ?  Backend Pods (?2)  ?       ?
?  ?  [React App]        ? ?  [FastAPI]          ?       ?
?  ??????????????????????? ??????????????????????       ?
?                                     ?                    ?
?              ??????????????????????????????????         ?
?              ?                                ?         ?
?  ??????????????????????       ??????????????????????? ?
?  ?  PostgreSQL Pod    ?       ?    Redis Pod         ? ?
?  ?  (with PVC 10Gi)   ?       ?    (with PVC 5Gi)    ? ?
?  ??????????????????????       ??????????????????????? ?
?                                                          ?
?  ?????????????????????????????????????????????????????? ?
?  ?         Horizontal Pod Autoscaler (HPA)            ? ?
?  ?  Backend: 2-10 pods | Frontend: 2-5 pods          ? ?
?  ?????????????????????????????????????????????????????? ?
???????????????????????????????????????????????????????????
```

### Resource Allocation

| Component | Dev Replicas | Prod Replicas | CPU Request | Memory Request |
|-----------|--------------|---------------|-------------|----------------|
| Backend | 1 | 3 | 250m | 256Mi |
| Frontend | 1 | 3 | 100m | 128Mi |
| PostgreSQL | 1 | 1 | 250m | 256Mi |
| Redis | 1 | 1 | 100m | 128Mi |

---

## ?? Configuration

### 1. Update Secrets (REQUIRED for Production)

```bash
# Edit k8s/base/secret.yaml
# Change these values:
stringData:
  POSTGRES_PASSWORD: "your-secure-password-here"
  SECRET_KEY: "your-secret-key-min-32-characters-here"
```

Or create secret directly:
```bash
kubectl create secret generic shopping-mart-secrets \
  --from-literal=POSTGRES_PASSWORD='SecurePass123!' \
  --from-literal=SECRET_KEY='your-long-secret-key-at-least-32-chars' \
  -n shopping-mart
```

### 2. Update Image Registry

Edit `k8s/overlays/prod/kustomization.yaml`:

```yaml
images:
  - name: shopping-mart-backend
    newName: gcr.io/your-project/shopping-mart-backend
    newTag: v1.0.0
  - name: shopping-mart-frontend
    newName: gcr.io/your-project/shopping-mart-frontend
    newTag: v1.0.0
```

### 3. Configure Ingress & DNS

Edit `k8s/base/ingress.yaml`:

```yaml
spec:
  rules:
  - host: your-actual-domain.com      # Change this
  - host: api.your-actual-domain.com  # Change this
```

Then point DNS records to your ingress IP:
```bash
kubectl get ingress -n shopping-mart
# Get EXTERNAL-IP and create A records
```

---

## ?? Deployment Options

### Development (Minikube/Local)

```bash
# Start Minikube
minikube start --memory=4096 --cpus=2

# Enable ingress
minikube addons enable ingress

# Deploy
./k8s/deploy.sh dev apply

# Access via port-forward
kubectl port-forward svc/dev-frontend-service 3000:3000 -n shopping-mart-dev
kubectl port-forward svc/dev-backend-service 8000:8000 -n shopping-mart-dev

# Or via minikube
minikube service dev-frontend-service -n shopping-mart-dev
```

### Production (Cloud Provider)

**Google Kubernetes Engine (GKE):**
```bash
# Create cluster
gcloud container clusters create shopping-mart \
  --num-nodes=3 \
  --machine-type=n1-standard-2 \
  --zone=us-central1-a

# Get credentials
gcloud container clusters get-credentials shopping-mart

# Deploy
./k8s/deploy.sh prod apply
```

**Amazon EKS:**
```bash
# Create cluster (via eksctl)
eksctl create cluster \
  --name shopping-mart \
  --region us-east-1 \
  --nodegroup-name standard \
  --node-type t3.medium \
  --nodes 3

# Deploy
./k8s/deploy.sh prod apply
```

**Azure AKS:**
```bash
# Create cluster
az aks create \
  --resource-group shopping-mart-rg \
  --name shopping-mart \
  --node-count 3 \
  --node-vm-size Standard_DS2_v2

# Get credentials
az aks get-credentials --resource-group shopping-mart-rg --name shopping-mart

# Deploy
./k8s/deploy.sh prod apply
```

---

## ?? Monitoring & Management

### Check Status

```bash
# All resources
kubectl get all -n shopping-mart

# Pods with details
kubectl get pods -n shopping-mart -o wide

# Services and endpoints
kubectl get svc,endpoints -n shopping-mart

# Ingress
kubectl get ingress -n shopping-mart

# HPA status
kubectl get hpa -n shopping-mart

# Persistent volumes
kubectl get pvc -n shopping-mart
```

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/backend -n shopping-mart

# Frontend logs
kubectl logs -f deployment/frontend -n shopping-mart

# All backend pods
kubectl logs -f -l component=backend -n shopping-mart

# Tail last 100 lines
kubectl logs --tail=100 deployment/backend -n shopping-mart

# Previous pod logs (if crashed)
kubectl logs --previous deployment/backend -n shopping-mart
```

### Execute Commands

```bash
# Shell into backend pod
kubectl exec -it deployment/backend -n shopping-mart -- /bin/bash

# Run Python shell
kubectl exec -it deployment/backend -n shopping-mart -- python

# Connect to PostgreSQL
kubectl exec -it deployment/postgres -n shopping-mart -- psql -U postgres -d shopping_mart

# Redis CLI
kubectl exec -it deployment/redis -n shopping-mart -- redis-cli
```

---

## ?? Scaling

### Manual Scaling

```bash
# Scale backend to 5 replicas
kubectl scale deployment backend --replicas=5 -n shopping-mart

# Scale frontend to 3 replicas
kubectl scale deployment frontend --replicas=3 -n shopping-mart
```

### Auto-Scaling (HPA)

HPA automatically scales based on CPU/Memory:

```bash
# Check HPA
kubectl get hpa -n shopping-mart

# Expected output:
# NAME           REFERENCE            TARGETS         MINPODS   MAXPODS   REPLICAS
# backend-hpa    Deployment/backend   15%/70%         2         10        2
# frontend-hpa   Deployment/frontend  10%/70%         2         5         2

# Describe HPA
kubectl describe hpa backend-hpa -n shopping-mart

# Edit HPA
kubectl edit hpa backend-hpa -n shopping-mart
```

---

## ?? Security Features

### Implemented

? **Network Isolation**: ClusterIP services (internal only)
? **Pod Security**: Non-root users, dropped capabilities
? **Secret Management**: Kubernetes secrets for sensitive data
? **RBAC**: Role-based access control (namespace-scoped)
? **Resource Limits**: CPU/Memory limits to prevent resource exhaustion
? **Liveness/Readiness Probes**: Automatic health checks
? **TLS/SSL**: Ingress with TLS termination

### Recommended Additions

- **Network Policies**: Restrict pod-to-pod communication
- **Pod Security Policies**: Enforce security standards
- **External Secrets**: Use Vault, AWS Secrets Manager, etc.
- **Image Scanning**: Scan images for vulnerabilities
- **Admission Controllers**: Enforce policies (OPA, Kyverno)

---

## ?? Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -n shopping-mart

# Describe pod for events
kubectl describe pod <pod-name> -n shopping-mart

# Check events
kubectl get events -n shopping-mart --sort-by='.lastTimestamp'

# Common issues:
# - ImagePullBackOff: Image not found or auth issue
# - CrashLoopBackOff: Application crashing, check logs
# - Pending: Insufficient resources or PVC issues
```

### Database Connection Errors

```bash
# Verify PostgreSQL is running
kubectl get pods -l component=database -n shopping-mart

# Check logs
kubectl logs deployment/postgres -n shopping-mart

# Test connection from backend
kubectl exec -it deployment/backend -n shopping-mart -- nc -zv postgres-service 5432

# Check service DNS
kubectl exec -it deployment/backend -n shopping-mart -- nslookup postgres-service
```

### Storage Issues

```bash
# Check PVC status
kubectl get pvc -n shopping-mart

# Describe PVC
kubectl describe pvc postgres-pvc -n shopping-mart

# Check available storage classes
kubectl get storageclass

# If pending, may need to provision PV manually
```

### Ingress Not Working

```bash
# Check ingress
kubectl get ingress -n shopping-mart
kubectl describe ingress shopping-mart-ingress -n shopping-mart

# Install NGINX Ingress Controller (if missing)
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml

# Check ingress controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller
```

---

## ?? Cleanup

### Delete Deployment (Keep Data)

```bash
# Delete deployments and services only
kubectl delete deployment,service -n shopping-mart --all

# PVCs and data remain intact
```

### Complete Cleanup

```bash
# Using script
./k8s/deploy.sh dev delete

# Or delete namespace (removes everything)
kubectl delete namespace shopping-mart

# Warning: This deletes all data including PVCs!
```

---

## ?? Performance Tuning

### Resource Optimization

```yaml
# Adjust in deployment files
resources:
  requests:
    cpu: "500m"      # Guaranteed CPU
    memory: "512Mi"  # Guaranteed memory
  limits:
    cpu: "1000m"     # Max CPU
    memory: "1Gi"    # Max memory
```

### Database Optimization

```yaml
# PostgreSQL configuration
env:
  - name: POSTGRES_SHARED_BUFFERS
    value: "256MB"
  - name: POSTGRES_MAX_CONNECTIONS
    value: "100"
```

### HPA Tuning

```yaml
# Adjust scaling thresholds
metrics:
- type: Resource
  resource:
    name: cpu
    target:
      type: Utilization
      averageUtilization: 70  # Scale up at 70% CPU
```

---

## ?? Best Practices

### ? Do

- Use namespaces for isolation
- Set resource requests and limits
- Use liveness and readiness probes
- Version your images (avoid `:latest`)
- Use ConfigMaps for configuration
- Use Secrets for sensitive data
- Implement HPA for scalability
- Use Ingress for external access
- Monitor logs and metrics
- Backup database regularly

### ? Don't

- Don't hardcode secrets in manifests
- Don't use `:latest` tag in production
- Don't skip resource limits
- Don't run as root user
- Don't expose services unnecessarily
- Don't ignore security policies
- Don't skip health checks
- Don't forget to backup data

---

## ?? Next Steps

1. **Deploy to Dev**: Test with `./k8s/deploy.sh dev apply`
2. **Configure Monitoring**: Set up Prometheus + Grafana
3. **Set up Logging**: Deploy EFK/ELK stack
4. **Configure Backups**: Velero for cluster backups
5. **CI/CD Integration**: Automate deployments
6. **Production Deploy**: `./k8s/deploy.sh prod apply`

---

## ?? Useful Commands

```bash
# Get cluster info
kubectl cluster-info

# View all namespaces
kubectl get namespaces

# Switch namespace context
kubectl config set-context --current --namespace=shopping-mart

# View resource usage
kubectl top nodes
kubectl top pods -n shopping-mart

# Port forward multiple services
kubectl port-forward svc/frontend-service 3000:3000 -n shopping-mart &
kubectl port-forward svc/backend-service 8000:8000 -n shopping-mart &

# Generate YAML from running resources
kubectl get deployment backend -n shopping-mart -o yaml > backup.yaml

# Apply changes
kubectl apply -f k8s/base/backend-deployment.yaml

# Restart deployment
kubectl rollout restart deployment/backend -n shopping-mart

# View rollout status
kubectl rollout status deployment/backend -n shopping-mart

# Rollback deployment
kubectl rollout undo deployment/backend -n shopping-mart
```

---

**Your Shopping Mart System is now Kubernetes-ready! ??**

**Access after deployment:**
- Frontend: http://localhost:3000 (via port-forward)
- Backend: http://localhost:8000 (via port-forward)
- API Docs: http://localhost:8000/api/docs

**Default credentials:**
- Admin: `admin` / `admin123`
- Manager: `manager` / `manager123`
- Cashier: `cashier` / `cashier123`
