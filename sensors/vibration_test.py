from gpiozero import DigitalInputDevice
import time

# Define the GPIO pin for DOUT (BCM numbering)
vibration_pin = 27  # Purple wire connected to GPIO27

# Create input device (pull-up disabled for active-low sensor)
sensor = DigitalInputDevice(vibration_pin, pull_up=False)

print("MH Vibration Sensor Test - Press Ctrl+C to stop")
print("Adjust potentiometer for sensitivity if needed")

try:
    while True:
        if sensor.value == 0:  # LOW = vibration detected (active-low)
            print("Vibration DETECTED!")
        else:
            print("No vibration...")
        time.sleep(0.5)  # Check every 500ms
except KeyboardInterrupt:
    print("\nTest stopped.")
finally:
    # Cleanup (optional)
    sensor.close()
