#!/usr/bin/python3
# File name   : servos.py
# Description : By controlling Servo,the camera can move Up and down,left and right and the Ultrasonic wave can move to left and right.
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : wcb
# Date        : 1/24/2019

import sys
sys.path.insert(0, "../common")
import config

from __future__ import division
import time

import Adafruit_PCA9685

#import the settings for servos
vtr_mid_orig    = config.importConfigInt('E_C1')
hoz_mid_orig    = config.importConfigInt('E_C2')

turn_right_max  = config.importConfigInt('turn_right_max')
turn_left_max   = config.importConfigInt('turn_left_max')
turn_middle     = config.importConfigInt('turn_middle')
heading = None

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

STEERING_SERVO = 2
HEAD_YAW_SERVO = 1
HEAD_PITCH_SERVO = 0

def turn_ang(ang):
    global heading
    print("turn_ang: %s" %ang)
    if ang < turn_right_max:
        ang = turn_right_max
    elif ang > turn_left_max:
        ang = turn_left_max
    else:
        pass
    pwm.set_pwm(STEERING_SERVO, 0, ang)
    heading = ang

def right():
    turn_ang(turn_right_max)

def left():
    turn_ang(turn_left_max)

def middle():
    turn_ang(turn_middle)

def ultra_turn(hoz_mid):
    pwm.set_pwm(HEAD_YAW_SERVO, 0, hoz_mid)

def camera_turn(vtr_mid):
    pwm.set_pwm(HEAD_PITCH_SERVO, 0, vtr_mid)

def ahead():
	pwm.set_pwm(HEAD_YAW_SERVO, 0, hoz_mid_orig)
	pwm.set_pwm(HEAD_PITCH_SERVO, 0, vtr_mid_orig)

middle()   # call middle() to center steering and init heading variable
