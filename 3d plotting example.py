import numpy as np
import plotly.graph_objects as go

# Set random seed for reproducibility
np.random.seed(0)

# Function to apply the Diamond-Square algorithm
def diamond_square(height_map, x, y, step_size, scale):
    half = step_size // 2

    # Diamond step
    top_left = height_map[x, y]
    top_right = height_map[x + step_size, y]
    bottom_left = height_map[x, y + step_size]
    bottom_right = height_map[x + step_size, y + step_size]

    center = np.mean([top_left, top_right, bottom_left, bottom_right])
    height_map[x + half, y + half] = center + np.random.randn() * scale

    # Square step
    height_map[x + half, y] = (top_left + top_right + center) / 3 + np.random.randn() * scale
    height_map[x, y + half] = (top_left + bottom_left + center) / 3 + np.random.randn() * scale
    height_map[x + step_size, y + half] = (top_right + bottom_right + center) / 3 + np.random.randn() * scale
    height_map[x + half, y + step_size] = (bottom_left + bottom_right + center) / 3 + np.random.randn() * scale

# Generate synthetic terrain data
size = 129  # Size of the height map (should be 2^n + 1)
scale = 20  # Controls the roughness of the terrain

height_map = np.zeros((size, size))
step_size = size - 1

while step_size > 1:
    half = step_size // 2

    for x in range(0, size - 1, step_size):
        for y in range(0, size - 1, step_size):
            diamond_square(height_map, x, y, step_size, scale)

    scale *= 0.5
    step_size //= 2

# Generate X and Y coordinates based on the height map dimensions
x = np.arange(0, size)
y = np.arange(0, size)
X, Y = np.meshgrid(x, y)

# Set colormap colors
olive_green = '#808000'
brown_tones = '#8B4513'
white = '#FFFFFF'

# Define the colormap
colorscale = [[0, olive_green],
              [height_map.max() * 0.7 / height_map.max(), brown_tones],
              [1, white]]

# Create 3D plot using Plotly
fig = go.Figure(data=go.Surface(z=height_map, colorscale=colorscale))
fig.update_layout(scene=dict(aspectratio=dict(x=1, y=1, z=0.7),
                             xaxis=dict(title='X'),
                             yaxis=dict(title='Y'),
                             zaxis=dict(title='Z')),
                  margin=dict(l=0, r=0, b=0, t=0))

# Add hover functionality to display Z coordinate
hovertemplate = 'Z: %{z:.2f}<extra></extra>'
fig.data[0].update(hovertemplate=hovertemplate)

fig.show()
