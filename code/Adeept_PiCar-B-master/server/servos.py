#!/usr/bin/python3
# File name   : servos.py
# Description : By controlling Servos,the camera and Ultrasonic scanner can move Up and down, left and right and
#             ; the steering can move to left and right.
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : wcb
# Date        : 1/24/2019

from __future__ import division

import sys
sys.path.insert(0, "../common")
import config

import time
import Adafruit_PCA9685

#import the settings for servos
HEAD_PITCH_MIDDLE    = config.importConfigInt('E_C1')
HEAD_PITCH_UP_MAX    = config.importConfigInt('look_up_max')
HEAD_PITCH_DOWN_MAX  = config.importConfigInt('look_down_max')
HEAD_YAW_MIDDLE      = config.importConfigInt('E_C2')
HEAD_YAW_RIGHT_MAX   = config.importConfigInt('look_right_max')
HEAD_YAW_LEFT_MAX    = config.importConfigInt('look_left_max')

STEERING_RIGHT_MAX  = config.importConfigInt('turn_right_max')
STEERING_LEFT_MAX   = config.importConfigInt('turn_left_max')
STEERING_MIDDLE     = config.importConfigInt('turn_middle')
heading = None

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)

STEERING_SERVO = 2
HEAD_YAW_SERVO = 1
HEAD_PITCH_SERVO = 0

def steer(position):
    global heading
    #print("turn_ang: %s" %ang)
    if position < STEERING_RIGHT_MAX:
        position = STEERING_RIGHT_MAX
    elif position > STEERING_LEFT_MAX:
        position = STEERING_LEFT_MAX
    else:
        pass
    pwm.set_pwm(STEERING_SERVO, 0, position)
    heading = position

def steeringRight():
    steer(STEERING_RIGHT_MAX)

def steeringLeft():
    steer(STEERING_LEFT_MAX)

def steeringMiddle():
    steer(STEERING_MIDDLE)

def headYaw(position):
    pwm.set_pwm(HEAD_YAW_SERVO, 0, position)

def headPitch(position):
    pwm.set_pwm(HEAD_PITCH_SERVO, 0, position)

def lookAhead():
	pwm.set_pwm(HEAD_YAW_SERVO, 0, HEAD_YAW_MIDDLE)
	pwm.set_pwm(HEAD_PITCH_SERVO, 0, HEAD_PITCH_MIDDLE)

steeringMiddle()   # call steeringMiddle() to center steering and init heading variable
