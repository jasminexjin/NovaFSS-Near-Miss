import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('results_maps_clusters/incidents.csv')

#separate cyclist and pedestrians
df_cyclist = df[df['Who was impacted?'] == 'Cyclist']
df_pedestrian = df[df['Who was impacted?'] == 'Person_Walking']

#function to calculate the percentage
def calculate_percentage(file, column, main_value):
    main_value_percentage = (file[column] == main_value).mean() * 100 if main_value is not np.nan else 0
    return main_value_percentage



#travel lane factor, top 3 and their percentages
#cyclist
t3_travel_lane_cyclist = df_cyclist['Travel Lane'].value_counts().nlargest(3)

# Create a new DataFrame to store value and percentage
df_travel_lane_cyclist = pd.DataFrame(t3_travel_lane_cyclist).reset_index()
df_travel_lane_cyclist.columns = ['Travel Lane', 'Count']

# Calculate percentage for each value
df_travel_lane_cyclist['Percentage'] = df_travel_lane_cyclist.apply(lambda row: calculate_percentage(df_cyclist, 'Travel Lane', row['Travel Lane']), axis=1)


#pedestrian
t3_travel_lane_pedestrian = df_pedestrian['Travel Lane'].value_counts().nlargest(3)

# Create a new DataFrame to store value and percentage
df_travel_lane_pedestrian = pd.DataFrame(t3_travel_lane_pedestrian).reset_index()
df_travel_lane_pedestrian.columns = ['Travel Lane', 'Count']

# Calculate percentage for each value
df_travel_lane_pedestrian['Percentage'] = df_travel_lane_pedestrian.apply(lambda row: calculate_percentage(df_pedestrian, 'Travel Lane', row['Travel Lane']), axis=1)



#incident Area main factor, top 3 and their percentages
#cyclist
t3_Area_cyclist = df_cyclist['Area'].value_counts().nlargest(3)

# Create a new DataFrame to store value and percentage
df_Area_cyclist = pd.DataFrame(t3_Area_cyclist).reset_index()
df_Area_cyclist.columns = ['Area', 'Count']

# Calculate percentage for each value
df_Area_cyclist['Percentage'] = df_Area_cyclist.apply(lambda row: calculate_percentage(df_cyclist, 'Area', row['Area']), axis=1)


#pedestrian
t3_Area_pedestrian = df_pedestrian['Area'].value_counts().nlargest(3)

# Create a new DataFrame to store value and percentage
df_Area_pedestrian = pd.DataFrame(t3_Area_pedestrian).reset_index()
df_Area_pedestrian.columns = ['Area', 'Count']

# Calculate percentage for each value
df_Area_pedestrian['Percentage'] = df_Area_pedestrian.apply(lambda row: calculate_percentage(df_pedestrian, 'Area', row['Area']), axis=1)



#Driver / Cyclist behavior factors, top3
#cyclist
t3_behavior_cyclist = df_cyclist['Driver / Cyclist behavior factors'].value_counts().nlargest(3)

# Create a new DataFrame to store value and percentage
df_behavior_cyclist = pd.DataFrame(t3_behavior_cyclist).reset_index()
df_behavior_cyclist.columns = ['Driver / Cyclist behavior factors', 'Count']

# Calculate percentage for each value
df_behavior_cyclist['Percentage'] = df_behavior_cyclist.apply(lambda row: calculate_percentage(df_cyclist, 'Driver / Cyclist behavior factors', row['Driver / Cyclist behavior factors']), axis=1)


#pedestrian
t3_behavior_pedestrian = df_pedestrian['Driver / Cyclist behavior factors'].value_counts().nlargest(3)

# Create a new DataFrame to store value and percentage
df_behavior_pedestrian = pd.DataFrame(t3_behavior_pedestrian).reset_index()
df_behavior_pedestrian.columns = ['Driver / Cyclist behavior factors', 'Count']

# Calculate percentage for each value
df_behavior_pedestrian['Percentage'] = df_behavior_pedestrian.apply(lambda row: calculate_percentage(df_pedestrian, 'Driver / Cyclist behavior factors', row['Driver / Cyclist behavior factors']), axis=1)

#put pedestrian data in a csv file
combined_df = pd.concat([df_travel_lane_pedestrian, df_Area_pedestrian, df_behavior_pedestrian])
combined_df.to_csv('combined_data_pedestrian.csv', index=False)

#put cyclist data in a csv file
combined_df = pd.concat([df_travel_lane_cyclist, df_Area_cyclist, df_behavior_cyclist])
combined_df.to_csv('combined_data_cyclist.csv', index=False)

