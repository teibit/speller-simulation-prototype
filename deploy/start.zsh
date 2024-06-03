#!/bin/zsh

# CLI entrypoint for the system.

# This script:
#   1, builds all the docker images anew, and
#   2, creates the Kubernetes deployment.
# Helpful stdout is produced by the modules themselves.

# Run from app/: ./deploy/start.zsh
# After running, manage through Docker Desktop.
# Observe the microservices come and go while collaborating asynchronously.
# Finish by running: ./deploy/stop.zsh

# Note that the server images are already handled by Kubernetes.

# Run on app directory
cd /Users/teibit/app || exit

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

# Start Kubernetes deployment
kubectl create -f deploy/k8s.yaml
