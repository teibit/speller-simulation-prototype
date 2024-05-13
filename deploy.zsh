#!/bin/zsh

# Run on app directory
cd /Users/teibit/app || exit

# Remove images from docker
docker rmi -f raw-topics-producer
docker rmi -f numbers-processor-consumer-producer
docker rmi -f dots-processor-consumer-producer
docker rmi -f processed-topics-consumer
docker rmi -f numeralia-db-manager

# Remove Kubernetes deployment
kubectl delete deployment/app-deployment

# Remove Kubernetes service
kubectl delete svc app-service

# Remove all dangling Docker images
docker image prune --force

# Builds new images from their respective Dockerfiles
cd raw-topics-producer-container || exit
docker build --no-cache -qt raw-topics-producer .

cd ../numbers-processor-consumer-producer-container || exit
docker build --no-cache -qt numbers-processor-consumer-producer .

cd ../dots-processor-consumer-producer-container || exit
docker build --no-cache -qt dots-processor-consumer-producer .

cd ../processed-topics-consumer-container || exit
docker build --no-cache -qt processed-topics-consumer .

cd ../numeralia-db-manager-container || exit
docker build --no-cache -qt numeralia-db-manager .

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
