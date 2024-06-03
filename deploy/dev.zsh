#!/bin/zsh

# Full CLI stop-start-logs point for the system, mainly for development.
# It is useful when developing incremental changes in the overall system.

# Run from app/: ./deploy/dev.zsh

# Run on app directory
cd /Users/teibit/app || exit

# Remove Kubernetes deployment
kubectl delete deployment/simulation

# Remove images from docker
docker rmi -f inputter

docker rmi -f speller

docker rmi -f archiver-mysql
docker rmi -f archiver-postgres
docker rmi -f archiver-redis
docker rmi -f archiver-mongo

docker rmi -f observer-mysql
docker rmi -f observer-postgres
docker rmi -f observer-redis
docker rmi -f observer-mongo

docker rmi -f benchmarker

# Remove:
#   - all stopped containers
#   - all networks not used by at least one container
#   - all dangling images
#   - unused build cache
docker system prune --force --volumes

sleep 5

# Builds new images from their respective Dockerfiles
docker build --no-cache -qt inputter -f src/containers/inputter/Dockerfile .

docker build --no-cache -qt speller -f src/containers/speller/Dockerfile .

docker build --no-cache -qt archiver-mysql -f src/containers/archiver/MySQL.Dockerfile .
docker build --no-cache -qt archiver-postgres -f src/containers/archiver/Postgres.Dockerfile .
docker build --no-cache -qt archiver-redis -f src/containers/archiver/Redis.Dockerfile .
docker build --no-cache -qt archiver-mongo -f src/containers/archiver/Mongo.Dockerfile .

docker build --no-cache -qt observer-mysql -f src/containers/observer/MySQL.Dockerfile .
docker build --no-cache -qt observer-postgres -f src/containers/observer/Postgres.Dockerfile .
docker build --no-cache -qt observer-redis -f src/containers/observer/Redis.Dockerfile .
docker build --no-cache -qt observer-mongo -f src/containers/observer/Mongo.Dockerfile .

docker build --no-cache -qt benchmarker -f src/containers/benchmarker/Dockerfile .

clear

# Start Kubernetes deployment
kubectl create -f deploy/k8s.yaml
sleep 45
echo ''

# Show Kubernetes logs
kubectl get deployment
echo ''
kubectl get replicasets
echo ''
kubectl get pods
#echo ''
#kubectl describe pods
