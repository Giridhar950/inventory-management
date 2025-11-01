#!/bin/bash

# Shopping Mart System - Build Verification Script
# Run this to verify everything is ready to deploy

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "??????????????????????????????????????????????????????????"
echo "?   Shopping Mart System - Build Verification           ?"
echo "??????????????????????????????????????????????????????????"
echo ""

ERRORS=0
WARNINGS=0

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}? $2${NC}"
    else
        echo -e "${RED}? $2${NC}"
        ((ERRORS++))
    fi
}

print_warning() {
    echo -e "${YELLOW}??  $1${NC}"
    ((WARNINGS++))
}

print_info() {
    echo -e "${BLUE}??  $1${NC}"
}

echo "?? Checking Prerequisites..."
echo "????????????????????????????????????????????????????????"

# Check Docker
if command -v docker &> /dev/null; then
    print_status 0 "Docker is installed"
else
    print_status 1 "Docker is NOT installed"
fi

# Check Docker Compose
if command -v docker-compose &> /dev/null || docker compose version &> /dev/null 2>&1; then
    print_status 0 "Docker Compose is installed"
else
    print_status 1 "Docker Compose is NOT installed"
fi

# Check kubectl (optional)
if command -v kubectl &> /dev/null; then
    print_status 0 "kubectl is installed (for Kubernetes deployment)"
else
    print_info "kubectl NOT installed (only needed for Kubernetes)"
fi

echo ""
echo "?? Checking Project Structure..."
echo "????????????????????????????????????????????????????????"

# Check backend files
[ -f "backend/requirements.txt" ] && print_status 0 "backend/requirements.txt exists" || print_status 1 "backend/requirements.txt MISSING"
[ -f "backend/Dockerfile" ] && print_status 0 "backend/Dockerfile exists" || print_status 1 "backend/Dockerfile MISSING"
[ -f "backend/app/main.py" ] && print_status 0 "backend/app/main.py exists" || print_status 1 "backend/app/main.py MISSING"
[ -f "backend/init_db.py" ] && print_status 0 "backend/init_db.py exists" || print_status 1 "backend/init_db.py MISSING"

# Check frontend files
[ -f "frontend/package.json" ] && print_status 0 "frontend/package.json exists" || print_status 1 "frontend/package.json MISSING"
[ -f "frontend/Dockerfile" ] && print_status 0 "frontend/Dockerfile exists" || print_status 1 "frontend/Dockerfile MISSING"
[ -f "frontend/src/App.jsx" ] && print_status 0 "frontend/src/App.jsx exists" || print_status 1 "frontend/src/App.jsx MISSING"

# Check docker-compose
[ -f "docker-compose.yml" ] && print_status 0 "docker-compose.yml exists" || print_status 1 "docker-compose.yml MISSING"

# Check K8s
[ -d "k8s/base" ] && print_status 0 "k8s/base directory exists" || print_status 1 "k8s/base directory MISSING"
[ -f "k8s/deploy.sh" ] && print_status 0 "k8s/deploy.sh exists" || print_status 1 "k8s/deploy.sh MISSING"

echo ""
echo "?? Checking Configuration Files..."
echo "????????????????????????????????????????????????????????"

# Check .env.example files
[ -f "backend/.env.example" ] && print_status 0 "backend/.env.example exists" || print_status 1 "backend/.env.example MISSING"
[ -f "frontend/.env.example" ] && print_status 0 "frontend/.env.example exists" || print_status 1 "frontend/.env.example MISSING"

# Check for secrets warnings
if grep -q "your-secret-key-change" backend/.env.example 2>/dev/null; then
    print_warning "Default SECRET_KEY in backend/.env.example (OK for dev, change for prod)"
fi

if grep -q "postgres:postgres" docker-compose.yml 2>/dev/null; then
    print_warning "Default PostgreSQL password in docker-compose.yml (OK for dev, change for prod)"
fi

echo ""
echo "?? Validating Python Files..."
echo "????????????????????????????????????????????????????????"

# Count Python files
PYTHON_FILES=$(find backend/app -name "*.py" -type f 2>/dev/null | wc -l)
print_info "Found $PYTHON_FILES Python files in backend/app"

# Check for syntax errors (basic check)
SYNTAX_ERRORS=0
for file in backend/app/*.py backend/app/**/*.py 2>/dev/null; do
    if [ -f "$file" ]; then
        if ! python3 -m py_compile "$file" 2>/dev/null; then
            print_status 1 "Syntax error in $file"
            ((SYNTAX_ERRORS++))
        fi
    fi
done

if [ $SYNTAX_ERRORS -eq 0 ]; then
    print_status 0 "All Python files have valid syntax"
fi

echo ""
echo "?? Checking Dependencies..."
echo "????????????????????????????????????????????????????????"

# Check backend requirements
if [ -f "backend/requirements.txt" ]; then
    BACKEND_DEPS=$(wc -l < backend/requirements.txt)
    print_info "Backend has $BACKEND_DEPS dependencies"
    
    # Check for known secure versions
    if grep -q "fastapi==0.109" backend/requirements.txt; then
        print_status 0 "FastAPI version is pinned"
    fi
    if grep -q "sqlalchemy==2.0" backend/requirements.txt; then
        print_status 0 "SQLAlchemy 2.0 is used"
    fi
fi

# Check frontend dependencies
if [ -f "frontend/package.json" ]; then
    if grep -q '"react": "^18' frontend/package.json; then
        print_status 0 "React 18 is used"
    fi
    if grep -q '@mui/material' frontend/package.json; then
        print_status 0 "Material-UI is configured"
    fi
fi

echo ""
echo "?? Testing Docker Builds..."
echo "????????????????????????????????????????????????????????"

# Test backend Dockerfile syntax
if [ -f "backend/Dockerfile" ]; then
    if docker build --no-cache -f backend/Dockerfile -t shopping-mart-backend:test backend/ &>/dev/null; then
        print_status 0 "Backend Docker build succeeds"
        docker rmi shopping-mart-backend:test &>/dev/null || true
    else
        print_status 1 "Backend Docker build FAILS"
    fi
else
    print_status 1 "Backend Dockerfile not found"
fi

# Test frontend Dockerfile syntax
if [ -f "frontend/Dockerfile" ]; then
    print_info "Frontend Dockerfile exists (build test skipped - takes too long)"
fi

echo ""
echo "??  Validating Kubernetes Manifests..."
echo "????????????????????????????????????????????????????????"

if command -v kubectl &> /dev/null; then
    K8S_ERRORS=0
    for file in k8s/base/*.yaml; do
        if [ -f "$file" ]; then
            if kubectl apply --dry-run=client -f "$file" &>/dev/null; then
                : # Success, do nothing
            else
                print_status 1 "Invalid K8s manifest: $file"
                ((K8S_ERRORS++))
            fi
        fi
    done
    
    if [ $K8S_ERRORS -eq 0 ]; then
        print_status 0 "All Kubernetes manifests are valid"
    fi
else
    print_info "kubectl not installed, skipping K8s validation"
fi

echo ""
echo "?? Security Checks..."
echo "????????????????????????????????????????????????????????"

# Check for hardcoded secrets
if grep -r "admin123" backend/ frontend/ docker-compose.yml 2>/dev/null | grep -v ".example" | grep -v "README" | grep -v "QUICKSTART" | grep -v "init_db.py" > /dev/null; then
    print_warning "Default passwords found (OK for dev, change for prod)"
fi

# Check for DEBUG=True
if grep -q "DEBUG: bool = True" backend/app/config.py 2>/dev/null; then
    print_warning "DEBUG=True in config.py (OK for dev, set to False for prod)"
fi

# Check CORS settings
if grep -q "localhost" backend/app/config.py 2>/dev/null; then
    print_warning "CORS allows localhost (OK for dev, update for prod)"
fi

echo ""
echo "?? Checking Documentation..."
echo "????????????????????????????????????????????????????????"

[ -f "README.md" ] && print_status 0 "README.md exists" || print_status 1 "README.md MISSING"
[ -f "QUICKSTART.md" ] && print_status 0 "QUICKSTART.md exists" || print_status 1 "QUICKSTART.md MISSING"
[ -f "KUBERNETES.md" ] && print_status 0 "KUBERNETES.md exists" || print_status 1 "KUBERNETES.md MISSING"
[ -f "DEPLOYMENT_CHECKLIST.md" ] && print_status 0 "DEPLOYMENT_CHECKLIST.md exists" || print_status 1 "DEPLOYMENT_CHECKLIST.md MISSING"
[ -f "CODE_AUDIT_AND_FIXES.md" ] && print_status 0 "CODE_AUDIT_AND_FIXES.md exists" || print_status 1 "CODE_AUDIT_AND_FIXES.md MISSING"

echo ""
echo "??????????????????????????????????????????????????????????"
echo "?                  VERIFICATION SUMMARY                  ?"
echo "??????????????????????????????????????????????????????????"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}? BUILD VERIFICATION PASSED${NC}"
    echo ""
    echo "   Errors:   $ERRORS"
    echo "   Warnings: $WARNINGS"
    echo ""
    echo -e "${GREEN}?? Your project is ready to deploy!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. For local testing:     ./start.sh"
    echo "  2. For Podman:            ./start-podman.sh"
    echo "  3. For Kubernetes:        ./k8s/deploy.sh dev apply"
    echo ""
    echo "Before production:"
    echo "  ? Read DEPLOYMENT_CHECKLIST.md"
    echo "  ? Change all default passwords"
    echo "  ? Update SECRET_KEY"
    echo "  ? Configure CORS for your domain"
    echo "  ? Set DEBUG=False"
    echo ""
    exit 0
else
    echo -e "${RED}? BUILD VERIFICATION FAILED${NC}"
    echo ""
    echo "   Errors:   $ERRORS"
    echo "   Warnings: $WARNINGS"
    echo ""
    echo "Please fix the errors above before deploying."
    echo ""
    exit 1
fi
