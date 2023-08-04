import os

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

# Load your csv file into a pandas DataFrame
df = pd.read_csv('incidents.csv')

# Conversion of latitude/longitude to radians for use by haversine
df['y_rad'], df['x_rad'] = np.radians(df['y']), np.radians(df['x'])

# Constants
miles_per_radian = 3958.7613
epsilon = 0.1 / miles_per_radian  # define epsilon as 1 mile, converted to radians for use by haversine

# Create a DBSCAN model
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine')

# Perform the clustering
df['cluster'] = db.fit_predict(df[['y_rad', 'x_rad']])

# Print the number of clusters found
print(f"Number of clusters: {len(df['cluster'].unique())}")

# Create a directory for cluster CSVs if it doesn't exist
if not os.path.exists('clusters'):
    os.makedirs('clusters')

# Create a DataFrame to store the main factors for each cluster
reasons_df = pd.DataFrame(columns=['cluster_id', 'main_factor'])

# Save each cluster as a separate CSV file and find the main factor
for cluster_num in df['cluster'].unique():
    cluster_df = df[df['cluster'] == cluster_num]
    cluster_df.to_csv(f'clusters/cluster_{cluster_num}.csv', index=False)

    # Calculate the main factor for this cluster and add it to the reasons DataFrame
    mode_result = cluster_df['Driver / Cyclist behavior factors'].mode()
    if len(mode_result) > 0:
        main_factor = mode_result[0]
        temp_df = pd.DataFrame([{'cluster_id': cluster_num, 'main_factor': main_factor}])
        reasons_df = pd.concat([reasons_df, temp_df])
    else:
        print(f"No mode found for cluster {cluster_num}, writing null...")
        # Add a row with a null value for the main factor
        temp_df = pd.DataFrame([{'cluster_id': cluster_num, 'main_factor': np.nan}])
        reasons_df = pd.concat([reasons_df, temp_df])

# Save the main factors to a CSV
reasons_df.to_csv('reasons.csv', index=False)

# Add a column with the cluster number to the original DataFrame
df['cluster'] = db.labels_

# Save the original DataFrame with the cluster number to a CSV
df.to_csv('incidents_with_clusters.csv', index=False)
