#!/usr/bin/python3
# File name   : motor.py
# Description : Control Motors 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William
# Date        : 2018/10/12

import RPi.GPIO as GPIO
import time
import atexit

# MOTOR_EN_A: Pin7  |  MOTOR_EN_B: Pin11
# MOTOR_A:  Pin8,Pin10    |  MOTOR_B: Pin13,Pin12

MOTOR_A_EN   = 7
MOTOR_B_EN   = 11
MOTOR_A_PIN1 = 8
MOTOR_A_PIN2 = 10
MOTOR_B_PIN1 = 13
MOTOR_B_PIN2 = 12

FORWARD  = 0
BACKWARD = 1

pwm_A = None
pwm_B = None


def motorStop():      
    pwm_A.stop()
    pwm_B.stop()


def move(direction, speed):         # motor control for PiCar-B that has just one motor
    motorA(direction, speed)
    if direction == FORWARD:
        motorB(BACKWARD, speed)
    else:
        motorB(FORWARD, speed)


def motorB(direction, speed):   #Motor B positive and negative rotation
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


def motorA(direction, speed):   #Motor A positive and negative rotation
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


# initialization code, intentionally not in a method to encapsulate it within the module and to ensure its execution 
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(MOTOR_A_EN, GPIO.OUT)
GPIO.setup(MOTOR_B_EN, GPIO.OUT)
GPIO.setup(MOTOR_A_PIN1, GPIO.OUT)
GPIO.setup(MOTOR_A_PIN2, GPIO.OUT)
GPIO.setup(MOTOR_B_PIN1, GPIO.OUT)
GPIO.setup(MOTOR_B_PIN2, GPIO.OUT)
try:
    pwm_A = GPIO.PWM(MOTOR_A_EN, 100)
    pwm_B = GPIO.PWM(MOTOR_B_EN, 100)
except Exception as e:
    print(e)
