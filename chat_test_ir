import gpiod
import time

# Set up GPIO using chip name and line offset
chipname = "gpiochip0"  # This is usually gpiochip0 on Raspberry Pi
IR_PIN_OFFSET = 18  # GPIO pin number

# Open GPIO chip
chip = gpiod.Chip(chipname)

# Get the GPIO line
line = chip.get_line(IR_PIN_OFFSET)

# Request the line and configure it for input
line.request(consumer="ir_sensor", type=gpiod.LINE_REQ_DIR_IN)

# Function to be called when interrupt is triggered
def on_color_change(event_type, offset):
    if event_type == gpiod.LINE_EVENT_RISING_EDGE:  # If input is HIGH (white color)
        print("White color detected! Halting...")
        # Put your code here to halt/stop whatever process you need to interrupt
        # For example, you can raise an exception to stop the program:
        raise KeyboardInterrupt
    else:  # If input is LOW (black color)
        print("Black color detected.")

# Add event detection to the GPIO line
line.request_event(gpiod.LINE_EVENT_RISING_EDGE | gpiod.LINE_EVENT_FALLING_EDGE, callback=on_color_change)

try:
    while True:
        # Main program loop
        # You can put your main code logic here
        # This loop will be interrupted when a color change is detected
        time.sleep(0.1)  # Adjust the sleep time as needed
except KeyboardInterrupt:
    print("Program halted by user or color change.")
finally:
    # Clean up GPIO
    line.release()
    chip.close()
