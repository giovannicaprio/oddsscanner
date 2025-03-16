#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Starting MySQL Container ===${NC}"
docker-compose up -d

# Run the health check script
./oddsscanner_test_health.sh 