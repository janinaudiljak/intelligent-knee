import os
from plot import plot_experiment

def process_all_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory, filename)
            plot_experiment(file_path, ignore_plotting=True)

if __name__ == "__main__":
    process_all_files("logs/saved")