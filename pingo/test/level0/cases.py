import time
import unittest

import pingo
from pingo.board import Mode, State

'''
In order to use this set of cases, it is necessary to set
the following attributes on your TestCase setUp:
    self.vdd_pin_number = 2
    self.digital_output_pin_number = 13
    self.digital_input_pin_number = 8
    self.total_pins = 26

AND the VDD pin must be connected to the digital_input_pin_number
'''


class BoardBasics(object):

    def test_list_pins(self):
        vdd_pin = self.board.pins[self.vdd_pin_number]
        assert isinstance(vdd_pin, pingo.VccPin)

        pin = self.board.pins[self.digital_output_pin_number]
        assert isinstance(pin, pingo.DigitalPin)

        assert len(self.board.pins) == self.total_pins

    def test_led(self):
        pin = self.board.pins[self.digital_output_pin_number]
        pin.mode = Mode.OUT
        pin.high()

    def test_filter(self):
        pins_subset = self.board.filter_pins(pingo.DigitalPin)
        assert all(isinstance(pin, pingo.DigitalPin) for pin in pins_subset)

        other_pins = set(self.board.pins.values()) - set(pins_subset)
        assert not any(isinstance(pin, pingo.DigitalPin) for pin in other_pins)

    @unittest.skip("Not automatic enough.")
    def test_button(self):
        pin = self.board.pins[self.digital_input_pin_number]
        pin.mode = Mode.IN
        output = State.LOW
        t0 = time.time()
        delay = 5

        while output == State.LOW:
            output = pin.state
            if time.time() - t0 > delay:
                break

        # TODO: show message on fail
        # msg = 'The button must be pressed in %ss for this test to pass' % delay
        assert output == pingo.HIGH

    def test_jumpwire(self):
        ''' Wire this DigitalPin directly into VDD '''
        pin = self.board.pins[self.digital_input_pin_number]
        pin.mode = Mode.IN
        output = pin.state

        assert output == State.HIGH

    def test_toggle(self):
        pin = self.board.pins[self.digital_input_pin_number]
        pin.mode = Mode.OUT
        pin.high()
        pin.toggle()

        assert pin.state == State.LOW

    def test_digital_pins(self):
        digital_pins = self.board.digital_pins
        # TODO:
        # assert len(digital_pins) == self.len_digital_pins
        assert len(digital_pins) > 0

    def test_select(self):
        selected_pins = self.board.select_pins([
            self.digital_input_pin_number,
            self.digital_output_pin_number
        ])
        assert len(selected_pins) == 2


class BoardExceptions(object):

    def test_disabled_pin(self):
        pin = self.board.pins[self.digital_output_pin_number]
        with self.assertRaises(pingo.WrongPinMode):
            pin.high()

    def test_wrong_pin_mode_in(self):
        pin = self.board.pins[self.digital_input_pin_number]
        pin.mode = Mode.IN

        with self.assertRaises(pingo.WrongPinMode):
            pin.high()

        with self.assertRaises(pingo.WrongPinMode):
            pin.state = State.HIGH

#    def test_wrong_pin_mode_out(self):
#        pin = self.board.pins[digital_output_pin_number]
#        pin.mode = pingo.OUT
#        with self.assertRaises(pingo.WrongPinMode) as cm:
#            pin.state
