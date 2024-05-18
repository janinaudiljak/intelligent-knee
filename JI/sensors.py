# sensors.py

import random
import time
import Adafruit_ADS1x15
import gpiod

class PressureSensor:
    def __init__(self, gain=1, fake=True, num_channels=4):
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

    def __init__(self, pin=17, fake=True):
        self.pin = pin
        self.fake = fake

        if self.fake:
            self.chip = gpiod.Chip("gpiochip4" )
            self.line = self.chip.get_line(self.pin)
            self.line.request(consumer="ir_sensor", type=gpiod.LINE_REQ_DIR_IN)

    def read(self):
        if self.fake:
            random.choice([0, 1])

        return self.line.get_value()
    
    def __del__(self):
        if self.fake:
            return
        
        self.line.release()
        self.chip.close()

    def __str__(self):
        return f"IR sensor: {self.read()}"

class Motor:
    def __init__(self):
        self.temp = 0
        self.position = 0
        self.velocity = 0
        self.acceleration = 0

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
        print("Motor stopped.")
