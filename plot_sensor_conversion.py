import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
plt.close('all')

# Select file to use
file_name = "sensor/sensor2"
df = pd.read_csv(f"logs/{file_name}.csv")

# Convert the 'timestamp' column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['t'] = (df['timestamp'] - df['timestamp'][0]).dt.total_seconds()

# Set values to zero for time < 0.6 or time > 8.6 to make cleaner plot
df.loc[(df['t'] < 0.6) | (df['t'] > 8.5), ['r3', 'input3']] = 0

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.step(df['t'], df['r3']/1000, label='Input', color='blue')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Resistance [kΩ]', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True)
ax1.legend(loc='upper left')

ax2 = ax1.twinx()
ax2.step(df['t'], df['input3'], label='Output', color='red')
ax2.set_ylabel('Value', color='red')
ax2.tick_params(axis='y', labelcolor='red')
ax2.legend(loc='upper right')

try:
    plt.tight_layout()
    plt.show()
    
    import time
    
    time.sleep(0.1)
    fig.savefig(f"images/{file_name.split('/')[-1].split('.')[0]}.png")
    
    plt.close()
except KeyboardInterrupt as e:
    plt.close('all')
