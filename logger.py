# logger.py

import pandas as pd
from datetime import datetime

class DataLogger:
    def __init__(self):
        self.file_name = f"logs/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.columns = [
            'timestamp', 
            'p0', 'p1', 'p2', 'p3',
            'adc0', 'adc1', 'adc2', 'adc3',
            'v0', 'v1', 'v2', 'v3',
            'r0', 'r1', 'r2', 'r3',
            'f0', 'f1', 'f2', 'f3',
            'input0', 'input1', 'input2', 'input3',
            'safety', 
            'temp', 'pos', 'vel', 'torque'
        ]

        self.df = pd.DataFrame(columns=self.columns)
        self.df.to_csv(self.file_name, index=False)
        self.df.to_csv("logs/data_latest.csv", index=False)

    def log_data(self, data: dict):
        timestamp = datetime.now().isoformat(sep=' ', timespec='milliseconds')
        data['timestamp'] = timestamp

        self.df = pd.concat(
            [
                self.df, 
                pd.DataFrame([data])
            ], 
            ignore_index=True)
        
        self.df.iloc[[-1]].round(3).to_csv(self.file_name, mode='a', header=False, index=False)
        self.df.iloc[[-1]].round(3).to_csv("logs/data_latest.csv", mode='a', header=False, index=False)
        
