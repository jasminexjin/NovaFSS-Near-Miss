import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('results_maps_clusters/incidents.csv')


#graph for travel lane count
travel_lane_counts = df['Travel Lane'].value_counts()
plt.figure(figsize=(10, 8))
travel_lane_counts.plot(kind='barh', color='skyblue')

plt.title('Distribution of Incidents in Different Travel Lanes')
plt.xlabel('Number of Incidents')
plt.ylabel('Travel Lane')

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('Distribution of Incidents in Different Travel Lanes.png', dpi=300)
plt.show()


#graph for Area count
travel_lane_counts = df['Area'].value_counts()
plt.figure(figsize=(10, 8))
travel_lane_counts.plot(kind='barh', color='skyblue')


plt.title('Distribution of Incidents in Different Area')
plt.xlabel('Number of Incidents')
plt.ylabel('Area')

plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('Distribution of Incidents in Different Area.png', dpi=300)
plt.show()


#graph for behavior - only top 20 since there are 100 different categories
#checking how many different factors there are in driver/cyclist behavior
behavior_factors_counts = df['Driver / Cyclist behavior factors'].value_counts()
top_20_behavior_factors = behavior_factors_counts[:20]

plt.figure(figsize=(10,8))

# Create a horizontal bar plot
top_20_behavior_factors.plot(kind='barh', color='skyblue')

# Set the title and labels
plt.title('Top 20 Driver / Cyclist Behavior Factors')
plt.xlabel('Count')
plt.ylabel('Behavior Factors')

# Reverse the order of categories for better readability
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('Distribution of Incidents with different behavior.png', dpi=300)
plt.show()
