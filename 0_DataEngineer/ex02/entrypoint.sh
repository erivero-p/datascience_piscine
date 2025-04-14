#!/bin/bash
set -e

# Call the original PostgreSQL entrypoint script to initialize the database
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to be ready
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting Postgress to be ready..."
  sleep 2
done

# Run the custom script to create the table and load data
echo "Creating table and loading data..."
./table.sh

# Keep the container running
wait -n