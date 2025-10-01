#!/bin/bash

# Quick Start Script for Full Docker Application
echo "🚀 Starting Contact Manager - Full Docker Application"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "🐳 Starting all services in Docker..."
echo "   - Contact Manager Application (Python)"
echo "   - MySQL Database"
echo "   - PostgreSQL Database"
echo "   - MongoDB Database"
echo "   - Adminer (Database Admin Tool)"
echo ""

# Stop any existing containers first
echo "🧹 Stopping any existing containers..."
docker compose down > /dev/null 2>&1

# Start the full application in detached mode
echo "🏗️  Building and starting containers..."
docker compose --profile full up --build -d

# Wait for containers to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check if containers are running
if docker compose ps | grep -q "contact-manager.*Up"; then
    echo ""
    echo "✅ Application started successfully!"
    echo ""
    echo "🌐 Access Points:"
    echo "   📱 Contact Manager App: Ready (see connection below)"
    echo "   🗄️  MySQL: localhost:3306"
    echo "   🐘 PostgreSQL: localhost:5433"
    echo "   🍃 MongoDB: localhost:27017"
    echo "   🔧 Adminer: http://localhost:8050"
    echo ""
    echo "🔗 How to connect to your Contact Manager:"
    echo "   Option 1 - Attach to running container:"
    echo "   docker compose exec contact-manager /bin/bash"
    echo ""
    echo "   Option 2 - View logs:"
    echo "   docker compose logs -f contact-manager"
    echo ""
    echo "   Option 3 - Stop everything:"
    echo "   docker compose down"
    echo ""
    echo "🚀 Connecting to Contact Manager now..."
    echo ""

    # Attach to the contact manager container for interactive use
    docker compose exec contact-manager python main.py
else
    echo "❌ Failed to start application. Check logs:"
    docker compose logs
    exit 1
fi
