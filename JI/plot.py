import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.close('all')

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('logs/data_latest.csv')

# Convert the 'timestamp' column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['t'] = (df['timestamp'] - df['timestamp'][0]).dt.total_seconds()


fig, ax = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

# Plot the variables p0, p1, p2, and p3 on the first subplot
# ax[0].step(df['t'], df['adc0'], label='p0')
# ax[0].step(df['t'], df['adc1'], label='p1')
# ax[0].step(df['t'], df['adc2'], label='p2')
# ax[0].step(df['t'], df['adc3'], label='p3')
ax[0].step(df['t'], df['pos'], label='position')
ax[0].set_ylabel('position')
ax[0].grid(True)
ax[0].legend()

# ax[1].step(df['t'], df['v0']  , label='v0')
# ax[1].step(df['t'], df['v1']  , label='v1')
# ax[1].step(df['t'], df['v2']  , label='v2')
# ax[1].step(df['t'], df['v3']  , label='v3')
ax[1].step(df['t'], df['torque']  , label='reference torque')
ax[1].set_ylabel('Torque [Nm]')
ax[1].grid(True)
ax[1].legend()

# ax[2].step(df['t'], df['r0']  , label='r0')
# ax[2].step(df['t'], df['r1']  , label='r1')
ax[2].step(df['t'], df['r2']  , label='r2')
ax[2].step(df['t'], df['r3']  , label='r3')
ax[2].set_ylabel('Reistance [Ohm]')
ax[2].grid(True)
ax[2].legend()

# ax[3].step(df['t'], df['input0'] , label='f0')
# ax[3].step(df['t'], df['input1'] , label='f1')
ax[3].step(df['t'], df['input2'] , label='f2')
ax[3].step(df['t'], df['input3'] , label='f3')
ax[3].set_ylabel('')

ax[3].grid(True)
ax[3].legend()

# ax[1].step(df['t'], df['f0'], label='f0')
# ax[1].step(df['t'], df['f1'] , label='f1')
# ax[1].step(df['t'], df['f2'] , label='f2')
# ax[1].step(df['t'], df['f3'], label='f3')
# ax[1].set_ylabel('Mass [kg]')
# ax[1].grid(True)
# ax[1].legend()


# Show the plot
try:
    plt.tight_layout()
    plt.show()
except KeyboardInterrupt as e:
    plt.close('all')


# Max value is 4096