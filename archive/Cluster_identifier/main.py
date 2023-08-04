import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
import os

# Load your csv file into a pandas DataFrame
df = pd.read_csv('incidents.csv')

# Conversion of latitude/longitude to radians for use by haversine
df['y_rad'], df['x_rad'] = np.radians(df['y']), np.radians(df['x'])

# Constants
kms_per_radian = 6371.0088
epsilon = 1 / kms_per_radian  # define epsilon as 1 miles, converted to radians for use by haversine

# Create a DBSCAN model
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine')

# Perform the clustering
df['cluster'] = db.fit_predict(df[['y_rad', 'x_rad']])

# Print the number of clusters found
print(f"Number of clusters: {len(df['cluster'].unique())}")

# Create a directory for cluster CSVs if it doesn't exist
if not os.path.exists('clusters'):
    os.makedirs('clusters')

# Add a column with the cluster number to the original DataFrame
df['cluster'] = db.labels_

# Save clusters to one big CSV file
df.to_csv('clusters/all_clusters.csv', index=False)

# # Save each cluster as a separate CSV file
# for cluster_num in df['cluster'].unique():
#     cluster_df = df[df['cluster'] == cluster_num]
#     cluster_df.to_csv(f'clusters/cluster_{cluster_num}.csv', index=False)
