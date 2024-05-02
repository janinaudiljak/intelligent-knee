"""
This file holds HX711 class
"""
#!/usr/bin/env python3

import statistics as stat
import time
import gpiod


class HX711:
    """
    HX711 represents chip for reading load cells.
    """
    def outliers_filter(self, data):
        """
        outliers_filter function filters the outliers from input data.
        
        Args:
            data(list): list of integers
        
        Returns:
            list: Filtered list of integers
        """
        data_len = len(data)
        data_mean = stat.mean(data)
        data_stddev = stat.stdev(data)
        filtered_data = []

        for i in range(0, data_len):
            if (data[i] >= (data_mean - (3 * data_stddev)) and
                    data[i] <= (data_mean + (3 * data_stddev))):
                filtered_data.append(data[i])
            else:
                if self._debug_mode:
                    print('Outlier detected. Removed {}'.format(data[i]))

        return filtered_data

    def __init__(self,
                 dout_pin,
                 pd_sck_pin,
                 gain_channel_A=128,
                 select_channel='A'):
        print("Initializing HX711")
    
    

        """
        Init a new instance of HX711

        Args:
            dout_pin(int): Raspberry Pi pin number where the Data pin of HX711 is connected.
            pd_sck_pin(int): Raspberry Pi pin number where the Clock pin of HX711 is connected.
            gain_channel_A(int): Optional, by default value 128. Options (128 || 64)
            select_channel(str): Optional, by default 'A'. Options ('A' || 'B')

        Raises:
            TypeError: if pd_sck_pin or dout_pin are not int type
        """
        if (isinstance(dout_pin, int)):
            if (isinstance(pd_sck_pin, int)):
                self._pd_sck = pd_sck_pin
                self._dout = dout_pin
            else:
                raise TypeError('pd_sck_pin must be type int. '
                                'Received pd_sck_pin: {}'.format(pd_sck_pin))
        else:
            raise TypeError('dout_pin must be type int. '
                            'Received dout_pin: {}'.format(dout_pin))

        self._gain_channel_A = 0
        self._offset_A_128 = 0  # offset for channel A and gain 128
        self._offset_A_64 = 0  # offset for channel A and gain 64
        self._offset_B = 0  # offset for channel B
        self._last_raw_data_A_128 = 0
        self._last_raw_data_A_64 = 0
        self._last_raw_data_B = 0
        self._wanted_channel = ''
        self._current_channel = ''
        self._scale_ratio_A_128 = 1  # scale ratio for channel A and gain 128
        self._scale_ratio_A_64 = 1  # scale ratio for channel A and gain 64
        self._scale_ratio_B = 1  # scale ratio for channel B
        self._debug_mode = False
        self._data_filter = self.outliers_filter  # default it is used outliers_filter

        self._chip = gpiod.Chip('gpiochip0')
        self._pd_sck_line = self._chip.get_line(self._pd_sck)
        self._dout_line = self._chip.get_line(self._dout)
        self._pd_sck_line.request(consumer='hx711', type=gpiod.LINE_REQ_DIR_OUT)
        self._dout_line.request(consumer='hx711', type=gpiod.LINE_REQ_DIR_IN)

        self.select_channel(select_channel)
        self.set_gain_A(gain_channel_A)

    def select_channel(self, channel):
        """
        select_channel method evaluates if the desired channel
        is valid and then sets the _wanted_channel variable.

        Args:
            channel(str): the channel to select. Options ('A' || 'B')
        Raises:
            ValueError: if channel is not 'A' or 'B'
        """
        channel = channel.capitalize()
        if (channel == 'A'):
            self._wanted_channel = 'A'
        elif (channel == 'B'):
            self._wanted_channel = 'B'
        else:
            raise ValueError('Parameter "channel" has to be "A" or "B". '
                             'Received: {}'.format(channel))
        # after changing channel or gain it has to wait 50 ms to allow adjustment.
        # the data before is garbage and cannot be used.
        print("Selecting channel:", channel)
        self._read()
        time.sleep(0.5)

    def set_gain_A(self, gain):
        """
        set_gain_A method sets gain for channel A.
        
        Args:
            gain(int): Gain for channel A (128 || 64)
        
        Raises:
            ValueError: if gain is different than 128 or 64
        """
        if gain == 128:
            self._gain_channel_A = gain
        elif gain == 64:
            self._gain_channel_A = gain
        else:
            raise ValueError('gain has to be 128 or 64. '
                             'Received: {}'.format(gain))
        # after changing channel or gain it has to wait 50 ms to allow adjustment.
        # the data before is garbage and cannot be used.
        self._read()
        time.sleep(0.5)

    def get_raw_data_mean(self, num_readings):
        """
        Calculate the mean of multiple readings from the HX711.

        Args:
            num_readings (int): The number of readings to average.

        Returns:
            float: The average of the readings.
        """
        if num_readings <= 0:
            raise ValueError("Number of readings must be greater than zero.")
        total = 0
        for _ in range(num_readings):
            total += self._read()
        return total / num_readings

    def get_weight_mean(self, times=10):
        """
        Calculates the mean weight from multiple readings.

        Args:
            times (int): The number of readings to average.

        Returns:
            float: The average weight.
        """
        total_weight = 0
        for _ in range(times):
            total_weight += self.get_units()
        return total_weight / times


    def zero(self, readings=30):
        """
        zero is a method which sets the current data as
        an offset for particulart channel. It can be used for
        subtracting the weight of the packaging. Also known as tare.

        Args:
            readings(int): Number of readings for mean. Allowed values 1..99

        Raises:
            ValueError: if readings are not in range 1..99

        Returns: True if error occured.
        """
        if readings > 0 and readings < 100:
            result = self.get_raw_data_mean(readings)
            if result != False:
                if (self._current_channel == 'A' and
                        self._gain_channel_A == 128):
                    self._offset_A_128 = result
                    return False
                elif (self._current_channel == 'A' and
                      self._gain_channel_A == 64):
                    self._offset_A_64 = result
                    return False
                elif (self._current_channel == 'B'):
                    self._offset_B = result
                    return False
                else:
                    if self._debug_mode:
                        print('Cannot zero() channel and gain mismatch.\n'
                              'current channel: {}\n'
                              'gain A: {}\n'.format(self._current_channel,
                                                    self._gain_channel_A))
                    return True
            else:
                if self._debug_mode:
                    print('From method "zero()".\n'
                          'get_raw_data_mean(readings) returned False.\n')
                return True
        else:
            raise ValueError('Parameter "readings" '
                             'can be in range 1 up to 99. '
                             'Received: {}'.format(readings))

    def set_offset(self, offset, channel='', gain_A=0):
        """
        set offset method sets desired offset for specific
        channel and gain. Optional, by default it sets offset for current
        channel and gain.
        
        Args:
            offset(int): specific offset for channel
            channel(str): Optional, by default it is the current channel.
                Or use these options ('A' || 'B')
        
        Raises:
            ValueError: if channel is not ('A' || 'B' || '')
            TypeError: if offset is not int type
        """
        channel = channel.capitalize()
        if isinstance(offset, int):
            if channel == 'A' and gain_A == 128:
                self._offset_A_128 = offset
                return
            elif channel == 'A' and gain_A == 64:
                self._offset_A_64 = offset
                return
            elif channel == 'B':
                self._offset_B = offset
                return
            elif channel == '' and self._wanted_channel == 'A' and self._gain_channel_A == 128:
                self._offset_A_128 = offset
                return
            elif channel == '' and self._wanted_channel == 'A' and self._gain_channel_A == 64:
                self._offset_A_64 = offset
                return
            elif channel == '' and self._wanted_channel == 'B':
                self._offset_B = offset
                return
            else:
                raise ValueError('Parameter "channel" has to be "A" or "B". '
                                 'Received: {}'.format(channel))
        else:
            raise TypeError('offset must be type int. '
                            'Received: {}'.format(offset))

    def get_offset(self, channel='', gain_A=0):
        """
        get_offset method returns offset for channel and gain.
        
        Args:
            channel(str): Optional, by default it is the current channel.
                Or use these options ('A' || 'B')
        
        Returns:
            int: Offset for channel and gain.
        
        Raises:
            ValueError: if channel is not ('A' || 'B' || '')
        """
        channel = channel.capitalize()
        if channel == 'A' and gain_A == 128:
            return self._offset_A_128
        elif channel == 'A' and gain_A == 64:
            return self._offset_A_64
        elif channel == 'B':
            return self._offset_B
        elif channel == '' and self._wanted_channel == 'A' and self._gain_channel_A == 128:
            return self._offset_A_128
        elif channel == '' and self._wanted_channel == 'A' and self._gain_channel_A == 64:
            return self._offset_A_64
        elif channel == '' and self._wanted_channel == 'B':
            return self._offset_B
        else:
            raise ValueError('Parameter "channel" has to be "A" or "B". '
                             'Received: {}'.format(channel))

    def set_scale_ratio(self, scale_ratio, channel='', gain_A=0):
        """
        set_scale_ratio method sets desired scale ratio for specific
        channel and gain. Optional, by default it sets scale ratio for current
        channel and gain.
        
        Args:
            scale_ratio(float): specific scale ratio for channel
            channel(str): Optional, by default it is the current channel.
                Or use these options ('A' || 'B')
        
        Raises:
            ValueError: if channel is not ('A' || 'B' || '')
            TypeError: if scale_ratio is not float type
        """
        channel = channel.capitalize()
        if isinstance(scale_ratio, float):
            if channel == 'A' and gain_A == 128:
                self._scale_ratio_A_128 = scale_ratio
                return
            elif channel == 'A' and gain_A == 64:
                self._scale_ratio_A_64 = scale_ratio
                return
            elif channel == 'B':
                self._scale_ratio_B = scale_ratio
                return
            elif channel == '' and self._wanted_channel == 'A' and self._gain_channel_A == 128:
                self._scale_ratio_A_128 = scale_ratio
                return
            elif channel == '' and self._wanted_channel == 'A' and self._gain_channel_A == 64:
                self._scale_ratio_A_64 = scale_ratio
                return
            elif channel == '' and self._wanted_channel == 'B':
                self._scale_ratio_B = scale_ratio
                return
            else:
                raise ValueError('Parameter "channel" has to be "A" or "B". '
                                 'Received: {}'.format(channel))
        else:
            raise TypeError('scale_ratio must be type float. '
                            'Received: {}'.format(scale_ratio))

    def get_scale_ratio(self, channel='', gain_A=0):
        """
        get_scale_ratio method returns scale ratio for channel and gain.
        
        Args:
            channel(str): Optional, by default it is the current channel.
                Or use these options ('A' || 'B')
        
        Returns:
            float: Scale ratio for channel and gain.
        
        Raises:
            ValueError: if channel is not ('A' || 'B' || '')
        """
        channel = channel.capitalize()
        if channel == 'A' and gain_A == 128:
            return self._scale_ratio_A_128
        elif channel == 'A' and gain_A == 64:
            return self._scale_ratio_A_64
        elif channel == 'B':
            return self._scale_ratio_B
        elif channel == '' and self._wanted_channel == 'A' and self._gain_channel_A == 128:
            return self._scale_ratio_A_128
        elif channel == '' and self._wanted_channel == 'A' and self._gain_channel_A == 64:
            return self._scale_ratio_A_64
        elif channel == '' and self._wanted_channel == 'B':
            return self._scale_ratio_B
        else:
            raise ValueError('Parameter "channel" has to be "A" or "B". '
                             'Received: {}'.format(channel))

    def set_debug_mode(self, debug_mode):
        """
        set_debug_mode method sets the debug mode
        to trace the problem during operations.
        
        Args:
            debug_mode(bool): Optional, by default False
        """
        self._debug_mode = debug_mode

    def outliers_filter(self, data):
        """
        outliers_filter function filters the outliers
        from input data.
        
        Args:
            data(list): list of integers
        
        Returns:
            list: Filtered list of integers
        """
        data_len = len(data)
        data_mean = stat.mean(data)
        data_stddev = stat.stdev(data)
        filtered_data = []

        for i in range(0, data_len):
            if (data[i] >= (data_mean - (3 * data_stddev)) and
                    data[i] <= (data_mean + (3 * data_stddev))):
                filtered_data.append(data[i])
            else:
                if self._debug_mode:
                    print('Outlier detected. Removed {}'.format(data[i]))

        return filtered_data

    def _read(self):
        """
        _read method reads raw data from the HX711.
        Returns:
            int: Raw data.
        """
        # Power up the HX711
        self._pd_sck_line.set_value(0)

        # wait for the HX711 to become ready.
        while (self._dout_line.get_value() == 1):
            pass

        # Read raw data
        raw_data = 0
        for i in range(0, 24):
            self._pd_sck_line.set_value(1)
            raw_data = (raw_data << 1) | self._dout_line.get_value()
            self._pd_sck_line.set_value(0)
        for i in range(0, self._gain_channel_A):
            self._pd_sck_line.set_value(1)
            self._pd_sck_line.set_value(0)

        # Set channel A or B
        if (self._wanted_channel == 'A'):
            self._current_channel = 'A'
        else:
            self._current_channel = 'B'

        # If channel A selected, add offset and scale
        if (self._current_channel == 'A'):
            if (self._gain_channel_A == 128):
                raw_data = raw_data ^ 0x800000
                self._current_offset = self._offset_A_128
                self._current_scale_ratio = self._scale_ratio_A_128
            else:
                self._current_offset = self._offset_A_64
                self._current_scale_ratio = self._scale_ratio_A_64
        else:
            self._current_offset = self._offset_B
            self._current_scale_ratio = self._scale_ratio_B

        return raw_data

    def _read_average(self, times=3):
        """
        _read_average method reads the average raw data 
        from the HX711 for given times.
        
        Args:
            times(int): Optional, by default 3
        
        Returns:
            int: Average raw data.
        """
        sum = 0
        for i in range(0, times):
            sum += self._read()
        return sum / times

    def _get_value(self, times=3):
        """
        _get_value method reads the value from the HX711 for given times.
        
        Args:
            times(int): Optional, by default 3
        
        Returns:
            float: Scale ratio multiplied by average value.
        """
        value = self._read_average(times) - self._current_offset
        return value / self._current_scale_ratio

    def get_units(self, times=3):
        """
        get_units method reads the value from the HX711 for given times.
        
        Args:
            times(int): Optional, by default 3
        
        Returns:
            float: Scale ratio multiplied by average value.
        """
        return self._get_value(times)

hx = HX711(dout_pin=4, pd_sck_pin=18)


hx.zero()

input('Place known weight on scale & press Enter') # get a reading
reading = hx.get_raw_data_mean(num_readings=100) #more for calibration purposes

known_weight_grams = input('Enter the known weight in grams & press Enter:') # asks the user to type in the known weight
value = float(known_weight_grams) # gives the value as a decimal
ratio = reading/value
hx.set_scale_ratio(ratio)

while True: 
    weight = hx.get_weight_mean()
    print(weight)
    

