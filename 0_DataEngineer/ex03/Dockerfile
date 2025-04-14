FROM postgres:15

# Copy the entrypoint and table scripts
COPY entrypoint.sh /entrypoint.sh
COPY table.sh /table.sh

# Change execution permissions for the scripts
RUN chmod +x /entrypoint.sh /table.sh

# Set the custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]