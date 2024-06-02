import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the general exponential function
def func(x, a, b, c):
    return a*np.exp(-b*x) + c

# Generate sample data
np.random.seed(42)  # For reproducibility
x = np.linspace(0, 20*9.82, 100)  # Force measurements
a_true = 100_000 # True parameter a
b_true = 0.02 # True parameter b
c_true = 0  # True parameter c
y_true = func(x, a_true, b_true, c_true)  # True resistance values


# x_meas = np.linspace(0, 20, 10)
# y_meas_true = general_exponential_function(x_meas, a_true, b_true, c_true)
# noise = np.random.normal(0, 0.05, x_meas.size) grgra # Noise
# y_meas = y_meas_true   # Noisy resistance values

# x_meas = np.array([  0.38,    0.6,   1.08,   1.5,       2,    5.2,    6.6]) * 9.82 # F = m*g
# y_meas = np.array([79_000, 62_000, 34_000, 29_000, 26_000, 13_000, 11_500])

x_meas = np.array([  0.38,    0.6,   1.08,   1.5,       2]) * 9.82 # F = m*g
y_meas = np.array([79_000, 62_000, 34_000, 29_000, 26_000])




# Fit the general exponential curve
popt, pcov = curve_fit(func, x_meas, y_meas, p0=[100_000, 0.01, 1])
a_est, b_est, c_est = popt
print(f"Estimated parameters: a = {a_est}, b = {b_est}, c = {c_est}")

# Generate estimated resistance values
x_est = np.linspace(x_meas[0], x_meas[-1], 100)
y_est = func(x_est, a_est, b_est, c_est)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(x, y_true, 'g-', label='True function')

plt.scatter(x_meas, y_meas, color='r', s=10, label='Noisy samples')

plt.plot(x_est, y_est, 'b--', label='Fitted function')

plt.xlabel('Force [N]')
plt.ylabel('Resistance [Ohm]')
plt.title('General Exponential Curve Fitting')
plt.legend()
plt.grid(True)
plt.show()


