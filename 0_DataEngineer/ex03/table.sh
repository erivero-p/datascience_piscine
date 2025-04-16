#!/bin/bash
set -e

CSV_DIR="/csv_data/customer"

# Function to check if a table already exists
function table_exists() {
  local table_name=$1
  EXISTS=$(psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -tAc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '$table_name');")
  [ "$EXISTS" = "t" ]
}

# Process each CSV file in the directory recursively
find "$CSV_DIR" -type f -name "*.csv" | while read -r csv_file; do
  # Extract the table name from the CSV file name (remove directory path and extension)
  TABLE_NAME=$(basename "$csv_file" .csv)

  if table_exists "$TABLE_NAME"; then
    echo "Table '$TABLE_NAME' already exists. Skipping..."
  else
    echo "Creating table '$TABLE_NAME' from file '$csv_file'..."

    # Create table dynamically based on the CSV file structure
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

    # Load data from the CSV file into the table
    psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy $TABLE_NAME FROM '$csv_file' DELIMITER ',' CSV HEADER;"

    echo "Table '$TABLE_NAME' successfully created and populated."
  fi
done