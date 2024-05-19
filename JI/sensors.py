# sensors.py

import random
import time
import Adafruit_ADS1x15
import gpiod

import can
import myactuator_rmd_py as rmd
import os

from gpiod.line import Direction, Value

class PressureSensor:
    def __init__(self, gain=1, fake=False, num_channels=4):
        self.gain = gain
        self.fake = fake
        self.channels = num_channels

        if not fake:
            self.adc = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=1)

    def convert_to_force(self, adc_counts):
        # Implement conversion from adc_counts -> voltage -> resistance -> force/pressure
        return adc_counts
        voltage = adc_counts / 2096 * 3.3
        pressure = voltage * 1
    
    def read(self, channel=0):
        if self.fake:
            return random.uniform(0, 2096)
        
        return self.adc.read_adc(channel, self.gain)
    
    def read_all(self):
        if self.fake:
            return [random.uniform(0,2096) for _ in range(0, self.channels)]
        
        return [self.adc.read_adc(channel, self.gain) for channel in range(0, self.channels)]
    
    def __str__(self):
        data = self.read_all()
        output = [f"Channel {channel}: {reading}" for channel, reading in enumerate(data)]
        return "\n".join(output)

class SafetySensor:

    def __init__(self, pin=17, fake=False):
        self.pin = pin
        self.fake = fake

        if not self.fake:
            self.line = line = gpiod.request_lines(
                "/dev/gpiochip4",
                consumer="get-line-value",
                config={self.pin: gpiod.LineSettings(direction=Direction.INPUT)},
        )

    def read(self):
        if self.fake:
            return random.choice([0, 1])

        return 0 if self.line.get_value(self.pin) == Value.ACTIVE else 1
    
    def __del__(self):
        if self.fake:
            return 
        self.line.release()

    def __str__(self):
        return f"IR sensor: {self.read()}"

class Motor:
    def __init__(self):
        #Set CAN0 speed to 1M bps
        os.system('sudo ifconfig can0 down')
        os.system('sudo ip link set can0 type can bitrate 1000000')
        os.system("sudo ifconfig can0 txqueuelen 100000")
        os.system('sudo ifconfig can0 up')

        self.driver = rmd.CanDriver("can0")
        self.motor = rmd.ActuatorInterface(self.driver, 1)

        self.velocity_max = 100

        self.temp = 0
        self.position = 0
        self.velocity = 0
        self.acceleration = 0

    def get_mode(self):
        return self.motor.getControlMode()
    
    def get_status(self):
        s1 = self.motor.getMotorStatus1()
        s2 = self.motor.getMotorStatus2()
        s3 = self.motor.getMotorStatus3()
        return (s1, s2, s3)

    def get_angle(self):
        return self.motor.getMultiTurnAngle()
    
    def set_torque(self, torque):
        self.motor.sendTorqueSetpoint(torque, torque)

    def set_velocity(self, velocity):
        if velocity > self.velocity_max:
            velocity = self.velocity

        self.motor.sendVelocitySetpoint(self, velocity)

    def set_position_abs(self, pos, vel):
        self.motor.sendPositionAbsoluteSetpoint(pos, vel)

    def read_temp(self):
        # Simulate reading motor temperature
        return random.uniform(20, 80)

    def read_position(self):
        # Simulate reading motor position
        return random.uniform(0, 1000)

    def read_velocity(self):
        # Simulate reading motor velocity
        return random.uniform(0, 100)

    def read_acceleration(self):
        # Simulate reading motor acceleration
        return random.uniform(0, 10)

    def stop(self):
        self.motor.stopMotor()
        self.motor.shutdownMotor()
        print("Motor stopped.")
