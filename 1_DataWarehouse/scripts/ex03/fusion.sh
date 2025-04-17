#!/bin/bash
set -e

CUSTOMERS_TABLE="customers"
ITEMS_TABLE="items"
TMP_TABLE="customers_enriched"

echo "Fusing '$CUSTOMERS_TABLE' with '$ITEMS_TABLE'..."


psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF

CREATE TABLE $TMP_TABLE AS
SELECT 
  c.event_time,
  c.event_type,
  c.product_id,
  c.price,
  c.user_id,
  c.user_session,
  i.category_id,
  i.category_code,
  i.brand
FROM $CUSTOMERS_TABLE c
LEFT JOIN $ITEMS_TABLE i ON c.product_id = i.product_id;

DROP TABLE $CUSTOMERS_TABLE;
ALTER TABLE $TMP_TABLE RENAME TO $CUSTOMERS_TABLE;
EOF

echo "Fusion complete. '$CUSTOMERS_TABLE' now enriched with item data."