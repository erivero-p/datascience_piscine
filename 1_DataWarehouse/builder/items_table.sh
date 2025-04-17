#!/bin/bash
set -e

TABLE_NAME="items"
CSV_PATH="../csv_data/item/item.csv"

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
    product_id INTEGER,
    category_id BIGINT,
    category_code VARCHAR(255),
    brand VARCHAR(255)
);
EOF

  # Load CSV
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy $TABLE_NAME FROM '$CSV_PATH' DELIMITER ',' CSV HEADER;"

  echo "Table '$TABLE_NAME' succesfully created."
fi
