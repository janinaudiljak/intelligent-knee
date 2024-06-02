
import time
import traceback
from sensors import PressureSensor, SafetySensor
from motor import Motor
from logger import DataLogger
from pprint import pprint
import os
import numpy as np

def initialize_sensors():
    pressure_sensors = PressureSensor()
    safety_sensor = SafetySensor(fake=True)
    motor = Motor(fake=False)

    
    return pressure_sensors, safety_sensor, motor

def main():
    pressure_sensors, safety_sensor, motor = initialize_sensors()
    data_logger = DataLogger()

    try:
        while True:
            # if safety:
            #     motor.stop()
            #     break
            angle = motor.get_angle()
            u2 = pressure_sensors.read_linear(2)
            u3 = pressure_sensors.read_linear(3)

            delta = 3*u3- 2*u2
            ref_torque = np.clip(delta, -5, 5)
            motor.set_torque(ref_torque)
            

            data = {
                'adc0': pressure_sensors.read(0),
                'adc1': pressure_sensors.read(1),
                'adc2': pressure_sensors.read(2),
                'adc3': pressure_sensors.read(3),

                'r0': pressure_sensors.read_resistance(0),
                'r1': pressure_sensors.read_resistance(1),
                'r2': pressure_sensors.read_resistance(2),
                'r3': pressure_sensors.read_resistance(3),

                'input0': pressure_sensors.read_linear(0),
                'input1': pressure_sensors.read_linear(1),
                'input2': pressure_sensors.read_linear(2),
                'input3': pressure_sensors.read_linear(3),

                'safety': safety_sensor.read(),
                'temp': 0,
                'pos': angle,
                'vel': 0,
                'torque': ref_torque
            }
            data_logger.log_data(data)
            os.system('cls' if os.name == 'nt' else 'clear')
            pprint(data)
            time.sleep(0.01)  # Takes about 4.5ms 
    except KeyboardInterrupt as e:
        print("Exiting")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


    finally:
        motor.stop()

if __name__ == "__main__":
    main()

