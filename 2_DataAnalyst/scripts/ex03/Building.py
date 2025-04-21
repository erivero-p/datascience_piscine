import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Establish a connection to the PostgreSQL database using environment variables
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),  # Database host
    database=os.getenv("DB_NAME"),  # Database name
    user=os.getenv("DB_USER"),  # Database user
    password=os.getenv("DB_PASS")  # Database password
)

# SQL query to calculate the frequency of orders for each user and group by frequency
query_frequency = """
SELECT frequency, COUNT(*) AS customer_count
FROM (
    SELECT user_id, COUNT(*) AS frequency  -- Calculate the number of orders (frequency) for each user
    FROM customers
    WHERE event_type = 'purchase'  -- Only consider 'purchase' events
    GROUP BY user_id  -- Group by user_id to calculate the frequency of orders per user
) AS subquery
GROUP BY frequency  -- Group by the frequency of orders
ORDER BY frequency;  -- Sort the results by frequency in ascending order
"""

# Execute the query and load the results into a Pandas DataFrame
df_frequency = pd.read_sql(query_frequency, conn)

# Define bin edges to group frequencies into ranges (e.g., 0-5, 6-10, etc.)
bin_edges_frequency = list(range(0, 41, 5))  # Create bins: 0-5, 6-10, ..., 36-40
df_frequency['frequency_bin'] = pd.cut(df_frequency['frequency'], bins=bin_edges_frequency, right=False)  # Assign each frequency to a bin

# Aggregate the customer counts for each bin
df_frequency_binned = df_frequency.groupby('frequency_bin')['customer_count'].sum().reset_index()

# Replace bin ranges with custom labels (e.g., 0, 5, 10, ...)
df_frequency_binned['frequency_bin_label'] = bin_edges_frequency[1:]  # Use the upper bounds of the bins as labels (e.g., 5, 10, 15, ...)

# Plot the bar chart for order frequency
plt.figure(figsize=(10, 6))  # Set the figure size
plt.bar(
    df_frequency_binned['frequency_bin_label'],  # Use the custom bin labels for the x-axis
    df_frequency_binned['customer_count'],  # Use the aggregated customer counts for the y-axis
    color='skyblue',  # Set the bar color
    width=4  # Set the width of the bars
)
plt.title('Number of Customers by Order Frequency')  # Set the chart title
plt.xlabel('frequency')  # Label for the x-axis
plt.ylabel('customers')  # Label for the y-axis
plt.xticks(bin_edges_frequency[1:], rotation=45)  # Set x-axis ticks to the bin labels and rotate them for better readability
plt.tight_layout()  # Adjust the layout to prevent overlapping elements
plt.savefig("./scripts/ex03/bar_chart_order_frequency_binned.png")  # Save the chart as a PNG file
plt.show()  # Display the chart

# SQL query to calculate total spending by each customer and group by spending
query_spending = """
SELECT total_spent, COUNT(*) AS customer_count
FROM (
    SELECT user_id, SUM(price) AS total_spent  -- Calculate the total amount spent by each user
    FROM customers
    WHERE event_type = 'purchase'  -- Only consider 'purchase' events
    GROUP BY user_id  -- Group by user_id to calculate total spending per user
) AS subquery
GROUP BY total_spent  -- Group by the total amount spent
ORDER BY total_spent;  -- Sort the results by total spending in ascending order
"""

# Execute the query and load the results into a Pandas DataFrame
df_spending = pd.read_sql(query_spending, conn)

# Close the database connection
conn.close()

# Define bin edges to group spending into ranges (e.g., 0-50, 50-100, etc.)
spending_bin_edges = list(range(0, 251, 50))  # Create bins: 0-50, 50-100, ..., 200-250
df_spending['spending_bin'] = pd.cut(df_spending['total_spent'], bins=spending_bin_edges, right=False)  # Assign each spending value to a bin

# Aggregate the customer counts for each spending bin
df_spending_binned = df_spending.groupby('spending_bin')['customer_count'].sum().reset_index()

# Replace bin ranges with custom labels (e.g., 50, 100, 150, ...)
df_spending_binned['spending_bin_label'] = spending_bin_edges[1:]  # Use the upper bounds of the bins as labels

# Plot the bar chart for Altairian Dollars spent
plt.figure(figsize=(10, 6))  # Set the figure size
plt.bar(
    df_spending_binned['spending_bin_label'],  # Use the custom bin labels for the x-axis
    df_spending_binned['customer_count'],  # Use the aggregated customer counts for the y-axis
    color='skyblue',  # Set the bar color
    width=40  # Set the width of the bars
)
plt.title('Altairian Dollars Spent by Customers')  # Set the chart title
plt.xlabel('monetary value in ₳')  # Label for the x-axis
plt.ylabel('customers')  # Label for the y-axis
plt.xticks(spending_bin_edges[1:], rotation=45)  # Set x-axis ticks to the bin labels and rotate them for better readability
plt.tight_layout()  # Adjust the layout to prevent overlapping elements
plt.savefig("./scripts/ex03/bar_chart_spending_binned.png")  # Save the chart as a PNG file
plt.show()  # Display the chart