import pandas as pd
import folium
from folium import PolyLine
import concurrent.futures

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('Records.csv')

# Initialize the map
m = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()],
               zoom_start=12)

# Create a list of coordinates as [latitude, longitude] pairs
coordinates = data[['Latitude', 'Longitude']].values.tolist()


# Function to draw the PolyLine
def draw_polyline(coordinates):
    polyline = PolyLine(
        locations=coordinates,
        color='blue',  # Customize the color of the line
        weight=5,  # Customize the weight/thickness of the line
    )
    polyline.add_to(m)


# Use concurrent.futures to parallelize the line drawing
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(draw_polyline, coordinates)

# Save the map to an HTML file
m.save('travel_map_with_lines_parallel.html')

print("Map with lines saved as 'travel_map_with_lines_parallel.html'")
