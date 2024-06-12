# Script for running main control program 

import time
import traceback
from sensors import PressureSensor, SafetySensor
from myactuator_rmd_py import ActuatorException, ProtocolException, ValueRangeException
from myactuator_rmd_py.actuator_constants import X6S2V2 as motor_model
from motor import Motor
from logger import DataLogger
from pprint import pprint
from math import sqrt
import os
import numpy as np



import pandas as pd
from datetime import datetime

class DataLogger:
    def __init__(self):
        # self.file_name = f"logs/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.columns = [
            'timestamp', 'torque', 'ref_torque'
        ]

        self.df = pd.DataFrame(columns=self.columns)
        # self.df.to_csv(self.file_name, index=False)
        self.df.to_csv("logs/torque_data.csv", index=False)

    def log_data(self, data: dict):
        timestamp = datetime.now().isoformat(sep=' ', timespec='milliseconds')
        data['timestamp'] = timestamp

        self.df = pd.concat(
            [
                self.df, 
                pd.DataFrame([data])
            ], 
            ignore_index=True)
        self.df.iloc[[-1]].round(3).to_csv("logs/torque_data.csv", mode='a', header=False, index=False)
        



# Aboslute max torques the actuator should produce
TORQUE_ABS_MAX = 3
MAX_TORQUE = TORQUE_ABS_MAX
MIN_TORQUE = -TORQUE_ABS_MAX

def main():
    motor= Motor(fake=False)
    data_logger = DataLogger()

    try:

        k = 0
        ref_torque = 0
        k_times = 250

        while True:
            if k == 0:
                ref_torque = 0
                motor.set_torque(ref_torque)
            elif k == k_times*1:
                ref_torque = MAX_TORQUE
                motor.set_torque(ref_torque)
            elif k == k_times*2:
                ref_torque = 0
                motor.set_torque(ref_torque)
            elif k == k_times*3:
                ref_torque = MIN_TORQUE
                motor.set_torque(ref_torque)
            elif k == k_times*4:
                ref_torque = 0
                motor.set_torque(ref_torque)
                
            k = k+1

            # Read measured Iq current and convert to torque via torque constant. [A]
            # 2/sqrt(3) converts AC torque constant to DC torque constant [Nm/A]
            torque = motor.get_status2().current * motor_model.torque_constant  * 2/sqrt(3)

            data = {'torque': torque,  'ref_torque': ref_torque}
            data_logger.log_data(data)
            # os.system('cls' if os.name == 'nt' else 'clear')
            # pprint(data)
            # time.sleep(0.01)  
    except ProtocolException as e:
        pass
    except KeyboardInterrupt as e:
        print("Exiting")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


    finally:
        # Stop engages break, Release removes break
        # motor.stop()
        motor.set_torque(0)
        motor.release() 

if __name__ == "__main__":
    main()

