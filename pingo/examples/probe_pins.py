""" Sets each pin to high and waits for [ENTER]

This script is useful to map the connections of digital output pins to
a circuit such as a 7-segment display.
"""

import sys

import pingo
from pingo import Mode


def probe(first, last):
    board = pingo.detect.get_board()
    print('Found: %r' % board)

    pins = board.digital_pins[first:last + 1]

    for pin in pins:
        pin.mode = Mode.OUT

    for pin in pins:
        pin.hi()
        raw_input(pin)
        pin.lo()


if __name__ == '__main__':
    try:
        first, last = (int(arg) for arg in sys.argv[1:])
        probe(first, last)
    except ValueError:
        print('Usage: %s <first_pin> <last_pin>' % sys.argv[0])
        sys.exit(-1)
