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
import motor
import servos, headlights

#Set for motors
left_spd   = config.importConfigInt('E_M1')         #Speed of the car
right_spd  = config.importConfigInt('E_M2')         #Speed of the car
left       = config.importConfigInt('E_T1')         #Motor Left
right      = config.importConfigInt('E_T2')         #Motor Right

spd_ad_u = 1
Tr = 23
Ec = 24

def checkdist():       #Reading distance
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Tr, GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(Ec, GPIO.IN)
    GPIO.output(Tr, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(Tr, GPIO.LOW)
    while not GPIO.input(Ec):
        pass
    t1 = time.time()
    while GPIO.input(Ec):
        pass
    t2 = time.time()
    return (t2-t1)*340/2

def setup():          #initialization
    motor.setup()
    headlights.setup()

def destroy():        #motor stops when this program exit
    motor.destroy()
    GPIO.cleanup()

def loop(distance_stay, distance_range):   #Tracking with Ultrasonic
    motor.setup()
    headlights.setup()
    servos.ahead()
    servos.middle()
    dis = checkdist()
    if dis < distance_range:             #Check if the target is in diatance range
        if dis > (distance_stay+0.1) :   #If the target is in distance range and out of distance stay, then move forward to track
            servos.ahead()
            moving_time = (dis-distance_stay)/0.38
            if moving_time > 1:
                moving_time = 1
            print('mf')
            headlights.turn(headlights.BOTH, headlights.CYAN)
            motor.motorLeft(motor.BACKWARD, left_spd*spd_ad_u)
            motor.motorRight(motor.FORWARD, right_spd*spd_ad_u)
            time.sleep(moving_time)
            motor.motorStop()
        elif dis < (distance_stay-0.1) : #Check if the target is too close, if so, the car move back to keep distance at distance_stay
            moving_time = (distance_stay-dis)/0.38
            print('mb')
            headlights.turn(headlights.BOTH, headlights.PINK)
            motor.motorLeft(motor.FORWARD, left_spd*spd_ad_u)
            motor.motorRight(motor.BACKWARD, right_spd*spd_ad_u)
            time.sleep(moving_time)
            motor.motorStop()
        else:                            #If the target is at distance, then the car stay still
            motor.motorStop()
            headlights.turn(headlights.BOTH, headlights.YELLOW)
    else:
        motor.motorStop()

try:
    pass
except KeyboardInterrupt:
    destroy()
