#!/bin/bash

# Quick Rebuild Script with Options
# Provides multiple ways to rebuild and run the app

echo "🚀 Contact Manager - Quick Rebuild"
echo "=================================="
echo ""
echo "Choose an option:"
echo "1. 🔄 Rebuild app only (keeps databases running)"
echo "2. 🏗️  Rebuild app + restart databases"
echo "3. 🧹 Clean rebuild (remove old images)"
echo "4. 📋 Just run existing app (no rebuild)"
echo "5. 🛑 Stop all services"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "🔄 Rebuilding app container only..."
        docker compose stop contact-manager
        docker compose build contact-manager
        echo "🚀 Starting app interactively..."
        docker compose run --rm -it contact-manager
        ;;
    2)
        echo "🏗️  Rebuilding app and restarting databases..."
        docker compose down
        docker compose up -d mysql postgres mongodb
        echo "⏳ Waiting for databases to be ready..."
        sleep 15
        docker compose build contact-manager
        echo "🚀 Starting app interactively..."
        docker compose run --rm -it contact-manager
        ;;
    3)
        echo "🧹 Clean rebuild (removing old images)..."
        docker compose down
        docker compose build --no-cache contact-manager
        docker compose up -d mysql postgres mongodb
        echo "⏳ Waiting for databases to be ready..."
        sleep 15
        echo "🚀 Starting app interactively..."
        docker compose run --rm -it contact-manager
        ;;
    4)
        echo "📋 Running existing app..."
        if ! docker compose ps | grep -q "Up.*mysql"; then
            echo "⚠️  Starting databases first..."
            docker compose up -d mysql postgres mongodb
            sleep 10
        fi
        docker compose run --rm -it contact-manager
        ;;
    5)
        echo "🛑 Stopping all services..."
        docker compose down
        echo "✅ All services stopped."
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "✅ Operation completed!"
echo "💡 Run this script again anytime you need to rebuild or restart."
