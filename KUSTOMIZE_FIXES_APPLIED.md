# Kustomize Configuration Fixes

## Issues Found and Fixed

### 1. Deprecated Kustomize Fields

**Problem:** The kustomization files were using deprecated fields that caused warnings and errors:
- `bases` ? deprecated, replaced with `resources`
- `commonLabels` ? deprecated, replaced with `labels`
- `patchesStrategicMerge` ? deprecated, replaced with `patches`

**Files Fixed:**
- ? `/workspace/k8s/base/kustomization.yaml`
- ? `/workspace/k8s/overlays/dev/kustomization.yaml`
- ? `/workspace/k8s/overlays/prod/kustomization.yaml`

### 2. ConfigMap Merge Error

**Problem:** The overlays were trying to merge with a static ConfigMap resource, which doesn't work. The error was:
```
id resid.ResId{...Kind:"ConfigMap", Name:"shopping-mart-config"...} does not exist; cannot merge or replace
```

**Root Cause:** When using `configMapGenerator` with `behavior: merge` in overlays, the base must also use `configMapGenerator`, not a static ConfigMap resource.

**Solution:**
- ? Converted `/workspace/k8s/base/configmap.yaml` to use `configMapGenerator` in `kustomization.yaml`
- ? Removed the static `/workspace/k8s/base/configmap.yaml` file
- ? Now overlays can properly merge configuration values

### 3. Namespace Creation Timing

**Problem:** When using `kubectl apply -f k8s/base/` directly, the namespace was created alongside other resources in parallel, causing some resources to fail because they referenced a namespace that wasn't ready yet.

**Solution:**
- ? Updated documentation to warn against using `kubectl apply -f k8s/base/` directly
- ? Emphasized using the deployment script or `kubectl apply -k k8s/overlays/[dev|prod]`
- ? Kustomize properly orders resource creation when using `-k` flag

## Changes Made

### File: `/workspace/k8s/base/kustomization.yaml`

**Before:**
```yaml
commonLabels:
  app: shopping-mart
  managed-by: kustomize

resources:
  - configmap.yaml
  # ... other resources
```

**After:**
```yaml
labels:
  - pairs:
      app: shopping-mart
      managed-by: kustomize

resources:
  # configmap.yaml removed - now using configMapGenerator
  # ... other resources

configMapGenerator:
  - name: shopping-mart-config
    literals:
      - APP_NAME=Shopping Mart System
      - DEBUG=False
      - ALGORITHM=HS256
      # ... all configuration values
```

### File: `/workspace/k8s/overlays/dev/kustomization.yaml`

**Before:**
```yaml
bases:
  - ../../base

commonLabels:
  environment: development

patchesStrategicMerge:
  - replica-patch.yaml
  - resource-patch.yaml
```

**After:**
```yaml
resources:
  - ../../base

labels:
  - pairs:
      environment: development

patches:
  - path: replica-patch.yaml
  - path: resource-patch.yaml
```

### File: `/workspace/k8s/overlays/prod/kustomization.yaml`

Same updates as dev overlay.

### File: `/workspace/k8s/README.md`

- ? Updated directory structure to reflect configMapGenerator instead of static configmap.yaml
- ? Added warning against using `kubectl apply -f k8s/base/` directly
- ? Emphasized proper deployment methods

## How to Deploy (Fixed)

### ? Correct Method 1: Using Deployment Script (Recommended)

```bash
./k8s/deploy.sh dev apply
```

### ? Correct Method 2: Using kubectl with -k flag

```bash
kubectl apply -k k8s/overlays/dev
```

### ? Incorrect Method (Don't Do This)

```bash
# This will NOT work with Kustomize features
kubectl apply -f k8s/base/
```

## Testing the Fixes

To verify the fixes work, run:

```bash
# Test kustomize build without applying
kubectl kustomize k8s/overlays/dev

# If no errors, deploy
./k8s/deploy.sh dev apply
```

You should no longer see:
- ? Deprecation warnings about `bases`, `commonLabels`, or `patchesStrategicMerge`
- ? ConfigMap merge errors
- ? Namespace timing errors

## Migration from Old ConfigMap

The configuration values from the old static ConfigMap have been preserved in the new `configMapGenerator`. The overlays (dev/prod) can now properly merge and override specific values:

**Dev Environment:**
- Overrides `DEBUG=True`
- Overrides `VITE_API_BASE_URL=http://localhost:8000/api/v1`

**Prod Environment:**
- Overrides `DEBUG=False`
- Overrides `VITE_API_BASE_URL=https://api.shopping-mart.example.com/api/v1`

## Next Steps

1. **Clean up any existing resources** (if previously deployed):
   ```bash
   kubectl delete namespace shopping-mart-dev
   # or
   ./k8s/deploy.sh dev delete
   ```

2. **Deploy with fixed configuration**:
   ```bash
   ./k8s/deploy.sh dev apply
   ```

3. **Verify deployment**:
   ```bash
   kubectl get all -n shopping-mart-dev
   kubectl get configmap -n shopping-mart-dev
   ```

## Summary

All Kustomize configuration issues have been resolved. The deployment should now work cleanly without warnings or errors. The configuration follows current Kustomize best practices and properly uses the newer field names and configMapGenerator feature.

? **Ready to deploy!**
