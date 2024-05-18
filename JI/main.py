# main.py

import time
import traceback
from sensors import PressureSensor, SafetySensor, Motor
from logger import DataLogger

def initialize_sensors():
    pressure_sensors = [PressureSensor(i) for i in range(1, 5)]
    safety_sensor = SafetySensor()
    motor = Motor()
    return pressure_sensors, safety_sensor, motor

def main():
    pressure_sensors, safety_sensor, motor = initialize_sensors()
    data_logger = DataLogger()

    try:
        while True:
            data = {
                'p0': pressure_sensors[0].read(),
                'p1': pressure_sensors[1].read(),
                'p2': pressure_sensors[2].read(),
                'p3': pressure_sensors[3].read(),
                'safety': safety_sensor.read(),
                'temp': motor.read_temp(),
                'pos': motor.read_position(),
                'vel': motor.read_velocity(),
                'torque': motor.read_acceleration()
            }
            data_logger.log_data(data)
            print("Saved data")
            time.sleep(1)  # Adjust the sleep time as needed

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

    finally:
        motor.stop()

if __name__ == "__main__":
    main()
