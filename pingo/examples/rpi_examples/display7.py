import pingo
from pingo import Mode
import time

rpi = pingo.rpi.RaspberryPi()

led_locations = [7, 11, 13, 15, 19, 21, 24, 26]

pins = [pin for _, pin in sorted(rpi.pins.items())
        if pin.location in led_locations]

for pin in pins:
    pin.mode = Mode.OUT

for pin in pins:
    pin.high()

time.sleep(2)
