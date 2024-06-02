import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = "logs/data_20240601_161716.csv"
data = pd.read_csv(file_path)

# Parse the timestamp column as datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Set timestamp as the index
data.set_index('timestamp', inplace=True)

# Plot the data
fig, axes = plt.subplots(nrows=6, ncols=1)
fig.suptitle('Data Variables Over Time', fontsize=16)

# Plot pressure sensors in the first subplot
axes[0].plot(data.index, data['p0'], label='p0')
axes[0].plot(data.index, data['p1'], label='p1')
axes[0].plot(data.index, data['p2'], label='p2')
axes[0].plot(data.index, data['p3'], label='p3')
axes[0].set_title('Pressure Sensors')
axes[0].set_xlabel('Time')
axes[0].set_ylabel('Pressure')
axes[0].legend()
axes[0].grid(True)

# Plot the remaining variables in separate subplots
variables = ['safety', 'temp', 'pos', 'vel', 'torque']

for i, var in enumerate(variables, start=1):
    ax = axes[i]
    ax.plot(data.index, data[var])
    ax.set_title(var.capitalize())
    ax.set_xlabel('Time')
    ax.set_ylabel(var.capitalize())
    ax.grid(True)

# plt.tight_layout()
plt.show()
