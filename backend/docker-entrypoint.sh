#!/bin/bash
set -e

# Wait for postgres
echo "Waiting for postgres..."
while ! nc -z postgres 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Run migrations if needed
if [ "$RUN_MIGRATIONS" == "true" ]; then
  echo "Running database migrations..."
  uv run alembic upgrade head
fi

# Execute command
exec "$@"
