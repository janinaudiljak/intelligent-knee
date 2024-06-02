# main.py

import time
import traceback
from sensors import PressureSensor, SafetySensor
from motor import Motor
from logger import DataLogger
from pprint import pprint
import os

def initialize_sensors():
    pressure_sensors = PressureSensor()
    safety_sensor = SafetySensor(fake=True)
    motor = Motor(fake=True)
    return pressure_sensors, safety_sensor, motor

def main():
    pressure_sensors, safety_sensor, motor = initialize_sensors()
    data_logger = DataLogger()

    try:
        while True:
            safety = safety_sensor.read() 
            # if safety:
            #     motor.stop()
            #     break

            data = {
                'p0': pressure_sensors.read(0),
                'p1': pressure_sensors.read(1),
                'p2': pressure_sensors.read(2),
                'p3': pressure_sensors.read(3),

                'v0': pressure_sensors.read_voltage(0),
                'v1': pressure_sensors.read_voltage(1),
                'v2': pressure_sensors.read_voltage(2),
                'v3': pressure_sensors.read_voltage(3),

                'r0': pressure_sensors.read_resistance(0),
                'r1': pressure_sensors.read_resistance(1),
                'r2': pressure_sensors.read_resistance(2),
                'r3': pressure_sensors.read_resistance(3),

                'f0': pressure_sensors.read_linear(0),
                'f1': pressure_sensors.read_linear(1),
                'f2': pressure_sensors.read_linear(2),
                'f3': pressure_sensors.read_linear(3),

                'safety': safety_sensor.read(),
                'temp': motor.read_temp(),
                'pos': motor.read_position(),
                'vel': motor.read_velocity(),
                'torque': motor.read_acceleration()
            }
            data_logger.log_data(data)
            os.system('cls' if os.name == 'nt' else 'clear')
            pprint(data)
            time.sleep(0.1)  # Adjust the sleep time as needed
    except KeyboardInterrupt as e:
        print("Exiting")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


    finally:
        motor.stop()

if __name__ == "__main__":
    main()
