import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Database Connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)

# Create cursor
cur = conn.cursor()

# Query for selecting the required values
query = """
SELECT
  COUNT(*) AS count,
  AVG(price) AS mean,
  STDDEV(price) AS std,
  MIN(price) AS min,
  PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS q1,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS median,
  PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS q3,
  MAX(price) AS max
FROM customers
WHERE event_type = 'purchase' AND price > 0;
"""

cur.execute(query)
# Get the results
result = cur.fetchone()

# Print the results with tags
columns = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
for col, val in zip(columns, result):
    print(f"{col}: {val:.6f}" if isinstance(val, float) else f"{col}: {val}")

# Fetch all prices for box plot
query_prices = """
SELECT price
FROM customers
WHERE event_type = 'purchase';
"""
df_prices = pd.read_sql(query_prices, conn)

# Create the first box plot (with outliers)
plt.figure(figsize=(8, 6))
plt.boxplot(df_prices['price'], vert=False, patch_artist=True, boxprops=dict(facecolor="lightgreen"))
plt.title("Box Plot of Prices (with outliers)")
plt.xlabel("price")
plt.savefig("./scripts/ex02/boxplot_with_outliers.png")
plt.close()

# Create the second box plot (without extreme outliers)
# Define a reasonable range (e.g., within 1.5 * IQR)
q1 = df_prices['price'].quantile(0.25)
q3 = df_prices['price'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

filtered_prices = df_prices[(df_prices['price'] >= lower_bound) & (df_prices['price'] <= upper_bound)]

plt.figure(figsize=(8, 6))
plt.boxplot(filtered_prices['price'], vert=False, patch_artist=True, boxprops=dict(facecolor="lightgreen"))
plt.title("Box Plot of Prices (without extreme outliers)")
plt.xlabel("price")
plt.savefig("./scripts/ex02/boxplot_without_outliers.png")
plt.close()

# Calculate the average basket price per user
query_avg_basket = """
SELECT user_id, AVG(price) AS avg_basket_price
FROM customers
WHERE event_type = 'purchase'
GROUP BY user_id;
"""
df_avg_basket = pd.read_sql(query_avg_basket, conn)

# Use all the data
avg_cart_prices = df_avg_basket['avg_basket_price'].tolist()

# Calculate Q1 and Q3 to determine the adjusted range
q1 = df_avg_basket['avg_basket_price'].quantile(0.25)
q3 = df_avg_basket['avg_basket_price'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Create the box plot for average basket price per user
plt.figure(figsize=(10, 4))
plt.boxplot(
    avg_cart_prices,
    vert=False,
    widths=0.6,
    notch=True,
    boxprops=dict(facecolor='lightblue', edgecolor='black'),
    flierprops=dict(marker='o', markersize=3, markerfacecolor='red', markeredgecolor='black') ,
    patch_artist=True,
    whis=1.5  # Whiskers extend to 1.5 * IQR
)

plt.title("Box Plot of Average Basket Price per User")
plt.xlabel("average basket price")

# Adjust the x-axis ticks
plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(2))  # Increments of 2 on the x-axis
plt.gca().xaxis.set_minor_locator(ticker.MultipleLocator(1))  # Minor increments of 1 on the x-axis

# Adjust the x-axis limits to include the outliers
plt.xlim(lower_bound - 2, upper_bound + 2)  # Extend slightly beyond the adjusted range

# Remove the y-axis ticks (optional, since it's a horizontal box plot)
plt.yticks([])

# Save the image
plt.tight_layout()
plt.savefig("./scripts/ex02/boxplot_avg_basket_price_with_outliers.png")
plt.close()


# Close connection
cur.close()
conn.close()