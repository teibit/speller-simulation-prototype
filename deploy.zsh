#!/bin/zsh

# Run on app directory
cd /Users/teibit/app || exit

# Remove images from docker
docker rmi -f kafka-producer:latest
docker rmi -f kafka-consumer:latest

# Remove Kubernetes deployments
kubectl delete deployment/app-deployment

# Remove Kubernetes services
kubectl delete svc app-service

# Remove all dangling Docker images
docker image prune --force

# Builds new images from their respective Dockerfiles
cd kafka-producer-container || exit
docker build --no-cache -qt kafka-producer .

cd ../kafka-consumer-container || exit
docker build --no-cache -qt kafka-consumer .

cd .. || exit
clear

# Start Kubernetes deployment
kubectl create -f ./kubernetes-deployment-config.yaml
sleep 30
echo ''

# Show results
kubectl get deployment
echo ''
kubectl get services
echo ''
kubectl get pods
