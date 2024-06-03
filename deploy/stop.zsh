#!/bin/zsh

# CLI exit point for the system.

# This script:
#   1. forcefully deletes all:
#     1.1 containers,
#     1.2 docker images, and
#     1.3 dangling docker images.
#   2. deletes the Kubernetes deployment and related service.
# Helpful stdout is produced by the modules themselves.

# Run from app/: ./deploy/stop.zsh
# After running, notice the changes in Docker Desktop.

# Note that the server images are already handled by Kubernetes.

# Remove Kubernetes deployment
kubectl delete deployment/simulation

# Remove images from docker
docker rmi -f inputter

docker rmi -f speller

docker rmi -f archiver

docker rmi -f observer-mysql
docker rmi -f observer-postgres
docker rmi -f observer-redis
docker rmi -f observer-mongo

docker rmi -f benchmarker

# Remove:
#   - all stopped containers
#   - all networks not used by at least one container
#   - all dangling images
#   - all anonymous volumes
#   - unused build cache
docker system prune --force --volumes
