# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Define the parameters of the system
g = 9.81    # acceleration due to gravity in m/s^2
L = 1       # length of the pendulum in m
mu = 0.1    # damping coefficient
F0 = 1      # amplitude of the applied force

# Define the initial conditions
theta0 = np.pi/2     # initial angular displacement in radians
omega0 = 4           # initial angular velocity in radians/s
t0 = 0               # initial time in s
tf = 10              # final time in s
dt = 0.01            # time step in s

t = np.arange(t0, tf+dt, dt)  # time array
theta = np.zeros_like(t)      # angular displacement array
omega = np.zeros_like(t)      # angular velocity array

theta[0] = theta0
omega[0] = omega0

# Define the input force as a function of time and angular displacement
def input(t, theta):
    return F0*np.sin(theta)

# Define the right-hand side of the differential equation
def rhs(y, t):
    theta, omega = y
    dtheta_dt = omega
    domega_dt = -g/L*np.sin(theta) - mu*omega/L + input(t, theta)/L
    return [dtheta_dt, domega_dt]

# Solve the differential equation at each time step
for i in range(len(t)-1):
    sol = odeint(rhs, [theta[i], omega[i]], [t[i], t[i+1]])
    theta[i+1] = sol[-1, 0]
    omega[i+1] = sol[-1, 1]

# Plot the displacement and velocity of the pendulum as a function of time
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

ax1.plot(t, theta, label='angular displacement')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Angular Displacement (rad)')
ax1.legend()

ax2.plot(t, omega, label='angular velocity')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Angular Velocity (rad/s)')
ax2.legend()

plt.show()