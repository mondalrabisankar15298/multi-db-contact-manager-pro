#!/bin/bash

# Quick Stop Script for Full Docker Application
echo "🛑 Stopping Contact Manager - Full Docker Application"
echo "====================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Nothing to stop."
    exit 1
fi

echo "🔍 Checking running containers..."

# Check if any containers are running
RUNNING_CONTAINERS=$(docker ps --filter "name=contact-" --format "table {{.Names}}\t{{.Status}}" | grep -v NAMES)

if [ -z "$RUNNING_CONTAINERS" ]; then
    echo "ℹ️  No Contact Manager containers are currently running."
    echo ""
    echo "✅ All services are already stopped!"
    exit 0
fi

echo "📋 Currently running Contact Manager containers:"
echo "$RUNNING_CONTAINERS"
echo ""

# Stop all services including those with profiles
echo "🧹 Stopping all services..."
echo "   - Contact Manager Application (Python)"
echo "   - MySQL Database"
echo "   - PostgreSQL Database" 
echo "   - MongoDB Database"
echo "   - Adminer (Database Admin Tool)"
echo ""

# Stop containers with profile first, then regular containers
echo "🛑 Stopping Contact Manager application..."
docker compose --profile full down

# Double-check and stop any remaining containers
echo "🔄 Ensuring all Contact Manager containers are stopped..."
docker compose down

# Stop any remaining contact-related containers manually
REMAINING=$(docker ps --filter "name=contact-" -q)
if [ ! -z "$REMAINING" ]; then
    echo "🧹 Stopping remaining containers manually..."
    docker stop $REMAINING
    docker rm $REMAINING
fi

# Clean up unused networks (optional)
echo "🧽 Cleaning up unused networks..."
docker network prune -f > /dev/null 2>&1

# Final verification
echo "🔍 Final verification..."
FINAL_CHECK=$(docker ps --filter "name=contact-" -q)

if [ -z "$FINAL_CHECK" ]; then
    echo ""
    echo "✅ All Contact Manager services stopped successfully!"
    echo ""
    echo "📊 Summary:"
    echo "   🛑 All containers: Stopped and removed"
    echo "   🌐 Networks: Cleaned up"
    echo "   💾 Data volumes: Preserved (not removed)"
    echo ""
    echo "💡 To start again, run:"
    echo "   ./start-docker-app.sh"
    echo ""
    echo "🗑️  To completely remove everything including data:"
    echo "   docker compose --profile full down -v"
    echo "   docker system prune -f"
else
    echo ""
    echo "⚠️  Some containers may still be running:"
    docker ps --filter "name=contact-"
    echo ""
    echo "💡 You may need to stop them manually:"
    echo "   docker stop \$(docker ps --filter \"name=contact-\" -q)"
fi
