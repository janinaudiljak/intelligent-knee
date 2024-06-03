#import all necessary functionality to the Script
import time
import Adafruit_ADS1x15


adc = Adafruit_ADS1x15.ADS1015(address=0x48, busnum=1)
# Choose a gain of 1 for reading voltages from 0 to 4.09V.
GAIN0 = 1
GAIN1 = 1
GAIN2 = 1
GAIN3 = 1

#To boost small signals, the gain can be adjusted on the ADS1x15 chips in the following steps:
#GAIN_TWOTHIRDS (for an input range of +/- 6.144V)
#GAIN_ONE (for an input range of +/-4.096V)
#GAIN_TWO (for an input range of +/-2.048V)
#GAIN_FOUR (for an input range of +/-1.024V)
#GAIN_EIGHT (for an input range of +/-0.512V)
#GAIN_SIXTEEN (for an input range of +/-0.256V)

while True:
    values0 = adc.read_adc(0, gain=GAIN0) #1652-950
    # print("pin0: ", values0)
    # time.sleep(0.1)

    values1 = adc.read_adc(1, gain=GAIN1) #1652-
    # print("pin1: ", values1)
    # time.sleep(0.1)

    values2 = adc.read_adc(2, gain=GAIN2) #1652-650
    # print("pin2: ", values2)
    # time.sleep(0.1)

    values3 = adc.read_adc(3, gain=GAIN3) #254-222 KONSTIG!
    # print("pin3: ", values3)
    # time.sleep(0.1)


    print(f"{values0}, {values1}, {values2}, {values3}")
    time.sleep(0.1)
