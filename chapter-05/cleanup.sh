#!/bin/bash

# Chapter 05 Environment Cleanup Script
# This script completely shuts down and cleans all Docker resources for Chapter 05

set -e  # Exit on any error

echo "Starting Chapter 05 cleanup..."

echo "Stopping and removing main services..."
docker-compose down --volumes --remove-orphans

echo "Stopping and removing Airflow services..."
docker-compose -f airflow.yaml down --volumes --remove-orphans

echo "Cleaning up Docker volumes..."
docker volume prune -f

echo "Cleaning up Docker networks..."
docker network prune -f

echo "Cleaning up stopped containers..."
docker container prune -f

echo "Cleaning up unused images..."
docker image prune -f

echo "Verifying cleanup..."
echo "Running containers:"
docker ps --format "table {{.Names}}\t{{.Status}}"

echo "Chapter 05 volumes:"
docker volume ls | grep chapter-05 || echo "No chapter-05 volumes found"

echo "Chapter 05 networks:"
docker network ls | grep chapter-05 || echo "No chapter-05 networks found"

echo "Chapter 05 cleanup completed!"
echo "To remove ALL unused images (more aggressive), run: docker image prune -a -f"