#!/bin/bash
set -e

TABLE_NAME="data_2022_oct"
CSV_PATH="/subject/customer/data_2022_oct.csv"

# Function to check if table already exists
function table_exists() {
  EXISTS=$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '$TABLE_NAME');")
  [ "$EXISTS" = "t" ]
}

if table_exists; then
  echo "'$TABLE_NAME' table already exists."
else
  echo "Creating '$TABLE_NAME' table..."

  # Create table
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF
    CREATE TABLE $TABLE_NAME (
    event_time TIMESTAMP NOT NULL,
    event_type VARCHAR(255),
    product_id INTEGER,
    price NUMERIC,
    user_id BIGINT,
    user_session UUID
);
EOF

  # Load CSV
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy $TABLE_NAME FROM '$CSV_PATH' DELIMITER ',' CSV HEADER;"

  echo "Table '$TABLE_NAME' succesfully created."
fi
