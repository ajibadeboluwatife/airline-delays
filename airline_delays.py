import pandas as pd

# Read the files and import all rows.
df_18 = pd.read_csv('delays_2018.csv')
df_19 = pd.read_csv('delays_2019.csv')

# Concatenate the 2018 and 2019 data into a single DataFrame.
df = pd.concat([df_18, df_19], ignore_index=True)

# Print out the number of rows imported from the files.
print('Number of Rows: ' + str(len(df_18) + len(df_19)))
# Change the data type of the 'month' column to date and change the format to YYYY-M (e.g. 2018-1).
df['date'] = pd.to_datetime(df['date'], format='%Y-%m').dt.strftime('%Y-%m')

# Remove rows containing invalid data.
df = df[(df['date'] >= '2018-01') & (df['date'] <= '2019-12') & (df['arr_flights'].notnull())
              & (df['carrier'].notnull()) & (df['carrier_name'].notnull()) 
              & (df['airport'].notnull()) & (df['airport_name'].notnull())]

# Print out the number of rows remaining in the dataset.
print('Number of Rows: ' + str(len(df)))
# Identify the airports in the state of Tennessee.
df['TN'] = df['airport_name'].apply(lambda x: x.find('TN'))

# Create a set of airport names (to eliminate the duplicates).
airports = set(df[df['TN'] != -1]['airport_name'])

# Display the list of airports.
print('Tennessee Airports:')
print(airports)
# Read the coordinates file and import all rows.
df_coords = pd.read_csv('airport_coordinates.csv')

# Create a new DataFrame with airport codes and names.
df_airports = df[['airport', 'airport_name']].drop_duplicates().reset_index(drop=True)

# Merge the coordinates DataFrame with the airports DataFrame.
df_airports = pd.merge(df_airports, df_coords, on='airport')
# This code was required due to an Anaconda issue.  You may not need it depending on your environment.
import os
os.environ["PROJ_LIB"] = "C:\\Users\\Nick\\anaconda3\\envs\\sandbox\\Library\\share\\basemap";

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# Ready the Basemap for display.
fig = plt.figure(figsize=(16, 16))
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=32,lat_2=45,lon_0=-95)

# Load the shapefile to display the outlines of the US states.
m.readshapefile('st99_d00', name='states', drawbounds=True)

# Plot the airports on the map.
m.scatter(df_airports['long'].values, df_airports['lat'].values, latlon=True)
plt.show()
# Use crosstab to display the number of diverted flights for each carrier-airport pair, without null values.
pd.crosstab(df['carrier'], df['airport'], values=df['arr_del15'], aggfunc='sum', margins=True).fillna(0)        
# Subset DataFrame for planes arriving into JFK in 2019 with values in both the carrier_ct and weather_ct columns.
df_f = df[(df['date'] >= '2019-01') & (df['date'] <= '2019-12') & (df['airport'] == 'JFK') 
          & (df['carrier_ct'] > 0) & (df['weather_ct'] > 0)]

# Add together the sums of the two columns to obtain the total number of delays.

print("Number of Delays: " + str(df_f['carrier_ct'].sum()  + df_f['weather_ct'].sum()))
# Create a DataFrame containing airline names, total arriving flights and number of cancelled flights.
df_flights = df.groupby('carrier_name')['arr_flights'].sum().reset_index(name='num_arrived')
df_cancelled = df.groupby('carrier_name')['arr_cancelled'].sum().reset_index(name='num_cancelled')
df_cancelled = pd.merge(df_cancelled, df_flights, on='carrier_name')

# Calculate the percentage of flights cancelled.
df_cancelled['proportion'] = df_cancelled['num_cancelled'] / df_cancelled['num_arrived'] * 100

# Display the airline with the most cancellations as a percentage of total arriving flights.
df_cancelled.sort_values(by=['proportion'], ascending=False).head(1)
# Calculate the average number of delays per airport.
avg_delays = df.groupby('airport')['arr_del15'].sum().mean()

# Display average number of delays per airport.
print('Average Number of Delays per Airport: ' + str(avg_delays))
df.groupby('carrier')['arr_del15'].sum().nsmallest(3).reset_index(name='num_delays')
airline = input("What airline (9E, AA, AS, B6, DL, EV, F9, G4, HA, MQ, NK, OH, OO, UA, VX, WN, YV, YX)? ")
# Subset for carrier selected by user and rows with a NAS delay.
df_nas = df[(df['carrier'] == airline) & (df['nas_delay'] > 0)]

# Determine total number of NAS delay minutes by month.
df_nas = df_nas.groupby('date')['nas_delay'].sum().reset_index(name='total_nas_delay')
# Plot NAS delay minutes by month for selected airline.
plt.figure(figsize=(16, 8))
plt.plot(df_nas)
plt.xticks(rotation=85)
plt.show()
# Display whether total NAS delay minutes are increasing or decreasing for past 2 months.
if df_nas.iloc[-1] > df_nas.iloc[-2]:
    print('Total NAS delay minutes for ' + airline + ' are increasing.')
else:
    print('Total NAS delay minutes for ' + airline + ' are decreasing.')