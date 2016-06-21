"""Classic Garoa Hardware Dojo Exercise

Light up segments on perimeter of display in sequence,
with delay set by potentiometer.

This script assumes:

- ``board.pins[13]`` is a ``DigitalPin``
- there is an LED attached to it

"""

from time import sleep
import pingo
from pingo import Mode

POT_LOCATION = 'A0'
PIN_LOCATIONS = range(6, 14)

board = pingo.detect.get_board()
pot = pingo.pins[POT_LOCATION]
leds = (pingo.pins[loc] for loc in PIN_LOCATIONS if loc != 9)

for led in leds:
    led.mode = Mode.OUT

while True:
    for led in leds:
        led.high()
        sleep(pot.ratio())
        led.low()
