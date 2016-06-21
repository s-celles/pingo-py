import pingo
from pingo import Mode
from time import sleep

rpi = pingo.rpi.RaspberryPi()

#                 A  B   C   D   E   F  G   dp
led_locations = [11, 7, 21, 24, 26, 13, 15, 19]

pins = [rpi.pins[loc] for loc in led_locations[:6]]

for pin in pins:
    pin.mode = Mode.OUT
    pin.low()

while True:
    for pin in pins:
        pin.high()
        sleep(.04)
        pin.low()
