# sensors.py

import random
import time
import Adafruit_ADS1x15
import gpiod

import can
import myactuator_rmd_py as rmd
import os
import numpy as np

from gpiod.line import Direction, Value


def adc_2_voltage(cnt, max, Vcc_adc, Vcc):
    u = Vcc_adc / max * cnt
    u[u > Vcc] = Vcc # Since the ADS adc has internal ref which has different voltage from rpi, saturate
    return u

def R2(u, R1, Vcc):
    # u[u > Vcc] = Vcc
    R2 = R1 * u / (Vcc - u)
    # R2 = np.nan_to_num(R2, 0)
    R2[R2 < 0] = 0
    R2[R2 > 1_000_000] = 0
    return R2


class PressureSensor:
    def __init__(self, gain=1, fake=False, num_channels=4):
        self.gain = gain
        self.fake = fake
        self.channels = num_channels

        self.R1 = 4700
        self.VCC_ADC = 4.096 # Using gain=1 uses reference of 4.096V
        self.ADC_MAX = 2**11 - 1 #Single ended measurement uses 11 bits
        self.VCC = 3.3

        if not fake:
            self.adc = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=1)
    
    def adc_2_voltage(self, cnt):
        u = self.VCC_ADC / self.ADC_MAX * cnt
        if u > self.VCC: # Since the ADS adc has internal ref which has different voltage from rpi, saturate
            u = self.VCC
        return u
    
    def voltage_2_resistance(self, u):
        # u[u > Vcc] = Vcc
        denominator = (self.VCC - u)
        if denominator == 0:
            return 0
        
        R2 = self.R1 * u / (self.VCC - u)
        R2 = np.clip(R2, 0, 200_000)
        return R2

    def adc_2_force(self, cnt):
        # return self.voltage_2_resistance(self.adc_2_voltage(cnt))
        return self.resistance_2_force(self.voltage_2_resistance(self.adc_2_voltage(cnt)))
    
    def read_linear(self, channel=0, min=0, max=6):
        # Convert R = f(Force) which is a exponential decaying function to a linear model
        # Model is not accurate and output doesn't represent physical unit
        # Only used to get a linear response between min/max based on observed measurements
        R0 = 1_000
        A = 200e3
        scale_factor = 10
        R = self.read_resistance(channel=channel)
        u = (R - R0) / A
        if u <= 0.01: # log can't handle 0
            return 0
        
        output = np.exp( -np.log(u) )/ scale_factor
        output = np.nan_to_num(output, nan=0, posinf=0, neginf=0)
        return output
    

    def read_voltage(self, channel=0):
        return self.adc_2_voltage(self.read(channel))

    def read_resistance(self, channel=0):
        return self.voltage_2_resistance(self.adc_2_voltage(self.read(channel)))

    
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
