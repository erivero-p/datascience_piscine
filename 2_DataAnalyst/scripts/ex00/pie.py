import os
import psycopg2
import matplotlib.pyplot as plt

# Database connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)
cur = conn.cursor()

# SQL query to count event types
cur.execute("""
    SELECT event_type, COUNT(*) AS count
    FROM customers
    GROUP BY event_type;
""")

# Retrieve results
results = cur.fetchall()
event_types = [row[0] for row in results]
counts = [row[1] for row in results]

# Close connection
cur.close()
conn.close()

# Create the chart
plt.figure(figsize=(8, 8))
plt.pie(counts, labels=event_types, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Events on the Site')
plt.axis('equal')
plt.show()
plt.savefig("./scripts/ex00/chart.png")
print("✅ Pie chart saved as chart.png")