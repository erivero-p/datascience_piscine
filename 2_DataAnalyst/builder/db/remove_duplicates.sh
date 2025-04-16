#!/bin/bash
set -e

TABLE_NAME="customers"

echo "Removing near-duplicate rows from '$TABLE_NAME'..."

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF
WITH duplicates AS (
  SELECT c1.ctid
  FROM $TABLE_NAME c1
  JOIN $TABLE_NAME c2
    ON c1.ctid <> c2.ctid
    AND c1.event_type = c2.event_type
    AND c1.product_id = c2.product_id
    AND c1.price = c2.price
    AND c1.user_id = c2.user_id
    AND c1.user_session = c2.user_session
    AND ABS(EXTRACT(EPOCH FROM (c1.event_time - c2.event_time))) <= 1
  WHERE c1.ctid > c2.ctid
)
DELETE FROM $TABLE_NAME
WHERE ctid IN (SELECT ctid FROM duplicates);
EOF

echo "Duplicates removed from '$TABLE_NAME'."
