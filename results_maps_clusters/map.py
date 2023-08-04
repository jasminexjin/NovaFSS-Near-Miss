import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import folium
from scipy.spatial.distance import cdist

# Load the incidents data
incidents_df = pd.read_csv('incidents.csv')

# Conversion of latitude/longitude to radians for use by haversine
incidents_df['y_rad'], incidents_df['x_rad'] = np.radians(incidents_df['y']), np.radians(incidents_df['x'])

# Constants
miles_per_radian = 3958.7613
epsilon = 0.3 / miles_per_radian  # Define epsilon as 0.3 miles, converted to radians

# Create a DBSCAN model
db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine')

# Fitting the DBSCAN model
db.fit(incidents_df[['x_rad', 'y_rad']])

# Adding the cluster labels to the DataFrame
incidents_df['cluster'] = db.labels_

# Calculating the center x and y for each cluster
average_points = incidents_df.groupby('cluster')[['x', 'y']].mean().reset_index()
average_points.columns = ['cluster', 'avg_x', 'avg_y']

# Adding the count of incidents per cluster
average_points['incident_count'] = incidents_df.groupby('cluster')['cluster'].count().reset_index(drop=True)

# Function to calculate the radius of incidents for each cluster
def calculate_radius(cluster_df):
    if len(cluster_df) == 1:
        return 0
    avg_point = [cluster_df['y'].mean(), cluster_df['x'].mean()]
    distances = cdist([avg_point], cluster_df[['y', 'x']].values, metric='euclidean')
    return distances.max()/2

# Calculating the radius for each cluster
average_points['radius'] = incidents_df.groupby('cluster').apply(calculate_radius).reset_index(drop=True)

# Function to calculate the main factor and its percentage for each cluster
def calculate_main_factor(cluster_df):
    mode_result = cluster_df['Driver / Cyclist behavior factors'].mode()
    main_factor = mode_result[0] if len(mode_result) > 0 else np.nan
    main_factor_percentage = (cluster_df['Driver / Cyclist behavior factors'] == main_factor).mean() * 100 if main_factor is not np.nan else 0
    return pd.Series({'main_factor': main_factor, 'main_factor_percentage': main_factor_percentage})

# Calculating the main factor and its percentage for each cluster
main_factors_data = incidents_df.groupby('cluster').apply(calculate_main_factor).reset_index()

#Function to calculate the main person and its percentage for each cluster
def calculate_main_person(cluster_df):
    mode_result = cluster_df['Who was impacted?'].mode()
    main_person = mode_result[0] if len(mode_result) > 0 else np.nan
    main_person_percentage = (cluster_df['Who was impacted?'] == main_person).mean() * 100 if main_person is not np.nan else 0
    return pd.Series({'main_person': main_person, 'main_person_percentage': main_person_percentage})

# Calculating the main person and its percentage for each cluster
main_person_data = incidents_df.groupby('cluster').apply(calculate_main_person).reset_index()

# First, merge average_points with main_person_data
intermediate_data = average_points.merge(main_person_data, on='cluster', how='left')

# Then, merge intermediate_data with main_factors_data
final_data = intermediate_data.merge(main_factors_data, on='cluster', how='left')


# Creating a map centered around the average latitude and longitude
map_center = [final_data['avg_y'].mean(), final_data['avg_x'].mean()]
incident_map = folium.Map(location=map_center, zoom_start=12)

# Adding the clusters and circles to the map
for idx, row in final_data.iterrows():
    popup_text = f"Cluster: {row['cluster']}<br>Incidents: {row['incident_count']}<br>Main Factor: {row['main_factor']}<br>Main Factor Percentage: {row['main_factor_percentage']:.2f}%" \
                 f"<br>Main Person: {row['main_person']}<br>Main Person Percentage: {row['main_person_percentage']}"
    folium.Marker(location=[row['avg_y'], row['avg_x']], popup=popup_text).add_to(incident_map)
    folium.Circle(location=[row['avg_y'], row['avg_x']], radius=row['radius'] * 100000, color='blue', fill=True, fill_opacity=0.2).add_to(incident_map)

# Saving the map to an HTML file
incident_map.save('final_incident_map4.html')
