import time
import board
import adafruit_dht

dht_device = adafruit_dht.DHT22(board.D4)
max_reads = 10
count = 0

while count < max_reads:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print("Temp: {} C  Humidity: {} %".format(temperature, humidity))
        count += 1
    except RuntimeError as e:
        print("Error reading sensor:", e)
    time.sleep(2)

dht_device.exit()
print("Finished reading sensor.")
