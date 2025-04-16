FROM postgres:15

# Copy the entrypoint and table scripts
COPY entrypoint.sh /entrypoint.sh
COPY customers_table.sh /create_table.sh
COPY remove_duplicates.sh /remove_duplicates.sh

# Change execution permissions for the scripts
RUN chmod +x /entrypoint.sh /create_table.sh /remove_duplicates.sh

# Set the custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]