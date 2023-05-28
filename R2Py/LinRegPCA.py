import plotly.express as px
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA# Read the csv files
building_data = pd.read_csv("HOTDRY Summer.csv", sep=";")
weather = pd.read_csv("HOTDRY Summer Weather.csv", sep=";")

# Convert the date column to datetime
weather['Date'] = pd.to_datetime(weather['Date'])

# Convert the other columns to numeric
weather.iloc[:, 1:] = weather.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
building_data.iloc[:, 1:] = building_data.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

# Set the index to be the 'Date' column
weather = weather.set_index('Date')

# Combine the data frames
build_df = pd.concat([weather.iloc[0:504, :], building_data.iloc[0:504, 1:9]], axis=1)

# Group by year and month using the index attribute
infy_volume = build_df.groupby([build_df.index.year, build_df.index.month]).Volume.sum()

# Compute the correlation matrix and plot it
CorrMatrix = build_df.corr()
fig = px.imshow(CorrMatrix)
fig.show()

# Define the variables for multiple linear regression
cooling = build_df.iloc[:, 9]
drybulb = build_df.iloc[:, 1]
dewpoint = build_df.iloc[:, 2]
Igh = build_df.iloc[:, 4]
Idn = build_df.iloc[:, 5]
IDh = build_df.iloc[:, 6]

# Fit the multiple linear regression model
cool_lm2 = LinearRegression().fit(pd.DataFrame([drybulb, dewpoint, Igh]).T, cooling)
print(cool_lm2.coef_)
print(cool_lm2.intercept_)

# Perform principal components analysis
PCclg = PCA().fit(build_df.iloc[:, 0:8])
print(PCclg.explained_variance_ratio_)

# Plot the spectrum plot
fig = px.line(y=PCclg.explained_variance_ratio_, title="Variance explained vs. PC")
fig.show()
fig = px.line(y=PCclg.explained_variance_ratio_.cumsum(), title="Cumulative variance explained vs. PC")
fig.show()

# How many PCs needed to explain 99% of variance?
NPCimp = max(np.where(PCclg.explained_variance_ratio_.cumsum() < 0.99)[0]) + 1
print(NPCimp)

# Fit the linear regression model with PCs
cool_lm3 = LinearRegression().fit(PCclg.transform(build_df.iloc[:, 0:8])[:, :NPCimp], cooling)
print(cool_lm3.coef_)
print(cool_lm3.intercept_)
