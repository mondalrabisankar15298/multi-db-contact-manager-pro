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

# Start the full application
docker compose --profile full up --build

echo ""
echo "🎉 Application stopped. All containers have been shut down."
