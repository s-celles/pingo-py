import pingo
from pingo import Mode

rpi = pingo.rpi.RaspberryPi()

led_locations = [7, 11, 13, 15, 19, 21, 24, 26]

pins = [rpi.pins[loc] for loc in led_locations]

for pin in pins:
    pin.mode = Mode.OUT
    pin.low()

for pin in pins:
    pin.high()
    raw_input('Lit: pin %s' % pin.location)
    pin.low()
