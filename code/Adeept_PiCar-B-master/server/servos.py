#!/usr/bin/python3
# File name   : servos.py
# Description : By controlling Servos,the camera and Ultrasonic scanner can move Up and down, left and right and
#             ; the steering can move to left and right.
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : wcb
# Date        : 1/24/2019

import sys
sys.path.insert(0, "../common")
import config
import Adafruit_PCA9685
import time
import ultra

# import the settings for servos
# for pitch servo up is larger value
HEAD_PITCH_MIDDLE    = config.importConfigInt('pitch_middle')
HEAD_PITCH_DOWN_MAX  = config.importConfigInt('look_down_max')
HEAD_PITCH_UP_MAX    = config.importConfigInt('look_up_max')

# for yaw servo left is larger value
HEAD_YAW_MIDDLE      = config.importConfigInt('yaw_middle')
HEAD_YAW_RIGHT_MAX   = config.importConfigInt('look_right_max')
HEAD_YAW_LEFT_MAX    = config.importConfigInt('look_left_max')

# for steering servo left is larger value
STEERING_MIDDLE     = config.importConfigInt('turn_middle')
STEERING_RIGHT_MAX  = config.importConfigInt('turn_right_max')
STEERING_LEFT_MAX   = config.importConfigInt('turn_left_max')

SERVO_STEP          = config.importConfigInt('servo_step')

LEFT = SERVO_STEP
RIGHT = -SERVO_STEP
UP = SERVO_STEP
DOWN = -SERVO_STEP

STEERING_SERVO = 2
HEAD_YAW_SERVO = 1
HEAD_PITCH_SERVO = 0

steeringHeading = None
pitchPosition = None
yawPosition = None


def turnSteering(Input):
    steer(steeringHeading + Input)


def steer(position):
    global steeringHeading
    #print("turn_ang: %s" %ang)
    if position < STEERING_RIGHT_MAX:
        position = STEERING_RIGHT_MAX
    elif position > STEERING_LEFT_MAX:
        position = STEERING_LEFT_MAX
    else:
        pass
    pwm.set_pwm(STEERING_SERVO, 0, position)
    steeringHeading = position


def steerFullRight():
    steer(STEERING_RIGHT_MAX)


def steerFullLeft():
    steer(STEERING_LEFT_MAX)


def steerMiddle():
    steer(STEERING_MIDDLE)


def headYaw(position):
    global yawPosition
    if position < HEAD_YAW_RIGHT_MAX:
        position = HEAD_YAW_RIGHT_MAX
    elif position > HEAD_YAW_LEFT_MAX:
        position = HEAD_YAW_LEFT_MAX
    else:
        pass
    pwm.set_pwm(HEAD_YAW_SERVO, 0, position)
    yawPosition = position
    return position


def headPitch(position):
    global pitchPosition
    if position < HEAD_PITCH_DOWN_MAX:
        position = HEAD_PITCH_DOWN_MAX
    elif position > HEAD_PITCH_UP_MAX:
        position = HEAD_PITCH_UP_MAX
    else:
        pass
    pwm.set_pwm(HEAD_PITCH_SERVO, 0, position)
    pitchPosition = position
    return position


def changePitch(Input):
    headPitch(pitchPosition + Input)


def changeYaw(Input):
    headYaw(yawPosition + Input)


def lookAhead():
	headPitch(HEAD_PITCH_MIDDLE)
	headYaw(HEAD_YAW_MIDDLE)


def nodHead():    
    HALF_RANGE = 5
    RATE = .2

    savePitchPosition = pitchPosition
    downPosition = pitchPosition - SERVO_STEP*HALF_RANGE
    upPosition = pitchPosition + SERVO_STEP*HALF_RANGE
    if downPosition < HEAD_PITCH_DOWN_MAX:
        adj = HEAD_PITCH_DOWN_MAX - downPosition
        downPosition += adj
        upPosition += adj
        positions = [upPosition, downPosition, upPosition, downPosition, upPosition, downPosition]
    elif upPosition > HEAD_PITCH_UP_MAX:
        adj = upPosition - HEAD_PITCH_UP_MAX
        downPosition -= adj
        upPosition -= adj
        positions = [downPosition, upPosition, downPosition, upPosition, downPosition, upPosition]
    else:
        positions = [downPosition, upPosition, downPosition, upPosition, downPosition, upPosition]

    for p in positions:
        headPitch(p)
        time.sleep(RATE)
 
    headPitch(savePitchPosition)    


def shakeHead():    
    HALF_RANGE = 5
    RATE = .2

    saveYawPosition = yawPosition
    rightPosition = yawPosition - SERVO_STEP*HALF_RANGE
    leftPosition = yawPosition + SERVO_STEP*HALF_RANGE
    if rightPosition < HEAD_YAW_RIGHT_MAX:
        adj = HEAD_YAW_RIGHT_MAX - rightPosition
        rightPosition += adj
        leftPosition += adj
        positions = [leftPosition, rightPosition, leftPosition, rightPosition, leftPosition, rightPosition]
    elif leftPosition > HEAD_YAW_LEFT_MAX:
        adj = leftPosition - HEAD_YAW_LEFT_MAX
        rightPosition -= adj
        leftPosition -= adj
        positions = [rightPosition, leftPosition, rightPosition, leftPosition, rightPosition, leftPosition]
    else:
        positions = [leftPosition, rightPosition, leftPosition, rightPosition, leftPosition, rightPosition]

    for p in positions:
        headYaw(p)
        time.sleep(RATE)
 
    headYaw(saveYawPosition)    


def scan():                  # Ultrasonic Scanning
    headPitch(HEAD_PITCH_MIDDLE)
    direction = HEAD_YAW_LEFT_MAX           # Value of left-position
    headYaw(direction)
    time.sleep(.75)                         # Wait for the head to be in position
    dis_dir=['list']         # append this so that the client will know it is a scan list
    while direction > HEAD_YAW_RIGHT_MAX:   # Scan from left to right
        new_scan_data = round(ultra.checkDistance(), 2)   # Get a distance of a certern direction
        dis_dir.append(str(new_scan_data))            # Put distance value into list for future transmission 
        direction -= 3           # This value determines the speed of scanning,the greater the faster
        headYaw(direction)
        time.sleep(.005)                                # let servo complete movement to new position
    headYaw(HEAD_YAW_MIDDLE)     # Ultrasonic point forward
    return dis_dir


# initialization code
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(60)
lookAhead()        # call lookAhead() to center head and init position variables
steerMiddle()      # call steerMiddle() to center steering and init heading variable


if __name__ == '__main__':
    time.sleep(2)
    nodHead()
    time.sleep(2)
    headPitch(HEAD_PITCH_DOWN_MAX)
    time.sleep(1)
    nodHead()
    time.sleep(2)
    headPitch(HEAD_PITCH_UP_MAX)
    time.sleep(1)
    nodHead()
    time.sleep(2)
    """
    time.sleep(2)
    shakeHead()
    time.sleep(2)
    headYaw(HEAD_YAW_RIGHT_MAX)
    time.sleep(1)
    shakeHead()
    time.sleep(2)
    headYaw(HEAD_YAW_LEFT_MAX)
    time.sleep(1)
    shakeHead()
    time.sleep(2)
    """
    lookAhead()
    import RPi.GPIO as GPIO
    GPIO.cleanup()             


