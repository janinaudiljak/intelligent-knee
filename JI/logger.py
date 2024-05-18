# logger.py

import pandas as pd
from datetime import datetime

class DataLogger:
    def __init__(self):
        self.file_name = f"logs/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.columns = [
            'timestamp', 
            'p0', 'p1', 'p2', 'p3',
            'safety', 
            'temp', 'pos', 'vel', 'torque'
        ]

        self.df = pd.DataFrame(columns=self.columns)
        self.df.to_csv(self.file_name, index=False)

    def log_data(self, data: dict):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data['timestamp'] = timestamp

        self.df = pd.concat(
            [
                self.df, 
                pd.DataFrame([data])
            ], 
            ignore_index=True)
        
        self.df.iloc[[-1]].round(3).to_csv(self.file_name, mode='a', header=False, index=False)
        
