import os

import myactuator_rmd_py as rmd
from myactuator_rmd import ActuatorException, ProtocolException, ValueRangeException
from myactuator_rmd import AccelerationType, ControlMode, ErrorCode
from myactuator_rmd import Gains #Class containing PI gains for current,speed, position contorller
from myactuator_rmd.actuator_constants import X6S2V2 as motor_model



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
        self.motor.sendTorqueSetpoint(torque, torque) #(float const torque, float const torque_constant)

    def set_velocity(self, velocity):
        if velocity > self.velocity_max:
            velocity = self.velocity

        self.motor.sendVelocitySetpoint(self, velocity)

    def set_position_abs(self, pos, vel):
        self.motor.sendPositionAbsoluteSetpoint(pos, vel) #(position, max_speed)

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
        self.motor.shutdown()
        print("Motor stopped.")