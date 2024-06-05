#Wrapper class for interfacing with actuator more easily, setup, teardown, etc

import os
import threading
import myactuator_rmd_py as rmd
from myactuator_rmd_py import ActuatorException, ProtocolException, ValueRangeException
from myactuator_rmd_py.actuator_state import AccelerationType, ControlMode, ErrorCode
from myactuator_rmd_py.actuator_constants import X6S2V2 as motor_model
import time
import random

class Motor:
    def __init__(self, fake=False):
        self.fake = fake
        if fake:
            return 
        
        # Set CAN0 speed to 1M bps
        os.system('sudo ifconfig can0 down')
        os.system('sudo ip link set can0 type can bitrate 1000000')
        os.system("sudo ifconfig can0 txqueuelen 100000")
        os.system('sudo ifconfig can0 up')

        self.driver = rmd.CanDriver("can0")
        self.motor = rmd.ActuatorInterface(self.driver, 1)

        self.velocity_max = 100

        # Set current position as angle=0
        m = self.motor
        m.setCurrentPositionAsEncoderZero()
        m.reset()
        time.sleep(1)

    def get_mode(self):
        if self.fake:
            return
        return self.motor.getControlMode()
    
    def get_status(self):
        if self.fake:
            return
        s1 = self.motor.getMotorStatus1()
        s2 = self.motor.getMotorStatus2()
        s3 = self.motor.getMotorStatus3()
        return (s1, s2, s3)
    
    def get_status2(self):
        if self.fake:
            return
        return self.motor.getMotorStatus2()

    def get_angle(self):
        if self.fake:
            return 0
        return self.motor.getMultiTurnAngle()
    
    def set_torque(self, torque):
        if self.fake:
            return
        self.motor.sendTorqueSetpoint(torque, motor_model.torque_constant)

    def set_velocity(self, velocity):
        if self.fake:
            return
        
        if velocity > self.velocity_max:
            velocity = self.velocity

        self.motor.sendVelocitySetpoint(velocity)

    def set_position_abs(self, pos, vel):
        if self.fake:
            return 
        self.motor.sendPositionAbsoluteSetpoint(pos, vel)

    def stop(self):
        if self.fake:
            return
        self.motor.stopMotor()

    def release(self):
        if self.fake:
            return
        self.motor.releaseBrake()




def monitor_angle(motor :Motor):
    stopped = False

    while True:
        try:
            angle = motor.get_angle()

            if not stopped and (angle < -5 or angle > 125):
                stopped = True
                motor.stop()
                # motor.motor.sendPositionAbsoluteSetpoint(120, 10000) 
                print(f"Angle out of range: {angle:.2f} deg. Motor stopped.")
            elif stopped and (angle >= 0 and angle <= 120):
                print("Angle within limits again, resetting safety")
                stopped = False
            
        except Exception as e:
            print(e)
        time.sleep(0.01)

if __name__ == "__main__":
    #Test out some basic motor commands via a basic command line interface
    import datetime
    motor = Motor()
    m = motor.motor

    m.setCurrentPositionAsEncoderZero()
    m.reset()
    time.sleep(1)

    monitor_thread = threading.Thread(target=monitor_angle, args=(motor,))
    monitor_thread.start()

    time_start = datetime.datetime.now()

    while True:
        user_input = input("Enter command: ")
        if user_input == "angle":
            try:
                angle = motor.get_angle()
                print(f"Current angle: {angle:.2f} deg")
            except Exception as e:
                print(e)
        elif user_input.startswith("torque"):
            try:
                _, torque_value = user_input.split()
                torque_value = float(torque_value)
                motor.set_torque(torque_value)
                torque_setpoint = torque_value
                print(f"Torque set to: {torque_value}")
            except Exception as e:
                print(e)
        elif user_input.startswith("speed"):
            _, speed = user_input.split()
            speed = float(speed)
            m.sendVelocitySetpoint(speed)
            print(f"Speed set to {speed}")
        elif user_input == "lock":
            m.lockBrake()
        elif user_input == "unlock":
            m.releaseBrake()
        elif user_input == "calibrate":
            m.setCurrentPositionAsEncoderZero()
            m.reset()
            time.sleep(1)
            print(f"Motor zero reset, current angle = {motor.get_angle()}")
        elif user_input == "stop":
            m.stopMotor()
        elif user_input == "shutdown":
            m.shutdownMotor()

        else:
            print(f"Unknown command: {user_input}")

        print("\n")
