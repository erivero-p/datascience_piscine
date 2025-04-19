import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
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
WHERE event_type = 'purchase' AND price > 0;
"""
df_prices = pd.read_sql(query_prices, conn)

# Create the first box plot (with outliers)
plt.figure(figsize=(8, 6))
plt.boxplot(df_prices['price'], vert=False, patch_artist=True, boxprops=dict(facecolor="lightgreen"))
plt.title("Box Plot of Prices (with outliers)")
plt.xlabel("Price")
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
plt.xlabel("Price")
plt.savefig("./scripts/ex02/boxplot_without_outliers.png")
plt.close()

# Calculate the average basket price per user
query_avg_basket = """
SELECT user_id, AVG(price) AS avg_basket_price
FROM customers
WHERE event_type = 'purchase' AND price > 0
GROUP BY user_id;
"""
df_avg_basket = pd.read_sql(query_avg_basket, conn)

# Create the third box plot (average basket price with outliers)
plt.figure(figsize=(8, 6))
plt.boxplot(df_avg_basket['avg_basket_price'], vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))
plt.title("Box Plot of Average Basket Price per User (With Outliers)")
plt.xlabel("Average Basket Price")
plt.savefig("./scripts/ex02/boxplot_avg_basket_price_with_outliers.png")
plt.close()

# Create the fourth box plot (average basket price without extreme outliers)
# Define a reasonable range (e.g., within 1.5 * IQR)
q1_avg = df_avg_basket['avg_basket_price'].quantile(0.25)
q3_avg = df_avg_basket['avg_basket_price'].quantile(0.75)
iqr_avg = q3_avg - q1_avg
lower_bound_avg = q1_avg - 1.5 * iqr_avg
upper_bound_avg = q3_avg + 1.5 * iqr_avg

filtered_avg_basket = df_avg_basket[
    (df_avg_basket['avg_basket_price'] >= lower_bound_avg) &
    (df_avg_basket['avg_basket_price'] <= upper_bound_avg)
]

plt.figure(figsize=(8, 6))
plt.boxplot(filtered_avg_basket['avg_basket_price'], vert=False, patch_artist=True, boxprops=dict(facecolor="lightblue"))
plt.title("Box Plot of Average Basket Price per User (Without Extreme Outliers)")
plt.xlabel("Average Basket Price")
plt.savefig("./scripts/ex02/boxplot_avg_basket_price_without_outliers.png")
plt.close()

# Close connection
cur.close()
conn.close()