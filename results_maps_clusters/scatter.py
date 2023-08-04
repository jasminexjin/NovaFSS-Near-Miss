import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

# Load the incidents data (if you've already loaded it, you can skip this part)

incidents_df = pd.read_csv('incidents.csv')
incidents_df['y_rad'], incidents_df['x_rad'] = np.radians(incidents_df['y']), np.radians(incidents_df['x'])
miles_per_radian = 3958.7613
epsilon = 0.3 / miles_per_radian
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine')
db.fit(incidents_df[['x_rad', 'y_rad']])
incidents_df['cluster'] = db.labels_

# Scatter plot
plt.figure(figsize=(12, 8))
plt.scatter(incidents_df['x'], incidents_df['y'], c=incidents_df['cluster'], cmap='', s=10)
plt.colorbar(label='Cluster Label')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('The scatter plot shows the current clustering result using the DBSCAN algorithm')
plt.grid(True)
plt.show()
