# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the parameters of the system
m = 1    # mass in kg
c = 0.1  # damping coefficient in Ns/m
k = 1    # spring constant in N/m

wn = np.sqrt(k/m)  # natural frequency in rad/s
zeta = c/(2*np.sqrt(k*m))  # damping ratio

# Define the initial conditions
x0 = 0      # initial displacement in m
v0 = 0      # initial velocity in m/s
t0 = 0      # initial time in s
tf = 100     # final time in s
dt = 0.001  # time step in s

t = np.arange(t0, tf+dt, dt)  # time array
x = np.zeros_like(t)          # displacement array
v = np.zeros_like(t)          # velocity array

x[0] = x0
v[0] = v0

# Define the input force as a function of time
def input(t):
    if t < 1 or t % 5 < 3:
        return 0
    else:
        return 1

# Define the right-hand side of the differential equation
def rhs(xv, t, f):
    x, v = xv
    dxdt = v
    dvdt = (f/m) - 2*zeta*wn*v - wn**2*x
    return [dxdt, dvdt]

# Solve the differential equation at each time step
for i in range(len(t)-1):
    f = input(t[i])
    sol = odeint(rhs, [x[i], v[i]], [t[i], t[i+1]], args=(f,))
    x[i+1] = sol[-1, 0]
    v[i+1] = sol[-1, 1]

# Plot the displacement and velocity of the system as a function of time
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

ax1.plot(t, x, label='displacement')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Displacement (m)')
ax1.legend()

ax2.plot(t, v, label='velocity')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Velocity (m/s)')
ax2.legend()

plt.show()