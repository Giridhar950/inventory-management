# Kubernetes Deployment Fix

## Issues Fixed

### 1. **Deprecated Kustomize Fields**
The kustomization files were using deprecated fields that caused deployment failures:

**Fixed in all kustomization.yaml files:**
- ? `bases` ? ? `resources`
- ? `commonLabels` ? ? `labels` (with proper structure)
- ? `patchesStrategicMerge` ? ? `patches` (with path specification)

### 2. **ConfigMap Generator Conflict**
The dev and prod overlays were trying to use `configMapGenerator` with `behavior: merge`, but the base layer defined ConfigMap as a resource file, not a generator. This caused the error:
```
error: merging from generator: id does not exist; cannot merge or replace
```

**Solution:** Replaced the generators with ConfigMap patch files:
- Created `/workspace/k8s/overlays/dev/configmap-patch.yaml`
- Created `/workspace/k8s/overlays/prod/configmap-patch.yaml`

### 3. **Namespace Timing Issue**
When applying resources directly with `kubectl apply -f k8s/base/`, the namespace resource was created, but other resources that depended on it failed because kubectl processes files in parallel.

**Solution:** Always use kustomize (either `kubectl apply -k` or `kustomize build | kubectl apply -f -`)

---

## How to Deploy

### ? Option 1: Using the Deploy Script (Recommended)

```bash
# Deploy to development environment
./k8s/deploy.sh dev apply

# Deploy to production environment
./k8s/deploy.sh prod apply

# Delete from development
./k8s/deploy.sh dev delete

# Delete from production
./k8s/deploy.sh prod delete
```

### ? Option 2: Using kubectl with -k flag

```bash
# Deploy to dev
kubectl apply -k k8s/overlays/dev

# Deploy to prod
kubectl apply -k k8s/overlays/prod

# Delete from dev
kubectl delete -k k8s/overlays/dev

# Delete from prod
kubectl delete -k k8s/overlays/prod
```

### ? Option 3: Using kustomize command (if installed)

```bash
# Preview the manifests for dev
kustomize build k8s/overlays/dev

# Deploy to dev
kustomize build k8s/overlays/dev | kubectl apply -f -

# Deploy to prod
kustomize build k8s/overlays/prod | kubectl apply -f -

# Delete from dev
kustomize build k8s/overlays/dev | kubectl delete -f -

# Delete from prod
kustomize build k8s/overlays/prod | kubectl delete -f -
```

---

## ? What NOT to Do

**DO NOT** apply base resources directly:
```bash
# ? This will cause namespace timing issues
kubectl apply -f k8s/base/
```

**Reason:** When you apply files directly from the base directory, kubectl processes them in parallel. The namespace gets created, but other resources that reference it may fail because they're processed before the namespace is fully ready.

---

## Changes Made to Fix

### `/workspace/k8s/base/kustomization.yaml`
```yaml
# Before
commonLabels:
  app: shopping-mart
  managed-by: kustomize

# After
labels:
  - pairs:
      app: shopping-mart
      managed-by: kustomize
```

### `/workspace/k8s/overlays/dev/kustomization.yaml`
```yaml
# Before
bases:
  - ../../base
commonLabels:
  environment: development
patchesStrategicMerge:
  - replica-patch.yaml
  - resource-patch.yaml
configMapGenerator:
  - name: shopping-mart-config
    behavior: merge
    literals:
      - DEBUG=True
      - VITE_API_BASE_URL=http://localhost:8000/api/v1

# After
resources:
  - ../../base
labels:
  - pairs:
      environment: development
patches:
  - path: replica-patch.yaml
  - path: resource-patch.yaml
  - path: configmap-patch.yaml
```

### `/workspace/k8s/overlays/prod/kustomization.yaml`
Similar changes as dev overlay.

### New Files Created

**`/workspace/k8s/overlays/dev/configmap-patch.yaml`**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: shopping-mart-config
data:
  DEBUG: "True"
  VITE_API_BASE_URL: "http://localhost:8000/api/v1"
```

**`/workspace/k8s/overlays/prod/configmap-patch.yaml`**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: shopping-mart-config
data:
  DEBUG: "False"
  VITE_API_BASE_URL: "https://api.shopping-mart.example.com/api/v1"
```

---

## Verification

After deployment, verify the resources:

```bash
# Check all resources in dev namespace
kubectl get all -n shopping-mart-dev

# Check pods
kubectl get pods -n shopping-mart-dev

# Check services
kubectl get svc -n shopping-mart-dev

# Check ingress
kubectl get ingress -n shopping-mart-dev

# View logs
kubectl logs -f deployment/dev-backend -n shopping-mart-dev
kubectl logs -f deployment/dev-frontend -n shopping-mart-dev
```

---

## Port Forwarding (for local access)

```bash
# Forward frontend
kubectl port-forward svc/dev-frontend-service 3000:3000 -n shopping-mart-dev

# Forward backend
kubectl port-forward svc/dev-backend-service 8000:8000 -n shopping-mart-dev
```

---

## Troubleshooting

### If deployment still fails with deprecated warnings

Run this command to fix deprecated fields automatically:
```bash
cd k8s/overlays/dev
kustomize edit fix

cd ../prod
kustomize edit fix
```

### If ConfigMap issues persist

Make sure the configmap-patch.yaml files exist in both overlay directories:
```bash
ls -la k8s/overlays/dev/configmap-patch.yaml
ls -la k8s/overlays/prod/configmap-patch.yaml
```

### If namespace errors occur

Always use kustomize to apply resources (via deploy script or `kubectl apply -k`), never apply base files directly.

---

## Summary

? **All deprecated fields updated to current Kustomize syntax**  
? **ConfigMap generator conflict resolved with patch files**  
? **Namespace timing issues eliminated by using kustomize**  
? **Deploy script works correctly**  

You can now deploy successfully using: `./k8s/deploy.sh dev apply`
