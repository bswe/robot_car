#!/usr/bin/python3
# File name   : headlights.py
# Description : Control headlight LEDs 
# Website     : github.com/bswe
# E-mail      : billbollenba@yahoo.com
# Author      : WCB
# Date        : 2/11/2019

import RPi.GPIO as GPIO
import time
import atexit

# light state constants
OFF    = 0
RED    = 1
GREEN  = 2
BLUE   = 3
YELLOW = 4
PINK   = 5
CYAN   = 6
WHITE  = 7

# light target constants
LEFT  = 8
RIGHT = 9
BOTH  = 10


def turn (target, state):
    # encapsulate these so module details are safe and not accessable
    # constants for the GPIO pins connected to the headlight LEDs
    LEFT_R = 15
    LEFT_G = 16
    LEFT_B = 18

    RIGHT_R = 19
    RIGHT_G = 21
    RIGHT_B = 22

    def ledOn(led):
        GPIO.output(led, GPIO.LOW)

    def ledOff (led):
        GPIO.output (led, GPIO.HIGH)

    def turnOffOneLight (target):
        if target == LEFT:
            ledOff (LEFT_R)
            ledOff (LEFT_G)
            ledOff (LEFT_B)
        elif target == RIGHT:
            ledOff (RIGHT_R)
            ledOff (RIGHT_G)
            ledOff (RIGHT_B)
        else:
            print ("turnOffOneLight: unknown target %s" %str(target))
            pass
            
    def turnOff (target):
        if target == BOTH:
            turnOffOneLight (LEFT)
            turnOffOneLight (RIGHT)
        else:
            turnOffOneLight (target) 

    def turnRedOneLight (target):
        if target == LEFT:
            ledOn (LEFT_R)
        elif target == RIGHT:
            ledOn (RIGHT_R)
        else:
            print ("turnRedOneLight: unknown target %s" %str(target))
            
    def turnRed (target):
        turnOff (target)
        if target == BOTH:
            turnRedOneLight (LEFT)
            turnRedOneLight (RIGHT)
        else:
            turnRedOneLight (target) 
            
    def turnGreenOneLight (target):
        if target == LEFT:
            ledOn (LEFT_G)
        elif target == RIGHT:
            ledOn (RIGHT_G)
        else:
            print ("turnGreenOneLight: unknown target %s" %str(target))
            
    def turnGreen (target):
        turnOff (target)
        if target == BOTH:
            turnGreenOneLight (LEFT)
            turnGreenOneLight (RIGHT)
        else:
            turnGreenOneLight (target) 
            
    def turnBlueOneLight (target):
        if target == LEFT:
            ledOn (LEFT_B)
        elif target == RIGHT:
            ledOn (RIGHT_B)
        else:
            print ("turnBlueOneLight: unknown target %s" %str(target))
            
    def turnBlue (target):
        turnOff (target)
        if target == BOTH:
            turnBlueOneLight (LEFT)
            turnBlueOneLight (RIGHT)
        else:
            turnBlueOneLight (target) 
            
    def turnYellowOneLight (target):
        turnRedOneLight (target)
        turnGreenOneLight (target)
            
    def turnYellow (target):
        turnOff (target)
        if target == BOTH:
            turnYellowOneLight (LEFT)
            turnYellowOneLight (RIGHT)
        else:
            turnYellowOneLight (target) 
            
    def turnPinkOneLight (target):
        turnRedOneLight (target)
        turnBlueOneLight (target)
            
    def turnPink (target):
        turnOff (target)
        if target == BOTH:
            turnPinkOneLight (LEFT)
            turnPinkOneLight (RIGHT)
        else:
            turnPinkOneLight (target) 
            
    def turnCyanOneLight (target):
        turnGreenOneLight (target)
        turnBlueOneLight (target)
            
    def turnCyan (target):
        turnOff (target)
        if target == BOTH:
            turnCyanOneLight (LEFT)
            turnCyanOneLight (RIGHT)
        else:
            turnCyanOneLight (target) 
            
    def turnWhiteOneLight (target):
        turnRedOneLight (target)
        turnGreenOneLight (target)
        turnBlueOneLight (target)
            
    def turnWhite (target):
        turnOff (target)
        if target == BOTH:
            turnWhiteOneLight (LEFT)
            turnWhiteOneLight (RIGHT)
        else:
            turnWhiteOneLight (target) 
            
    if state == OFF:
        turnOff (target)
    elif state == RED:
        turnRed (target)
    elif state == GREEN:
        turnGreen (target)
    elif state == BLUE:
        turnBlue (target)
    elif state == YELLOW:
        turnYellow (target)
    elif state == PINK:
        turnPink (target)
    elif state == CYAN:
        turnCyan (target)
    elif state == WHITE:
        turnWhite (target)
    else:
        print ("turn: unknown state %s" %str(state))


def blinker (target, times):
    for i in range (1, times):
        turn (target, OFF)
        turn (target, YELLOW)
        time.sleep(0.5)
        turn (target, OFF)
        time.sleep(0.5)


def police (police_time):
    for i in range (1, police_time):
        for i in range (1, 3):
            turn (LEFT, RED)
            turn (RIGHT, BLUE)
            time.sleep(0.1)
            turn (LEFT, BLUE)
            turn (RIGHT, RED)
            time.sleep(0.1)
        for i in range (1, 5):
            turn (LEFT, RED)
            turn (RIGHT, BLUE)
            time.sleep(0.3)
            turn (LEFT, BLUE)
            turn (RIGHT, RED)
            time.sleep(0.3)
    turn (BOTH, OFF)


# initialization code, intentionally not in a method to encapsulate it within the module and to ensure its execution 
GPIO.setwarnings (True)
GPIO.setmode (GPIO.BOARD)
GPIO.setup (15, GPIO.OUT)   # LEFT_R
GPIO.setup (16, GPIO.OUT)   # LEFT_G
GPIO.setup (18, GPIO.OUT)   # LEFT_B
GPIO.setup (19, GPIO.OUT)   # RIGHT_R
GPIO.setup (21, GPIO.OUT)   # RIGHT_G
GPIO.setup (22, GPIO.OUT)   # RIGHT_B
turn (BOTH, OFF)


if __name__ == '__main__':
    # for stand alone module testing
    setup()
    turn (BOTH, WHITE)
    time.sleep(2)
    turn (RIGHT, RED)
    time.sleep(2)
    turn (LEFT, GREEN)
    time.sleep(2)
    turn (RIGHT, BLUE)
    time.sleep(2)
    turn (LEFT, YELLOW)
    time.sleep(2)
    turn (RIGHT, PINK)
    time.sleep(2)
    turn (LEFT, CYAN)
    time.sleep(2)
    turn (RIGHT, OFF)
    time.sleep(2)
    turn (LEFT, OFF)
    time.sleep(2)
    turn (BOTH, WHITE)
    time.sleep(2)
    turn (BOTH, OFF)
    blinker (LEFT, 5)
    police (4)
    cleanUp()
    
