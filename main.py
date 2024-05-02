import gpiod
import time
chip = gpiod.Chip('gpiochip4')
data_ir_sen = chip.get_line(17)
data_ir_sen.request(consumer="IR_SEN", type=gpiod.LINE_REQ_DIR_OUT)
try:
   while True:
       data_ir_sen.set_value(1)
       time.sleep(1)
       data_ir_sen.set_value(0)
       time.sleep(1)
finally:
   data_ir_sen.release()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               