import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

plt.close('all')

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('logs/data_latest.csv')

# Convert the 'timestamp' column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['t'] = (df['timestamp'] - df['timestamp'][0]).dt.total_seconds()

fig, ax = plt.subplots(4, 1, figsize=(10, 10), sharex=True)

# Plot initialization
lines = []
lines.append(ax[0].step([], [], label='position')[0])
lines.append(ax[1].step([], [], label='reference torque')[0])
lines.append(ax[2].step([], [], label='r2')[0])
lines.append(ax[2].step([], [], label='r3')[0])
lines.append(ax[3].step([], [], label='f2')[0])
lines.append(ax[3].step([], [], label='f3')[0])

for axis in ax:
    axis.grid(True)
    axis.legend()

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def update(frame):
    t = df['t'][:frame]
    
    lines[0].set_data(t, df['pos'][:frame])
    ax[0].relim()
    ax[0].autoscale_view()

    lines[1].set_data(t, df['torque'][:frame])
    ax[1].relim()
    ax[1].autoscale_view()

    lines[2].set_data(t, df['r2'][:frame])
    lines[3].set_data(t, df['r3'][:frame])
    ax[2].relim()
    ax[2].autoscale_view()

    lines[4].set_data(t, df['input2'][:frame])
    lines[5].set_data(t, df['input3'][:frame])
    ax[3].relim()
    ax[3].autoscale_view()

    return lines

# Set up the animation
ani = animation.FuncAnimation(fig, update, frames=len(df), init_func=init, blit=True, interval=55, repeat=False)

# Save the animation as an MP4 file
ani.save('animation.mp4', writer='ffmpeg', fps=18)

plt.close('all')
