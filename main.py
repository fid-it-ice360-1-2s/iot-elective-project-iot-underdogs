# vault.py - combine DHT, MQ-2, Vibration, RTC -> LED unlock
import time
from datetime import datetime, time as dt_time
import board, adafruit_dht
from gpiozero import DigitalInputDevice, LED

# CONFIG - tune these
TEMP_MIN, TEMP_MAX = 18.0, 28.0
HUMIDITY_MAX = 70.0
SMOKE_ALLOWED = False
ACCESS_WINDOW = ("09:00", "17:00")   # allowed time window
KNOCK_PATTERN = [0.25,0.25,0.5,0.25] # seconds between knocks
KNOCK_TOL = 0.15
KNOCK_TIMEOUT = 4.0

# pins (BCM)
DHT_PIN = board.D4
SMOKE_GPIO = 17
VIBE_GPIO = 27
LED_GPIO = 24

dht = adafruit_dht.DHT11(DHT_PIN)
smoke = DigitalInputDevice(SMOKE_GPIO)
vibe = DigitalInputDevice(VIBE_GPIO)
unlock_led = LED(LED_GPIO)

knocks = []

def parse_time(s):
    hh,mm = s.split(":"); return dt_time(int(hh), int(mm))

def in_window(now):
    start = parse_time(ACCESS_WINDOW[0]); end = parse_time(ACCESS_WINDOW[1])
    t = now.time()
    if start <= end: return start <= t <= end
    return t >= start or t <= end

def read_dht():
    for _ in range(3):
        try:
            t = dht.temperature; h = dht.humidity
            if t is not None and h is not None: return float(t), float(h)
        except RuntimeError:
            time.sleep(0.2)
    return None, None

def smoke_present():
    # if your module is active-low, invert this check
    return smoke.value == 1

def record_knock():
    global knocks
    now = time.monotonic()
    if knocks and (now - knocks[-1] > KNOCK_TIMEOUT): knocks = []
    knocks.append(now)

vibe.when_activated = lambda: record_knock()

def pattern_ok():
    if len(knocks) < len(KNOCK_PATTERN)+1: return False
    recent = knocks[-(len(KNOCK_PATTERN)+1):]
    gaps = [recent[i+1]-recent[i] for i in range(len(recent)-1)]
    for g,target in zip(gaps, KNOCK_PATTERN):
        if abs(g-target) > KNOCK_TOL: return False
    return True

print("Vault running. Ctrl+C to stop.")
try:
    while True:
        now = datetime.now()
        time_ok = in_window(now)
        t,h = read_dht()
        temp_ok = (t is not None and TEMP_MIN <= t <= TEMP_MAX)
        hum_ok = (h is not None and h <= HUMIDITY_MAX)
        smoke_ok = (SMOKE_ALLOWED or (not smoke_present()))
        knock_ok = pattern_ok()

        print(f"{now.strftime('%H:%M:%S')} | T={t} H={h} | temp_ok={temp_ok} hum_ok={hum_ok} smoke_ok={smoke_ok} time_ok={time_ok} knock_ok={knock_ok}")
        if temp_ok and hum_ok and smoke_ok and time_ok and knock_ok:
            print(">>> UNLOCKED <<<")
            unlock_led.on()
            time.sleep(5)
            unlock_led.off()
            knocks = []
        time.sleep(0.2)
except KeyboardInterrupt:
    print("Exiting")
