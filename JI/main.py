# main.py

import time
import traceback
from sensors import PressureSensor, SafetySensor, Motor
from logger import DataLogger
from pprint import pprint
import os

def initialize_sensors():
    pressure_sensors = PressureSensor()
    safety_sensor = SafetySensor()
    motor = Motor()
    return pressure_sensors, safety_sensor, motor

def main():
    pressure_sensors, safety_sensor, motor = initialize_sensors()
    data_logger = DataLogger()

    try:
        while True:
            safety = safety_sensor.read() 
            if safety:
                motor.stop()
                break

            data = {
                'p0': pressure_sensors.read(0),
                'p1': pressure_sensors.read(1),
                'p2': pressure_sensors.read(2),
                'p3': pressure_sensors.read(3),
                'safety': safety_sensor.read(),
                'temp': motor.read_temp(),
                'pos': motor.read_position(),
                'vel': motor.read_velocity(),
                'torque': motor.read_acceleration()
            }
            data_logger.log_data(data)
            os.system('cls' if os.name == 'nt' else 'clear')
            pprint(data)
            time.sleep(0.5)  # Adjust the sleep time as needed

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

    finally:
        motor.stop()

if __name__ == "__main__":
    main()
