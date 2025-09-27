#!/bin/bash

# Docker Contact Manager - Full Application Runner
echo "🐳 Starting Contact Manager in Docker..."

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo "❌ Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to stop existing containers
cleanup() {
    echo "🧹 Cleaning up existing containers..."
    docker compose down
}

# Function to start full application
start_full() {
    echo "🚀 Starting full Contact Manager application..."
    echo "📊 This includes:"
    echo "   - Contact Manager Application (Python)"
    echo "   - MySQL Database"
    echo "   - PostgreSQL Database" 
    echo "   - MongoDB Database"
    echo ""
    
    # Build and start all services
    docker compose --profile full up --build
}

# Function to start just databases
start_databases() {
    echo "🗄️  Starting only database services..."
    docker compose up -d mysql postgres mongodb
    echo "✅ Databases started. You can run your app locally with:"
    echo "   python main.py"
}

# Function to show status
show_status() {
    echo "📊 Docker Container Status:"
    docker compose ps
}

# Function to show logs
show_logs() {
    if [ -n "$1" ]; then
        echo "📋 Logs for $1:"
        docker compose logs --tail=50 -f "$1"
    else
        echo "📋 All container logs:"
        docker compose logs --tail=50 -f
    fi
}

# Function to enter application container
enter_app() {
    echo "🐳 Entering application container..."
    docker compose exec contact-manager /bin/bash
}

# Main script logic
case "$1" in
    "full")
        check_docker
        cleanup
        start_full
        ;;
    "databases"|"db")
        check_docker
        start_databases
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs "$2"
        ;;
    "shell"|"bash")
        enter_app
        ;;
    "stop")
        cleanup
        ;;
    "restart")
        check_docker
        cleanup
        start_full
        ;;
    *)
        echo "🐳 Contact Manager Docker Runner"
        echo "================================"
        echo ""
        echo "Usage: $0 {command}"
        echo ""
        echo "Commands:"
        echo "  full        - Start complete application in Docker (app + databases)"
        echo "  databases   - Start only databases (run app locally)"
        echo "  status      - Show container status"
        echo "  logs [name] - Show logs (optional: specify container name)"
        echo "  shell       - Enter application container shell"
        echo "  stop        - Stop all containers"
        echo "  restart     - Restart full application"
        echo ""
        echo "Examples:"
        echo "  $0 full                    # Run everything in Docker"
        echo "  $0 databases               # Just databases, app runs locally"
        echo "  $0 logs contact-manager    # Show app logs"
        echo "  $0 shell                   # Enter app container"
        echo ""
        echo "🎯 For full Docker deployment, use: $0 full"
        ;;
esac
