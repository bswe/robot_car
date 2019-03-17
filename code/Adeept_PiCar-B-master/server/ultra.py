#!/usr/bin/python3
# File name   : Ultrasonic.py
# Description : Detection distance and tracking with ultrasonic
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12

import sys
sys.path.insert(0, "../common")
import config
import RPi.GPIO as GPIO
import time
import atexit
import motor
import servos, headlights

#Set for motors
right_spd  = config.importConfigInt('E_M2')         #Speed of the car
left       = config.importConfigInt('E_T1')         #Motor Left
right      = config.importConfigInt('E_T2')         #Motor Right

spd_ad_u = 1
Tr = 23
Ec = 24

TIMEOUT = .5    # half a second


def checkDistance():       # perform ultrasonic distance check
    GPIO.output(Tr, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Tr, GPIO.LOW)
    startTimeout = time.time()
    while not GPIO.input(Ec):
        if (time.time() - startTimeout) > TIMEOUT:
            return 340          # somethings broken, so return an unrealistically large distance
    echoStartTime = time.time()
    while GPIO.input(Ec):
        if (time.time() - echoStartTime) > TIMEOUT:
            return 340          # somethings broken, so return an unrealistically large distance
    echoStopTime = time.time()
    return (echoStopTime - echoStartTime) * 170  # echo_delay_Time * 340/2   (speed of sound ~= 340 meters/second)


def loop(distance_stay, distance_range):   #Tracking with Ultrasonic
    servos.lookAhead()
    servos.steerMiddle()
    dis = checkDistance()
    if dis < distance_range:             #Check if the target is in diatance range
        if dis > (distance_stay+0.1) :   #If the target is in distance range and out of distance stay, then move forward to track
            moving_time = (dis-distance_stay)/0.38
            if moving_time > 1:
                moving_time = 1
            headlights.turn(headlights.BOTH, headlights.CYAN)
            motor.move(motor.FORWARD, right_spd*spd_ad_u)
            time.sleep(moving_time)
            motor.motorStop()
        elif dis < (distance_stay-0.1) : #Check if the target is too close, if so, the car move back to keep distance at distance_stay
            moving_time = (distance_stay-dis)/0.38
            headlights.turn(headlights.BOTH, headlights.PINK)
            motor.move(motor.BACKWARD, right_spd*spd_ad_u)
            time.sleep(moving_time)
            motor.motorStop()
        else:                            #If the target is at distance, then the car stay still
            motor.motorStop()
            headlights.turn(headlights.BOTH, headlights.YELLOW)
    else:
        motor.motorStop()


# initialization code, intentionally not in a method to encapsulate it within the module and to ensure its execution 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Tr, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Ec, GPIO.IN)
