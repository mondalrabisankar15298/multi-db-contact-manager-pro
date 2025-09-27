#!/bin/bash

# Quick Start Script for Databases Only (Run App Locally)
echo "🗄️  Starting Databases Only - Run App Locally"
echo "=============================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "🐳 Starting database services in Docker..."
echo "   - MySQL Database (port 3306)"
echo "   - PostgreSQL Database (port 5432)"
echo "   - MongoDB Database (port 27017)"
echo "   - Adminer (Database Admin Tool - port 8080)"
echo ""

# Start only databases
docker compose up -d mysql postgres mongodb adminer

echo "✅ Databases started successfully!"
echo ""
echo "🎯 Now you can run your application locally:"
echo "   python main.py"
echo ""
echo "🌐 Database Admin Tool available at:"
echo "   http://localhost:8080"
echo ""
echo "🛑 To stop databases:"
echo "   docker compose down"
