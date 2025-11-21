#!/bin/bash

# Simple App Runner
# Rebuilds and runs the app with minimal output

echo "🔄 Rebuilding and starting Contact Manager..."

# Ensure databases are running
docker compose up -d mysql postgres mongodb > /dev/null 2>&1

# Rebuild and run app
docker compose build contact-manager > /dev/null 2>&1
docker compose run --rm -it contact-manager
