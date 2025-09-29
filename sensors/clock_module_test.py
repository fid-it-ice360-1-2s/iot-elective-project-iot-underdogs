import time
from datetime import datetime

try:
    import RTC_DS1302  # Import the RTC_DS1302 module
except ImportError:
    print("Error: RTC_DS1302 library not found. Ensure RTC_DS1302.py is in /home/user/vault_system/sensors.")
    exit(1)

# Pin definitions for MH RTC 2 sensor (DS1302-based, CLK=GPIO5, DAT=GPIO6, RST=GPIO12)
CLK_PIN = 29  # Physical pin 29 (GPIO5)
DAT_PIN = 31  # Physical pin 31 (GPIO6)
RST_PIN = 32  # Physical pin 32 (GPIO12)

# Initialize MH RTC 2 sensor
print("Initializing MH RTC 2 sensor (DS1302-based)...")
try:
    rtc = RTC_DS1302.RTC_DS1302(clk_pin=CLK_PIN, dat_pin=DAT_PIN, rst_pin=RST_PIN)  # Use the RTC_DS1302 class
except Exception as e:
    print(f"Error initializing MH RTC 2 sensor: {e}")
    exit(1)

# Check if MH RTC 2 has a valid time
try:
    current_time = rtc.get_time()
    if current_time.year < 2000:  # DS1302 starts at 2000
        print("MH RTC 2 time is invalid. Setting time from system clock.")
        rtc.set_time(datetime.now())
        print(f"Time set to: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
except Exception as e:
    print(f"Error reading MH RTC 2 time: {e}")
    rtc.close()
    exit(1)

# Main loop: Read and print time from MH RTC 2 every 5 seconds
try:
    while True:
        try:
            current_time = rtc.get_time()
            print(f"MH RTC 2 Current Time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            print(f"Error reading MH RTC 2: {e}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped reading MH RTC 2 sensor.")
finally:
    try:
        rtc.close()  # Clean up GPIO
    except Exception as e:
        print(f"Error closing MH RTC 2: {e}")
