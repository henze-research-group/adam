import pandas as pd
import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
import openpyxl

# Load the Excel file to inspect the data

file_path = 'AREN 5090 OGCS Homework 7.xlsx'

excel_data = pd.ExcelFile(file_path)

data = excel_data.parse('Sheet1')

# Define the load and TOU prices
load = data['Load (kWh)'].values[:24]  # 24-hour load
tou_prices = np.array([
    0.13 if 0 <= h < 6 else
    0.18 if 6 <= h < 12 else
    0.22 if 12 <= h < 18 else
    0.18 if 18 <= h < 24 else
    0.13 for h in range(24)
])  # TOU prices in $/kWh

# Battery parameters
capacity = 15  # kWh
charge_rate = 2  # kW max charge/discharge rate

# Horizon lengths to test
horizons = [2, 6, 12]

# Store results for visualization
results = {}

for horizon in horizons:
    # Variables
    E = cp.Variable(24)  # Battery energy level
    P = cp.Variable(24)  # Battery charge/discharge power
    grid_power = cp.Variable(24)  # Power drawn from the grid

    # Constraints
    constraints = [
        E[0] == 0,  # Battery starts empty
        E >= 0,  # Battery cannot go below 0
        E <= capacity,  # Battery cannot exceed capacity
        P >= -charge_rate,  # Discharge rate limit
        P <= charge_rate,  # Charge rate limit
        grid_power == load - P,  # Power balance
        grid_power >= 0,  # No power is pushed back to the grid
    ]

    for t in range(23):  # Energy dynamics
        constraints.append(E[t + 1] == E[t] + P[t])

    # Objective: Minimize electricity cost
    objective = cp.Minimize(cp.sum(tou_prices * grid_power))

    # Solve the problem
    problem = cp.Problem(objective, constraints)
    problem.solve()

    # Store results
    results[horizon] = {
        'E': E.value,
        'P': P.value,
        'grid_power': grid_power.value,
        'cost': problem.value
    }

# Plot results
for horizon in horizons:
    plt.figure(figsize=(10, 6))
    plt.plot(load, label="Load (kWh)")
    plt.plot(results[horizon]['P'], label="Battery Charging/Discharging (kW)")
    plt.plot(results[horizon]['grid_power'], label="Grid Power (kW)")
    plt.title(f"MPC with Horizon {horizon} Hours")
    plt.xlabel("Hour")
    plt.ylabel("Power (kW) / Load (kWh)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Report total daily electricity cost for each horizon
total_costs = {horizon: results[horizon]['cost'] for horizon in horizons}
print(total_costs)
