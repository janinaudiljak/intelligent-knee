import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_experiment(file_path, ignore_plotting=False):
    plt.close('all')

    # Load data from file
    df = pd.read_csv(file_path)

    # Convert the 'timestamp' column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['t'] = (df['timestamp'] - df['timestamp'][0]).dt.total_seconds()

    fig, ax = plt.subplots(5, 1, figsize=(10, 10), sharex=True)

    # Plot
    # ax[0].step(df['t'], df['pos'], label='position')
    # ax[0].set_ylabel('Angular pos [deg]')
    # ax[0].grid(True)
    # ax[0].legend()

    # ax[1].step(df['t'], df['vel'], label='velocity')
    # ax[1].set_ylabel('Angular vel. [deg/s]')
    # ax[1].grid(True)
    # ax[1].legend()

    # ax[2].step(df['t'], df['input0'], color="green", label='f0')
    # # ax[2].step(df['t'], df['input1'], label='f1')
    # # ax[2].step(df['t'], df['input2'], label='f2')
    # ax[2].step(df['t'], df['input3'], color="orange", label='f3')
    # ax[2].set_ylabel('Input')
    # ax[2].grid(True)
    # ax[2].legend()

    ax[3].step(df['t'], df['ref_torque'], label='Ref. Torque')
    ax[3].plot(df['t'], df['torque'], label='Meas. Torque')
    ax[3].plot(df['t'], df['torque'].rolling(window=10, min_periods=1, center=True).mean(), label='Filt. rolling mean n=10, centered')
    # ax[3].plot(df['t'], moving_average(df['torque'].to_list(), 10), label='Meas. Torque')
    ax[3].set_ylabel('Torque [Nm]')
    ax[3].grid(True)
    ax[3].legend()

    # ax[4].step(df['t'], df['safety'], color="red", label='Safety')
    # ax[4].grid(True)
    # ax[4].legend()
    # ax[4].set_xlabel('Time [s]')
    # ax[4].set_ylabel('Safety')

    try:
        if not ignore_plotting:
            plt.tight_layout()
            plt.show()
            
            import time
            time.sleep(0.1)

        fig.savefig(f"images/{file_path.split('/')[-1].split('.')[0]}.png")
        
        plt.close()
    except KeyboardInterrupt as e:
        plt.close('all')

if __name__ == "__main__":
    plot_experiment("logs/torque_data.csv")
