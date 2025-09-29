import RPi.GPIO as GPIO
import time

# GPIO pin
SMOKE_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(SMOKE_PIN, GPIO.IN)

try:
    while True:
        if GPIO.input(SMOKE_PIN) == GPIO.LOW:  # Active low on most MQ2 modules
            print("?? Smoke/Gas detected!")
        else:
            print("? Air is clean.")
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()

