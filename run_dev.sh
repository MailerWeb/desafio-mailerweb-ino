#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}UV not found. Installing...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="/root/.local/bin:$PATH"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env from .env.example${NC}"
    cp .env.example .env
fi

echo -e "${GREEN}Starting development environment...${NC}"
echo ""

# Function to cleanup on exit
cleanup() {
    echo -e "${YELLOW}Stopping services...${NC}"
    pkill -P $$ 2>/dev/null || true
}

trap cleanup EXIT

# Check if running with specific service
if [ "$1" == "api" ]; then
    echo -e "${GREEN}Starting API only${NC}"
    uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
elif [ "$1" == "worker" ]; then
    echo -e "${GREEN}Starting Worker only${NC}"
    uv run celery -A celery_app worker --loglevel=info
elif [ "$1" == "redis" ]; then
    echo -e "${GREEN}Starting Redis${NC}"
    docker run --rm -p 6379:6379 redis:7-alpine
elif [ "$1" == "postgres" ]; then
    echo -e "${GREEN}Starting PostgreSQL${NC}"
    docker run --rm \
      -e POSTGRES_USER=postgres \
      -e POSTGRES_PASSWORD=postgres \
      -e POSTGRES_DB=booking_db \
      -p 5432:5432 \
      -v postgres_dev:/var/lib/postgresql/data \
      postgres:15-alpine
else
    echo -e "${GREEN}Starting all services...${NC}"
    echo -e "${YELLOW}Make sure PostgreSQL and Redis are running!${NC}"
    echo ""
    
    # Start API and Worker in parallel
    echo -e "${GREEN}Starting API...${NC}"
    uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
    API_PID=$!
    
    echo -e "${GREEN}Starting Worker...${NC}"
    uv run celery -A celery_app worker --loglevel=info &
    WORKER_PID=$!
    
    echo -e "${GREEN}Services running (PIDs: API=$API_PID, Worker=$WORKER_PID)${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
    
    wait
fi
