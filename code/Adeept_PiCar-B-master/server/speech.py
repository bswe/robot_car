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
import led
import RPi.GPIO as GPIO

status     = 1          #Motor rotation
forward    = 1          #Motor forward
backward   = 0          #Motor backward

left_spd   = config.importConfigInt('E_M1')         #Speed of the car
right_spd  = config.importConfigInt('E_M2')         #Speed of the car
left       = config.importConfigInt('E_T1')         #Motor Left
right      = config.importConfigInt('E_T2')         #Motor Right

left_R = 15
left_G = 16
left_B = 18

right_R = 19
right_G = 21
right_B = 22

on  = GPIO.LOW
off = GPIO.HIGH

spd_ad_1 = 1
spd_ad_2 = 1

v_command=''

def setup():
    GPIO.setwarnings(False)
    try:
        motor.setup()
    except:
        pass


def run():
    global v_command
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone(device_index =2,sample_rate=48000) as source:
        r.record(source,duration=2)
        #r.adjust_for_ambient_noise(source)
        led.both_off()
        led.yellow()
        print("Command?")
        audio = r.listen(source)
        led.both_off()
        led.blue()

    try:
        v_command = r.recognize_sphinx(audio,
        keyword_entries=[('forward',1.0),('backward',1.0),
        ('left',1.0),('right',1.0),('stop',1.0)])        #You can add your own command here
        print(v_command)
        led.both_off()
        led.cyan()
    except sr.UnknownValueError:
        print("say again")
        led.both_off()
        led.red()
    except sr.RequestError as e:
        led.both_off()
        led.red()
        pass

    #print('pre')

    if 'forward' in v_command:
        motor.motorLeft(status, forward,left_spd*spd_ad_2)
        motor.motorRight(status,backward,right_spd*spd_ad_2)
        time.sleep(2)
        motor.motorStop()

    elif 'backward' in v_command:
        motor.motorLeft(status, backward,left_spd)
        motor.motorRight(status,forward,right_spd)
        time.sleep(2)
        motor.motorStop()

    elif 'left' in v_command:
        servos.left()
        motor.motorLeft(status, forward,left_spd*spd_ad_2)
        motor.motorRight(status,backward,right_spd*spd_ad_2)
        time.sleep(2)
        motor.motorStop()

    elif "right" in v_command:
        servos.right()
        motor.motorLeft(status, forward,left_spd*spd_ad_2)
        motor.motorRight(status,backward,right_spd*spd_ad_2)
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
