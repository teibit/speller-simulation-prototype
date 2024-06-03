#!/bin/zsh

# CLI logs point for the system.

# This script shows various logs from the system.

# Run from app/: ./deploy/logs.zsh

# Show Kubernetes logs
kubectl get deployment
echo ''
kubectl get replicasets
echo ''
kubectl get pods
