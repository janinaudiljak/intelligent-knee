import gpiod
import time

chipname = "gpiochip0" 
IR_PIN_OFFSET = 17

chip = gpiod.Chip(chipname)

line = chip.get_line(IR_PIN_OFFSET)

line.request(consumer="ir_sensor", type=gpiod.LINE_REQ_DIR_IN)

def on_color_change(event_type, offset):
    if event_type == gpiod.LINE_EVENT_RISING_EDGE:
        print("White color detected! Halting...")
       
        raise KeyboardInterrupt
    else:  
        print("Black color detected.")


line.request_event(gpiod.LINE_EVENT_RISING_EDGE | gpiod.LINE_EVENT_FALLING_EDGE, callback=on_color_change)

try:
    while True:
        time.sleep(0.1) 
except KeyboardInterrupt:
    print("Program halted by user or color change.")
finally:
    line.release()
    chip.close()
