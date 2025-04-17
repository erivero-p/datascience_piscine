FROM postgres:15

# Copy the entrypoint and table scripts
COPY entrypoint.sh /entrypoint.sh
COPY customers_tables.sh /customers_tables.sh
COPY items_table.sh /items_table.sh

# Change execution permissions for the scripts
RUN chmod +x /entrypoint.sh /items_table.sh /customers_tables.sh

# Set the custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]