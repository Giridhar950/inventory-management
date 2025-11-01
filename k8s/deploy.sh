#!/bin/bash

# Shopping Mart System - Kubernetes Deployment Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "??????????????????????????????????????????????????????????"
echo "?   Shopping Mart System - Kubernetes Deployment        ?"
echo "??????????????????????????????????????????????????????????"
echo ""

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}? kubectl is not installed. Please install kubectl first.${NC}"
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}? Cannot connect to Kubernetes cluster. Check your kubeconfig.${NC}"
    exit 1
fi

echo -e "${GREEN}? Connected to Kubernetes cluster${NC}"
echo ""

# Parse arguments
ENVIRONMENT="${1:-dev}"
ACTION="${2:-apply}"

if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "prod" ]]; then
    echo -e "${RED}Invalid environment: $ENVIRONMENT${NC}"
    echo "Usage: $0 [dev|prod] [apply|delete]"
    exit 1
fi

if [[ "$ACTION" != "apply" && "$ACTION" != "delete" ]]; then
    echo -e "${RED}Invalid action: $ACTION${NC}"
    echo "Usage: $0 [dev|prod] [apply|delete]"
    exit 1
fi

echo -e "${YELLOW}Environment: $ENVIRONMENT${NC}"
echo -e "${YELLOW}Action: $ACTION${NC}"
echo ""

# Confirm production deployment
if [[ "$ENVIRONMENT" == "prod" ]]; then
    echo -e "${YELLOW}??  WARNING: You are about to $ACTION to PRODUCTION!${NC}"
    read -p "Are you sure? (yes/no): " confirm
    if [[ "$confirm" != "yes" ]]; then
        echo "Deployment cancelled."
        exit 0
    fi
fi

# Check if using kustomize or kubectl
if command -v kustomize &> /dev/null; then
    echo -e "${GREEN}? Using kustomize${NC}"
    USE_KUSTOMIZE=true
else
    echo -e "${YELLOW}??  kustomize not found, using kubectl with -k flag${NC}"
    USE_KUSTOMIZE=false
fi

# Deploy using kustomize
if [[ "$ACTION" == "apply" ]]; then
    echo ""
    echo "?? Deploying Shopping Mart System to $ENVIRONMENT..."
    echo ""
    
    if [[ "$USE_KUSTOMIZE" == "true" ]]; then
        kustomize build k8s/overlays/$ENVIRONMENT | kubectl apply -f -
    else
        kubectl apply -k k8s/overlays/$ENVIRONMENT
    fi
    
    echo ""
    echo -e "${GREEN}? Deployment initiated${NC}"
    echo ""
    
    # Wait for deployments
    echo "? Waiting for deployments to be ready..."
    
    if [[ "$ENVIRONMENT" == "dev" ]]; then
        NAMESPACE="shopping-mart-dev"
        PREFIX="dev-"
    else
        NAMESPACE="shopping-mart-prod"
        PREFIX="prod-"
    fi
    
    kubectl wait --for=condition=available --timeout=300s \
        deployment/${PREFIX}postgres \
        deployment/${PREFIX}redis \
        deployment/${PREFIX}backend \
        deployment/${PREFIX}frontend \
        -n $NAMESPACE || true
    
    echo ""
    echo -e "${GREEN}? Deployments are ready!${NC}"
    echo ""
    
    # Run database initialization job
    echo "???  Initializing database..."
    kubectl delete job ${PREFIX}init-database -n $NAMESPACE 2>/dev/null || true
    sleep 2
    
    if [[ "$USE_KUSTOMIZE" == "true" ]]; then
        kustomize build k8s/overlays/$ENVIRONMENT | kubectl apply -f - --selector=component=init
    else
        kubectl apply -k k8s/overlays/$ENVIRONMENT --selector=component=init
    fi
    
    echo "? Waiting for database initialization..."
    kubectl wait --for=condition=complete --timeout=120s job/${PREFIX}init-database -n $NAMESPACE || echo "Job may have already completed"
    
    echo ""
    echo "??????????????????????????????????????????????????????????"
    echo "?   ? Shopping Mart System deployed successfully!       ?"
    echo "??????????????????????????????????????????????????????????"
    echo ""
    
    # Show status
    echo "?? Deployment Status:"
    kubectl get pods -n $NAMESPACE
    echo ""
    
    echo "?? Services:"
    kubectl get svc -n $NAMESPACE
    echo ""
    
    echo "?? Ingress:"
    kubectl get ingress -n $NAMESPACE
    echo ""
    
    echo "?? To view logs:"
    echo "   kubectl logs -f deployment/${PREFIX}backend -n $NAMESPACE"
    echo "   kubectl logs -f deployment/${PREFIX}frontend -n $NAMESPACE"
    echo ""
    
    echo "?? To check status:"
    echo "   kubectl get all -n $NAMESPACE"
    echo ""
    
    # Port forwarding instructions
    echo "?? To access locally (port-forward):"
    echo "   Frontend:  kubectl port-forward svc/${PREFIX}frontend-service 3000:3000 -n $NAMESPACE"
    echo "   Backend:   kubectl port-forward svc/${PREFIX}backend-service 8000:8000 -n $NAMESPACE"
    echo ""

elif [[ "$ACTION" == "delete" ]]; then
    echo ""
    echo "???  Deleting Shopping Mart System from $ENVIRONMENT..."
    echo ""
    
    if [[ "$USE_KUSTOMIZE" == "true" ]]; then
        kustomize build k8s/overlays/$ENVIRONMENT | kubectl delete -f -
    else
        kubectl delete -k k8s/overlays/$ENVIRONMENT
    fi
    
    echo ""
    echo -e "${GREEN}? Resources deleted${NC}"
    echo ""
fi
