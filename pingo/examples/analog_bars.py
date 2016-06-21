import pingo
from pingo import Mode
import time

board = pingo.detect.get_board()
# board = pingo.arduino.get_arduino()

pot = board.pins['A0']
pot.mode = Mode.ANALOG


def bar(pin):
    print "*" * int(pin.ratio() * 70)

while True:
    bar(pot)
    time.sleep(0.05)
