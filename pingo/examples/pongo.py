"""
A simplified PONG clone developed in a couple of hours at the
Intel IoT Roadshow in São Paulo, Brazil, by Ricardo Banffy and
Luciano Ramalho.

The hardware setup is a Galileo Gen 2 connected to an Arduino,
each with a potentiometer in pin A0 (we used Garoa Dojo shields).
The script runs on the Galileo, and the display is a terminal
on any computer connected to the Galileo.
"""


# flake8: noqa

import curses
import pingo
from pingo import Mode
import time
import random

PADDLE_SIZE = 5
MIN_X = 0
MIN_Y = 0
MAX_X = 79
MAX_Y = 24

score_1 = 0
score_2 = 0

def init_ball():
    return ([39, 12],
        random.choice([ # [1, 0],
            [1, 1],     # [-1, 0],
            [-1, 1], [1, -1]]))

def new_ball_pos(pos, velocity):
    x = pos[0] + velocity[0]
    y = pos[1] + velocity[1]
    return (x, y)

def draw_paddle(x, y, color):
    for offset in range(PADDLE_SIZE):
        screen.addstr(y + offset, x, ' ', color)

if __name__ == '__main__':

    screen = curses.initscr()
    curses.noecho()
    curses.cbreak()
    try:
        curses.curs_set(False)
    except:
        pass
    screen.clear()
    curses.start_color()

    # Initializes the color pairs we'll use (black on white and white on black)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    ball_pos, ball_velocity = init_ball()

    # Start communicating with the local and remote sensors
    galileo = pingo.detect.get_board()
    arduino = pingo.arduino.get_arduino()

    pot_galileo = galileo.pins['A0']
    pot_galileo.mode = Mode.ANALOG

    pot_arduino = arduino.pins['A0']
    pot_arduino.mode = Mode.ANALOG

    # Read the initial values of the paddles
    paddle_1_pos = int(pot_arduino.ratio(to_min=MIN_Y, to_max=MAX_Y-PADDLE_SIZE))
    paddle_2_pos = int(pot_galileo.ratio(to_min=MIN_Y, to_max=MAX_Y-PADDLE_SIZE))

    while True:
        # Erases the paddles for the previous moment
        draw_paddle(MIN_X, paddle_1_pos, curses.color_pair(2))
        draw_paddle(MAX_X, paddle_2_pos, curses.color_pair(2))

        # Erase the ball
        screen.addstr(ball_pos[1], ball_pos[0], ' ', curses.color_pair(2))

        # Read current paddle positions
        paddle_1_pos = int(pot_arduino.ratio(to_min=MIN_Y, to_max=MAX_Y-PADDLE_SIZE))
        paddle_2_pos = int(pot_galileo.ratio(to_min=MIN_Y, to_max=MAX_Y-PADDLE_SIZE))

        # If left border collision, increase score and invert vx
        if ball_pos[0] <= MIN_X:
            ball_velocity[0] = - ball_velocity[0]
            # Check whether we collided with a paddle
            if not paddle_1_pos < ball_pos[1] < paddle_1_pos + PADDLE_SIZE:
                ball_pos, ball_velocity = init_ball()

        # If right border collision, increase score and invert vx
        if ball_pos[0] >= MAX_X:
            ball_velocity[0] = - ball_velocity[0]
            # Check whether we collided with a paddle
            if not paddle_2_pos < ball_pos[1] < paddle_2_pos + PADDLE_SIZE:
                ball_pos, ball_velocity = init_ball()

        # If top or botton collision, invert vy
        if not MIN_Y < ball_pos[1] < MAX_Y:
            ball_velocity[1] = - ball_velocity[1]

        ball_pos = new_ball_pos(ball_pos, ball_velocity)

        screen.addstr(ball_pos[1], ball_pos[0], ' ', curses.color_pair(1))
        draw_paddle(MIN_X, paddle_1_pos, curses.color_pair(1))
        draw_paddle(MAX_X, paddle_2_pos, curses.color_pair(1))

        screen.refresh()

        time.sleep(0.05)
