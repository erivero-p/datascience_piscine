import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# Database Conection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)

query = """
SELECT
    DATE(event_time) AS date,
    price,
    user_id
FROM customers
WHERE event_type = 'purchase'
  AND event_time >= '2022-10-01'
  AND event_time < '2023-03-01'
"""
df = pd.read_sql(query, conn)
conn.close()

df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.strftime('%b')  # Oct, Nov, etc.

# ------------------------
# 1. Number of customers per day
# ------------------------
daily_purchases = df.groupby('date')['user_id'].nunique()

plt.figure(figsize=(10, 5))
daily_purchases.plot()
plt.title("Number of customers")
plt.ylabel("Number of customers")
plt.tight_layout()
plt.savefig("./scripts/ex01/plot_01_customers_per_day.png")
plt.close()

# ------------------------
# 2. Total sales per month (in ₳ million)
# ------------------------
monthly_sales = df.groupby('month')['price'].sum() / 1_000_000
order = ['Oct', 'Nov', 'Dec', 'Jan', 'Feb']  # asegurar orden

monthly_sales = monthly_sales.reindex(order)

plt.figure(figsize=(8, 5))
monthly_sales.plot(kind='bar', color='lightsteelblue')
plt.title("total sales in million of ₳")
plt.ylabel("total sales in million of ₳")
plt.xlabel("month")
plt.tight_layout()
plt.savefig("./scripts/ex01/plot_02_sales_per_month.png")
plt.close()

# ------------------------
# 3. Average customer spent per day in ₳
# ------------------------
avg_spend_per_customer = df.groupby('date').apply(
    lambda x: x['price'].sum() / x['user_id'].nunique()
)

plt.figure(figsize=(10, 5))
avg_spend_per_customer.plot(kind='area', color='lightsteelblue')
plt.title("average spend/customers in ₳")
plt.ylabel("average spend/customers in ₳")
plt.tight_layout()
plt.savefig("./scripts/ex01/plot_03_avg_spend.png")
plt.close()
