# Import libraries
import numpy as np
import plotly.graph_objects as go

# Create a virtual dataset of a topographic map
# Define the range and resolution of x and y coordinates
x_min = -10
x_max = 10
y_min = -10
y_max = 10
x_res = 0.1
y_res = 0.1

# Create a meshgrid of x and y coordinates
x = np.arange(x_min, x_max + x_res, x_res)
y = np.arange(y_min, y_max + y_res, y_res)
X, Y = np.meshgrid(x, y)

# Define a function that maps each (x,y) pair to a height z
def f(x,y):
    # For example, a simple paraboloid function
    return x**2 + y**2

# Apply the function to the meshgrid to get the z coordinates
Z = f(X,Y)

# Visualize the dataset in a 3d shape using plotly
# Create a figure object
fig = go.Figure()

# Add a surface trace to the figure using a colormap
fig.add_trace(go.Surface(x=X, y=Y, z=Z, colorscale='Viridis'))

# Add labels to the axes
fig.update_layout(scene = dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z'))

# Add a title to the figure
fig.update_layout(title='Virtual dataset of a topographic map')

# Show the figure in an interactive mode that displays the z coordinate when hovering over the surface
fig.show()