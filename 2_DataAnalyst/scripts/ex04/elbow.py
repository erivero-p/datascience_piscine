import os
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS")
)

# extract relevant customer characteristics
query = """
SELECT
    user_id,
    COUNT(*) AS purchase_count, 
    SUM(price) AS total_spent,  
    AVG(price) AS avg_spent   
FROM customers
WHERE event_type = 'purchase' 
  AND price > 0               
GROUP BY user_id;              
"""

# load the query results into a Pandas DataFrame
df = pd.read_sql(query, conn)
conn.close()

# scale the features to standardize the data (mean = 0, standard deviation = 1)
# this ensures that all features contribute equally to the clustering process
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[['purchase_count', 'total_spent', 'avg_spent']])

# apply KMeans clustering for different values of k (number of clusters)
# the goal is to calculate the inertia (sum of squared distances to cluster centers)
# for each value of k and identify the "elbow point"
inertia = []  # list to store inertia values for each k
K_range = range(1, 11)  # test k values from 1 to 10
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)  # initialize KMeans with k clusters
    kmeans.fit(scaled_features)  # fit the model to the scaled features
    inertia.append(kmeans.inertia_)  # append the inertia (sum of squared distances)

plt.figure(figsize=(8, 5))
plt.plot(K_range, inertia, 'bo-', label='Inertia')
plt.xlabel('Number of clusters (k)') 
plt.ylabel('Inertia (Sum of Squared Distances)') 
plt.title('The Elbow Method')
plt.legend()
plt.tight_layout()
plt.savefig('./scripts/ex04/elbow_method.png')
plt.close()