#!/usr/bin/python3
# File name   : motor.py
# Description : Control Motors 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12

import RPi.GPIO as GPIO
import time

# MOTOR_EN_A: Pin7  |  MOTOR_EN_B: Pin11
# MOTOR_A:  Pin8,Pin10    |  MOTOR_B: Pin13,Pin12

MOTOR_A_EN   = 7
MOTOR_B_EN   = 11
MOTOR_A_PIN1 = 8
MOTOR_A_PIN2 = 10
MOTOR_B_PIN1 = 13
MOTOR_B_PIN2 = 12

FORWARD = 0
BACKWARD = 1
STOP = 0

pwm_A = 0
pwm_B = 0


def setup():   #Motor initialization
    global pwm_A, pwm_B
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOTOR_A_EN, GPIO.OUT)
    GPIO.setup(MOTOR_B_EN, GPIO.OUT)
    GPIO.setup(MOTOR_A_PIN1, GPIO.OUT)
    GPIO.setup(MOTOR_A_PIN2, GPIO.OUT)
    GPIO.setup(MOTOR_B_PIN1, GPIO.OUT)
    GPIO.setup(MOTOR_B_PIN2, GPIO.OUT)
    try:
        pwm_A = GPIO.PWM(MOTOR_A_EN, 1000)
        pwm_B = GPIO.PWM(MOTOR_B_EN, 1000)
    except:
        pass


def motorStop():#Motor stops
    GPIO.output(MOTOR_A_PIN1, GPIO.LOW)
    GPIO.output(MOTOR_A_PIN2, GPIO.LOW)
    GPIO.output(MOTOR_B_PIN1, GPIO.LOW)
    GPIO.output(MOTOR_B_PIN2, GPIO.LOW)
    GPIO.output(MOTOR_A_EN, GPIO.LOW)
    GPIO.output(MOTOR_B_EN, GPIO.LOW)


def motorRight(status, direction, speed):   #Motor 2 positive and negative rotation
    if status == STOP: 
        motorStop()
    else:
        if direction == FORWARD:
            GPIO.output(MOTOR_B_PIN1, GPIO.HIGH)
            GPIO.output(MOTOR_B_PIN2, GPIO.LOW)
            pwm_B.start(100)
            pwm_B.ChangeDutyCycle(speed)
        elif direction == BACKWARD:
            GPIO.output(MOTOR_B_PIN1, GPIO.LOW)
            GPIO.output(MOTOR_B_PIN2, GPIO.HIGH)
            pwm_B.start(0)
            pwm_B.ChangeDutyCycle(speed)


def motorLeft(status, direction, speed):   #Motor 1 positive and negative rotation
    if status == STOP: 
        motorStop()
    else:
        if direction == FORWARD:
            GPIO.output(MOTOR_A_PIN1, GPIO.HIGH)
            GPIO.output(MOTOR_A_PIN2, GPIO.LOW)
            pwm_A.start(100)
            pwm_A.ChangeDutyCycle(speed)
        elif direction == BACKWARD:
            GPIO.output(MOTOR_A_PIN1, GPIO.LOW)
            GPIO.output(MOTOR_A_PIN2, GPIO.HIGH)
            pwm_A.start(0)
            pwm_A.ChangeDutyCycle(speed)
    return direction


def destroy():
    motorStop()
    GPIO.cleanup()             # Release resource

# not sure what this was for, so I commented it out
#try:
#    pass
#except KeyboardInterrupt:
#    destroy()


