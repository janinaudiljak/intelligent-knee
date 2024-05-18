import os
import can
import myactuator_rmd_py as rmd
import code

# Define the encoder limits
MIN_ENCODER_POSITION = -83037160
MAX_ENCODER_POSITION = -82226231

# Define the counts per revolution (example value, adjust based on your actuator's specs)
COUNTS_PER_REVOLUTION = 4096

def angle_to_encoder_counts(angle):
    """Convert an angle in degrees to encoder counts."""
    return int((angle / 360.0) * COUNTS_PER_REVOLUTION)

if __name__ == "__main__":
    # Set CAN0 speed to 1M bps
    os.system('sudo ifconfig can0 down')
    os.system('sudo ip link set can0 type can bitrate 1000000')
    os.system("sudo ifconfig can0 txqueuelen 100000")
    os.system('sudo ifconfig can0 up')

    driver = rmd.CanDriver("can0")
    m = rmd.ActuatorInterface(driver, 1)
    m.getVersionDate()

    # Set the specific position -83037160 as zero
    m.setEncoderZero(-83037160)
    print("Zero offset set to -83037160")

    # Optional: Verify the current position
    current_position = m.getMultiTurnEncoderPosition()
    print(f"Current Position after zeroing: {current_position}")

    def within_limits(position):
        """Check if the given position is within the specified encoder limits."""
        return MIN_ENCODER_POSITION <= position <= MAX_ENCODER_POSITION

    def move_to_position(position):
        """Move to the specified position if within limits."""
        if within_limits(position):
            m.sendPositionAbsoluteSetpoint(position, 500.0)  # Adjust speed as necessary
            print(f"Moving to position: {position}")
        else:
            print(f"Position {position} is out of bounds. Movement aborted.")

    def move_to_angle(angle):
        """Move the actuator to the specified angle in degrees."""
        encoder_counts = angle_to_encoder_counts(angle)
        move_to_position(encoder_counts)
        print(f"Moving to angle: {angle} degrees (encoder counts: {encoder_counts})")

    # Test moving to a specific angle
    move_to_angle(90)  # Example: Move to 90 degrees

    # Uncomment these lines if you want to shut down the motor after operations
    # m.shutdownMotor()

    # Start interactive console
    code.interact(local=dict(globals(), **locals()))