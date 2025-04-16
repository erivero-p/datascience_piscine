#!/bin/bash
set -e

CSV_DIR="/csv_data/customer"
TABLE_NAME="customers"

# Check if table already exists
function table_exists() {
  EXISTS=$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '$TABLE_NAME');")
  [ "$EXISTS" = "t" ]
}

if table_exists; then
  echo "Table '$TABLE_NAME' already exists. Skipping creation."
else
  echo "Creating table '$TABLE_NAME'..."

  # Create an unic table
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

  echo "Table '$TABLE_NAME' created."
fi

# Import all csv to the table`
for csv_file in "$CSV_DIR"/*.csv; do
  echo "Importing $csv_file..."
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy $TABLE_NAME FROM '$csv_file' DELIMITER ',' CSV HEADER;"
done

echo "All data loaded into '$TABLE_NAME'."
