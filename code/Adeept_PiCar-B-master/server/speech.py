#!/usr/bin/python3
# File name   : speech.py
# Description : Speech Recognition 
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : William & Authors from https://github.com/Uberi/speech_recognition#readme
# Date        : 2018/10/12

import sys
sys.path.insert(0, "../common")
import config
import speech_recognition as sr
import motor
import servos, time
import headlights
import RPi.GPIO as GPIO

left_spd   = config.importConfigInt('E_M1')         #Speed of the car
right_spd  = config.importConfigInt('E_M2')         #Speed of the car
left       = config.importConfigInt('E_T1')         #Motor Left
right      = config.importConfigInt('E_T2')         #Motor Right

spd_ad_1 = 1
spd_ad_2 = 1


def setup():
    GPIO.setwarnings(True)
    try:
        motor.setup()
    except:
        pass


def run():
    v_command
    
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(device_index =2,sample_rate=48000) as source:
        r.record(source,duration=2)
        #r.adjust_for_ambient_noise(source)
        headlights.turn(headlights.BOTH, headlights.YELLOW)
        print("Command?")
        audio = r.listen(source)
        headlights.turn(headlights.BOTH, headlights.BLUE)

    try:
        v_command = r.recognize_sphinx(audio,
        keyword_entries=[('forward',1.0),('backward',1.0),
        ('left',1.0),('right',1.0),('stop',1.0)])        #You can add your own command here
        print(v_command)
        headlights.turn(headlights.BOTH, headlights.CYAN)
    except sr.UnknownValueError:
        print("say again")
        headlights.turn(headlights.BOTH, headlights.RED)
    except sr.RequestError as e:
        headlights.turn(headlights.BOTH, headlights.RED)
        pass

    #print('pre')

    if 'forward' in v_command:
        motor.motorLeft(motor.FORWARD, left_spd*spd_ad_2)
        motor.motorRight(motor.BACKWARD, right_spd*spd_ad_2)
        time.sleep(2)
        motor.motorStop()

    elif 'backward' in v_command:
        motor.motorLeft(motor.BACKWARD, left_spd)
        motor.motorRight(motor.FORWARD, right_spd)
        time.sleep(2)
        motor.motorStop()

    elif 'left' in v_command:
        servos.left()
        motor.motorLeft(motor.FORWARD, left_spd*spd_ad_2)
        motor.motorRight(motor.BACKWARD, right_spd*spd_ad_2)
        time.sleep(2)
        motor.motorStop()

    elif "right" in v_command:
        servos.right()
        motor.motorLeft(motor.FORWARD, left_spd*spd_ad_2)
        motor.motorRight(motor.BACKWARD, right_spd*spd_ad_2)
        time.sleep(2)
        motor.motorStop()

    elif 'stop' in v_command:
        motor.motorStop()

    else:
        pass


try:
    pass
except KeyboardInterrupt:
    motor.motorStop()
