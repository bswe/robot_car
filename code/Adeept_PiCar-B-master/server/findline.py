#!/usr/bin/python3
# File name   : findline.py
# Description : line tracking 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : wcb
# Date        : 1/24/2019

import sys
sys.path.insert(0, "../common")
import config
import RPi.GPIO as GPIO
import time
import motor
import servos
import headlights

right_spd  = config.importConfigInt('E_M2')         #Speed of the car
left       = config.importConfigInt('E_T1')         #Motor Left
right      = config.importConfigInt('E_T2')         #Motor Right

line_pin_right = 35
line_pin_middle = 36
line_pin_left = 38

spd_ad_1 = 1
spd_ad_2 = 1

def setup():
    GPIO.setwarnings(True)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(line_pin_right, GPIO.IN)
    GPIO.setup(line_pin_middle, GPIO.IN)
    GPIO.setup(line_pin_left, GPIO.IN)
    motor.setup()

def run():
    status_right = GPIO.input(line_pin_right)
    status_middle = GPIO.input(line_pin_middle)
    status_left = GPIO.input(line_pin_left)
    if status_left == 1:
        servos.steeringLeft()
        headlights.turn(headlights.BOTH, headlights.OFF)
        headlights.turn(headlights.LEFT, headlights.RED)
        motor.move(motor.FORWARD, right_spd*spd_ad_2)
    elif status_middle == 1:
        servos.steeringMiddle()
        headlights.turn(headlights.BOTH, headlights.YELLOW)
        motor.move(motor.FORWARD, right_spd*spd_ad_1)
    elif status_right == 1:
        servos.steeringRight()
        headlights.turn(headlights.BOTH, headlights.OFF)
        headlights.turn(headlights.RIGHT, headlights.RED)
        motor.move(motor.FORWARDBACKWARD, right_spd*spd_ad_2)
    else:
        servos.steeringMiddle()
        headlights.turn(headlights.BOTH, headlights.CYAN)
        motor.move(motor.BACKWARD, right_spd)

try:
    pass
except KeyboardInterrupt:
    motor.motorStop()
