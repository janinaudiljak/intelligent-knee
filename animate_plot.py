# Animate a plot in realtime and save as mp4 video

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

plt.close('all')

# Read the CSV file into a pandas DataFrame
file_name = "passive2"
df = pd.read_csv(f"logs/{file_name}.csv")

# Convert the 'timestamp' column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['t'] = (df['timestamp'] - df['timestamp'][0]).dt.total_seconds()

fig, ax = plt.subplots(5, 1, figsize=(10, 10), sharex=True)

# Plot initialization
lines = []
lines.append(ax[0].step([], [], label='position')[0])
lines.append(ax[1].step([], [], label='velocity')[0])
lines.append(ax[2].step([], [], label='reference torque')[0])
lines.append(ax[3].step([], [], color="green", label='input1')[0])
lines.append(ax[3].step([], [], color="orange", label='input2')[0])
lines.append(ax[4].step([], [], color="red", label='safety')[0])
ax[0].set_ylabel('[deg]')
ax[1].set_ylabel('[deg/s]')
ax[3].set_ylabel('[Nm]')
ax[4].set_xlabel("Time [s]")

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

    lines[1].set_data(t, df['vel'][:frame])
    ax[1].relim()
    ax[1].autoscale_view()

    lines[2].set_data(t, df['torque'][:frame])
    ax[2].relim()
    ax[2].autoscale_view()

    lines[3].set_data(t, df['input0'][:frame])
    lines[4].set_data(t, df['input3'][:frame])
    ax[3].relim()
    ax[3].autoscale_view()

    lines[5].set_data(t, df['safety'][:frame])
    ax[4].relim()
    ax[4].autoscale_view()

    return lines

# Set up the animation
ani = animation.FuncAnimation(fig, update, frames=len(df), init_func=init, blit=False, interval=55, repeat=False)
# plt.show()
# Save the animation as an MP4 file
ani.save(f"videos/{file_name}.mp4", writer='ffmpeg', fps=18)

plt.close('all')
