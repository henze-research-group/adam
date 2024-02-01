import pandas as pd  # pandas is the main data handling package in python
import numpy as np  # NumericalPython is the main package for mathematical/Matrix operations in python
import plotly.express as px  # plotly is the go-to plotting library for this course

# this is important when running in colab
import plotly.io as pio
import plotly.graph_objects as go

# pio.renderers.default = 'colab'
import datetime as dt
import os
import matplotlib.pyplot as plt


prices_df = pd.read_csv('energy-charts_spot_prices_in_Germany_in_2020.csv')
production_df = pd.read_csv('energy-charts_Public_net_electricity_generation_in_Germany_in_2020.csv')



# merge the two datasets
# note that this is an inner join: The production_df is quarter-hourly, the prices_df is only hourly.
# so the final dataframe will be at an hourly interval

data_df = pd.merge(prices_df, production_df, on=prices_df.columns[0])

data_df.head()
units = data_df.head(1)

# remove the header (where the units are stored)
data_df = data_df.tail(-1)

# Convert remaining columns to floats
data_df.iloc[:, 1:] = data_df.iloc[:, 1:].astype(float)


data_df['date_column'] = data_df['Date (GMT+1)'].str[:-6]  # Remove the timezone offset part
data_df['date_column'] = pd.to_datetime(data_df['date_column'], format='%Y-%m-%dT%H:%M')

data_df['hour_of_day'] = data_df['date_column'].apply(lambda x: x.hour)
data_df['month'] = data_df['date_column'].apply(lambda x: x.month)
# this only works if the 'Date (GMT+1)' variable is a datetime, not a string or an object


data_df.drop(columns='Date (GMT+1)')

list_of_columns = data_df.columns
energy_sources = list_of_columns.drop(['Date (GMT+1)', 'Day Ahead Auction', 'hour_of_day', 'month'])
random_week = 24

data_subset = data_df.iloc[random_week * 24 * 7: random_week * 24 * 7 + 24 * 7]
# Create a dictionary to map energy sources to colors
colors = {
    'Import Balance': 'lightgray',
    'Nuclear': 'red',
    'Hydro Run-of-River': 'blue',
    'Biomass': 'green',
    'Fossil brown coal / lignite': 'brown',
    'Fossil hard coal': 'black',
    'Fossil oil': 'orange',
    'Fossil gas': 'purple',
    'Geothermal': 'gray',
    'Hydro water reservoir': 'cyan',
    'Hydro pumped storage': 'magenta',
    'Others': 'yellow',
    'Waste': 'pink',
    'Wind offshore': 'darkblue',
    'Wind onshore': 'darkgreen',
    'Solar': 'gold',
    'Load': 'darkred'
}

# Convert non-numeric values to NaN
data_subset = data_subset.apply(pd.to_numeric, errors='coerce')

# Calculate the cumulative sum for each column except 'Load'
data_cumulative = data_subset.drop(['Load', 'date_column'], axis=1).apply(pd.to_numeric, errors='coerce').cumsum(axis=1)


# Create a trace for each column
traces = []
for column in data_cumulative.columns:
    # Exclude 'Load' and 'Import Balance' from the stacked area chart
    if column not in ['Load', 'Import Balance', 'Date (GMT+1)', 'Day Ahead Auction', 'hour_of_day', 'month']:
        trace = go.Scatter(
            x=data_subset.index,
            y=data_cumulative[column],
            mode='lines',
            name=column,
            fill='tonexty',
            fillcolor=colors[column],
            line=dict(color=colors[column])
        )
        traces.append(trace)

fig = go.Figure(data=traces)

# Add 'Import Balance' as a separate trace at the bottom
import_balance_trace = go.Scatter(
    x=data_subset.index,
    y=data_subset['Import Balance'],
    mode='lines',
    name='Import Balance',
    fill='tozeroy',
    fillcolor=colors['Import Balance'],
    line=dict(color=colors['Import Balance'])
)
fig.add_trace(import_balance_trace)

# Update layout properties
fig.update_layout(
    title='Stacked Line Chart',
    xaxis=dict(title='Index'),
    yaxis=dict(title='Value'),
    showlegend=True
)

# Show the plot
fig.write_image('stacked_line_chart.png')
fig.show()

for column in energy_sources:
    if column in ['date_column', 'Load']:
        continue
    plt.plot(data_subset[column], label=column)
    print(data_subset[column])
plt.legend()
plt.grid()
plt.show()

correlation_matrix = data_df.iloc[:, 1:].corr()
print(correlation_matrix)

fig = px.scatter_matrix(data_df.iloc[:, 1:])
fig.show()




import matplotlib.pyplot as plt
plt.scatter(data_df['Day Ahead Auction'], data_df['Load'])




import numpy as np
print(data_df.columns)

data_df_short = data_df[['Nuclear_x', 'Non-Renewable', 'Renewable',
       'Day Ahead Auction',]]

# Calculate the correlation matrix
correlation_matrix = data_df_short.corr()
print(correlation_matrix)

# Create scatter matrix
fig = px.scatter_matrix(data_df_short)

# Show the plot
fig.show()




# Reshape the DataFrame for Plotly
no_time_df = data_df.iloc[:, 1:].drop(columns=['date_column', 'Day Ahead Auction'])
data_df_melted = pd.melt(no_time_df)

# Create the box plot using Plotly
fig = px.box(data_df_melted, x='variable', y='value', title='Box Plot of DataFrame Columns')

# Display the plot
fig.show()




# Compute the monthly sum
monthly_sum = no_time_df.groupby('month').sum()

# Create pie chart
fig = px.pie(monthly_sum, values=monthly_sum.columns, names=monthly_sum.index,
             title='Monthly Sum', hole=0.4)
fig.show()


