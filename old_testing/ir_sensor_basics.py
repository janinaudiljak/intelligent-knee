import gpiod
import time

chipname = "gpiochip4" 
IR_PIN_OFFSET = 17

chip = gpiod.Chip(chipname)

line = chip.get_line(IR_PIN_OFFSET)

line.request(consumer="ir_sensor", type=gpiod.LINE_REQ_DIR_IN)

last_value = None

def on_color_change(event_type, offset):
    if event_type == gpiod.LINE_REQ_EV_FALLING_EDGE:
        print("White color detected! Halting...")
        raise KeyboardInterrupt
    else:  
        print("Black color detected.")

try:
    while True:
        value = line.get_value()
        
        time.sleep(0.1)  # Sleep briefly to avoid busy waiting
        
        if value:
            on_color_change(gpiod.LINE_REQ_EV_RISING_EDGE, IR_PIN_OFFSET)
        else:
            on_color_change(gpiod.LINE_REQ_EV_FALLING_EDGE, IR_PIN_OFFSET)

except KeyboardInterrupt:
    print("Program halted by user or color change.")
finally:
    line.release()
    chip.close()
