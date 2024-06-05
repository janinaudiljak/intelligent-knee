# Script for running main control program 

import time
import traceback
from sensors import PressureSensor, SafetySensor
from myactuator_rmd_py import ActuatorException, ProtocolException, ValueRangeException
from motor import Motor
from logger import DataLogger
from pprint import pprint
import os
import numpy as np


# Aboslute max torques the actuator should produce
TORQUE_ABS_MAX = 3
MAX_TORQUE = TORQUE_ABS_MAX
MIN_TORQUE = -TORQUE_ABS_MAX

def initialize_sensors():
    pressure_sensors = PressureSensor()
    safety_sensor = SafetySensor(fake=False)
    motor = Motor(fake=False)

    
    return pressure_sensors, safety_sensor, motor

def main():
    pressure_sensors, safety_sensor, motor = initialize_sensors()
    data_logger = DataLogger()

    flag_bounds = False
    prev_flag_bounds = False
    motor_disabled = True

    flag_safety = False
    prev_safety = safety_sensor.read()

    if motor_disabled:
        motor.release()

    try:
        # Loop takes about 5ms accoring to logged data => 200Hz frequency
        while True:
            angle = motor.get_angle()
            safety = safety_sensor.read()
            u2 = pressure_sensors.read_linear(0)
            u3 = pressure_sensors.read_linear(3)
            # s1, s2, s3 = motor.get_status()
            s2 = motor.get_status2()

            # if (safety == True and prev_safety == False):
            #     flag_safety = True

            # Calculate torque reference as the difference between sensors because they will be loaded when mounted on person
            # Due to sensor differences they are scaled to match 
            delta = 6*u3- 4*u2
            ref_torque = np.clip(delta, a_min=MIN_TORQUE, a_max=MAX_TORQUE)
            ref_torque_raw = np.clip(delta, a_min=MIN_TORQUE, a_max=MAX_TORQUE)
            speed = s2.shaft_speed
            

            # Safety stops 
            # Assuming it is starting in the straight position and bent knee results in positive angle
            # angle < 10 deg => only allowed to apply positive torque 
            # angle > (125-10) deg => only allowed to apply negative torque
            margin = 10 # 10 deg
            angle_max = 120
            angle_min = 0
            # Clip torque when close to endpoints
            inside_min_range = angle > (angle_max - margin)
            inside_max_range = angle < (angle_min + margin)
            inside_limits = inside_min_range or inside_max_range

            # Clipping used to still be able to drive leg in the opposite direction
            if inside_min_range:
                flag_bounds = True
                ref_torque = np.clip(delta, a_min=MIN_TORQUE, a_max=0)
            elif inside_max_range:
                flag_bounds = True
                ref_torque = np.clip(delta, a_min=0, a_max=MAX_TORQUE)
            else:
                flag_bounds = False

            if motor_disabled:
                # motor.release()
                pass
            elif (flag_bounds != prev_flag_bounds) and inside_limits:
                sign = np.sign(ref_torque_raw)
                print(f"STOP: (speed = {speed})")

                if np.abs(speed) > 230:
                    motor.set_torque(-15*sign)
                    time.sleep(0.08)
                elif np.abs(speed) > 170:
                    motor.set_torque(-10*sign)
                    time.sleep(0.1)

                motor.stop()
            else:
                motor.set_torque(ref_torque)

            
            prev_flag_bounds = flag_bounds
            prev_safety = safety

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
                'temp': s2.temperature,
                'pos': angle,
                'vel': s2.shaft_speed,
                'torque': ref_torque
            }
            data_logger.log_data(data)
            os.system('cls' if os.name == 'nt' else 'clear')
            pprint(data)
            time.sleep(0.01)  
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
        motor.release() 

if __name__ == "__main__":
    main()

