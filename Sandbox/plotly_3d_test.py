# Import libraries
import numpy as np
import plotly.graph_objects as go

# Load the topographic data from a text file
# The data is a 2D array of elevation values in meters
# The data source is https://www.eea.europa.eu/data-and-maps/data/eu-dem
data = np.loadtxt('sudetes.txt')

# Define the resolution and extent of the data in degrees
x_res = 0.0083333333 # 30 arc-seconds
y_res = 0.0083333333 # 30 arc-seconds
x_min = 14.5
x_max = 17.5
y_min = 50.0
y_max = 51.0

# Create a meshgrid of x and y coordinates
x = np.arange(x_min, x_max + x_res, x_res)
y = np.arange(y_min, y_max + y_res, y_res)
X, Y = np.meshgrid(x, y)

# Assign the elevation values to z coordinates
Z = data

# Visualize the dataset in a 3d shape using plotly
# Create a figure object
fig = go.Figure()

# Add a surface trace to the figure using a colormap
fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Viridis'))

# Add labels to the axes
fig.update_layout(scene = dict(
                    xaxis_title='Longitude',
                    yaxis_title='Latitude',
                    zaxis_title='Elevation'))

# Add a title to the figure
fig.update_layout(title='Topographic map of the Sudetes range')

# Show the figure in an interactive mode that displays the z coordinate when hovering over the surface
fig.show()