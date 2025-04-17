#!/bin/bash
set -e

TABLE_NAME="customers"

# Dynamically fetch table names that match the pattern 'data_%'
DATA_TABLES=$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT table_name FROM information_schema.tables WHERE table_name LIKE 'data_%' AND table_schema = 'public';")
# Check if table already exists
function table_exists() {
  EXISTS=$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '$TABLE_NAME');")
  [ "$EXISTS" = "t" ]
}

if table_exists; then
  echo "Table '$TABLE_NAME' already exists. Skipping creation."
else
  echo "Creating table '$TABLE_NAME'..."

  # Create the customers table
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

# Merge data from the dynamically fetched tables into the customers table
for data_table in $DATA_TABLES; do
  echo "Merging data from '$data_table' into '$TABLE_NAME'..."
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF
INSERT INTO $TABLE_NAME (event_time, event_type, product_id, price, user_id, user_session)
SELECT event_time, event_type, product_id, price, user_id, user_session
FROM $data_table;
EOF
done

echo "All data merged into '$TABLE_NAME'."