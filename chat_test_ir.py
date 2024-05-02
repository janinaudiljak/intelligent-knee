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

try:
    while True:
        event = line.event_wait(timeout=None)  # Wait indefinitely for events
        event_type = event.event_type
        on_color_change(event_type, IR_PIN_OFFSET)
except KeyboardInterrupt:
    print("Program halted by user or color change.")
finally:
    line.release()
    chip.close()
