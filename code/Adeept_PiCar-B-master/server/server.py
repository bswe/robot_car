#!/usr/bin/python3
# File name   : server.py
# Description : The main program server takes control of Ultrasonic, Motor, Servo by receiving the
#             : order from the client through TCP and carrying out the corresponding operation.
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : wcb
# Date        : 1/24/2019

def timeStamp():
    global t
    startTime = t
    t = time.time()
    print("elapsed time = %s" %str(t - startTime))
    
import time
t = time.time()

import sys
sys.path.insert(0, "../common")

timeStamp()
# import robot specific modules
import config
from comunication import *
import servos
import motor
import ultra
import headlights
import findline
import speech
import sounds
import speak

timeStamp()
# import installed modules
import socket
import threading
import picamera
from picamera.array import PiRGBArray
import cv2
from collections import deque
import numpy as np
import argparse
import rpi_ws281x
import zmq
import base64
import os
import subprocess
import atexit
from pygame import mixer
import RPi.GPIO as GPIO

timeStamp()
distance_stay  = 0.4
distance_range = 2

spd_adj    = 1          #Speed Adjustment

left_spd   = 100         #Speed of the car
right_spd  = 100         #Speed of the car

spd_ad_2 = 1
spd_ad_u = 1

#Status of the car
auto_status = 0
ap_status   = 0
led_status  = 0

NO_TURN       = 0
RIGHT_TURN    = 1
LEFT_TURN     = 2
turn_status   = NO_TURN

opencv_mode   = 0
findline_mode = 0
speech_mode   = 0
auto_mode     = 0

command = ''

dis_data = 0
dis_scan = 1


def get_ram():
    try:
        s = subprocess.check_output(['free','-m'])
        lines = s.split('\n') 
        return ( int(lines[1].split()[1]), int(lines[2].split()[3]) )
    except:
        return 0


def get_temperature():
    try:
        s = subprocess.check_output(['/opt/vc/bin/vcgencmd','measure_temp'])
        return float(s.split('=')[1][:-3])
    except:
        return 0


def get_cpu_speed():
    f = os.popen('/opt/vc/bin/vcgencmd get_config arm_freq')
    cpu = f.read()
    return cpu



def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return rpi_ws281x.rpi_ws281x.Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return rpi_ws281x.rpi_ws281x.Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return rpi_ws281x.rpi_ws281x.Color(0, pos * 3, 255 - pos * 3)


def rainbowCycle(strip, wait_ms = 20, iterations = 5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
    strip.show()
    time.sleep(wait_ms/1000.0)


def theaterChaseRainbow(strip, wait_ms = 50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)


def colorWipe(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(0.005)


def turn_left_led():         #blink the LED on the left
    headlights.blinker(headlights.LEFT, 4)


def turn_right_led():        #blink the LED on the right
    headlights.blinker(headlights.RIGHT, 4)


def opencv_thread():         #OpenCV and FPV video
    hoz_mid_orig = servos.yawPosition
    vtr_mid_orig = servos.pitchPosition
    font = cv2.FONT_HERSHEY_SIMPLEX
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port = True):
        image = frame.array
        cv2.line(image, (300,240), (340,240), (128,255,128),1)
        cv2.line(image, (320,220), (320,260), (128,255,128),1)

        if opencv_mode == 1:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, colorLower, colorUpper)
            mask = cv2.erode(mask, None, iterations = 2)
            mask = cv2.dilate(mask, None, iterations = 2)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            center = None
            if len(cnts) > 0:
                headlights.turn(headlights.BOTH, headlights.GREEN)
                cv2.putText(image, 'Target Detected', (40,60), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
                c = max(cnts, key = cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                X = int(x)
                Y = int(y)
                if radius > 10:
                    cv2.rectangle(image, (int(x-radius), int(y+radius)), (int(x+radius), int(y-radius)), (255,255,255), 1)
                    if X < 310:
                        mu1 = int((320 - X) /3 )
                        hoz_mid_orig += mu1
                        hoz_mid_orig = servos.headYaw(hoz_mid_orig)
                        #print('x=%d'%X)
                    elif X > 330:
                        mu1 = int((X - 330) / 3)
                        hoz_mid_orig -= mu1
                        hoz_mid_orig = servos.headYaw(hoz_mid_orig)
                        #print('x=%d'%X)
                    else:
                        servos.steerMiddle()

                    mu_t = 390 - (servos.STEERING_MIDDLE - hoz_mid_orig)
                    servos.steer(mu_t)

                    dis = dis_data
                    if dis < (distance_stay - 0.1) :
                        headlights.turn(headlights.BOTH, headlights.RED)
                        motor.move(motor.BACKWARD, right_spd*spd_ad_u)
                        cv2.putText(image, 'Too Close', (40,80), font, 0.5, (128,128,255), 1, cv2.LINE_AA)
                    elif dis > (distance_stay + 0.1):
                        motor.move(motor.FORWARD, right_spd*spd_ad_2)
                        cv2.putText(image, 'OpenCV Tracking', (40,80), font, 0.5, (128,255,128), 1, cv2.LINE_AA)
                    else:
                        motor.motorStop()
                        headlights.turn(headlights.BOTH, headlights.BLUE)
                        cv2.putText(image, 'In Position', (40,80), font, 0.5, (255,128,128), 1, cv2.LINE_AA)

                    if dis < 8:
                        cv2.putText(image, '%s m'%str(round(dis,2)), (40,40), font, 0.5, (255,255,255), 1, cv2.LINE_AA)

                    if Y < 230:
                        mu2 = int((240 - Y) / 5)
                        vtr_mid_orig += mu2
                        vtr_mid_orig = servos.headPitch(vtr_mid_orig)
                    elif Y > 250:
                        mu2 = int((Y - 240) / 5)
                        svtr_mid_orig = servos.headPitch(vtr_mid_orig)
                    
                    if X > 280:
                        if X < 350:
                            cv2.line(image, (300,240), (340,240), (64,64,255), 1)
                            cv2.line(image, (320,220), (320,260), (64,64,255), 1)
                            cv2.rectangle(image, (int(x-radius), int(y+radius)), (int(x+radius), int(y-radius)), (64, 64, 255), 1)
            else:
                headlights.turn(headlights.BOTH, headlights.YELLOW)
                cv2.putText(image, 'Target Detecting', (40,60), font, 0.5, (255,255,255), 1, cv2.LINE_AA)
                led_y = 1
                motor.motorStop()

            for i in range(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                cv2.line(image, pts[i - 1], pts[i], (0, 0, 255), thickness)
        else:
            dis = dis_data
            if dis < 8:
                cv2.putText(image, '%s m'%str(round(dis,2)), (40,40), font, 0.5, (255,255,255), 1, cv2.LINE_AA)

        encoded, buffer = cv2.imencode('.jpg', image)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)
        rawCapture.truncate(0)


def ws2812_thread():         #WS_2812 strip leds
    while 1:
        if 'forward' in command:
            rainbowCycle(ledStrip,1 ,1)
        elif 'backward' in command:
            colorWipe(ledStrip, rpi_ws281x.Color(255,0,0))
        elif turn_status == NO_TURN:
            ledStrip.setPixelColor(0, rpi_ws281x.Color(0,0,0))
            ledStrip.setPixelColor(1, rpi_ws281x.Color(0,0,0))
            ledStrip.setPixelColor(2, rpi_ws281x.Color(0,0,0))
            ledStrip.setPixelColor(3, rpi_ws281x.Color(0,0,0))
            ledStrip.setPixelColor(4, rpi_ws281x.Color(0,0,0))
            ledStrip.setPixelColor(5, rpi_ws281x.Color(0,0,0))
            ledStrip.show()
        elif turn_status == LEFT_TURN:
            ledStrip.setPixelColor(0, rpi_ws281x.Color(255,255,0))
            ledStrip.setPixelColor(1, rpi_ws281x.Color(255,255,0))
            ledStrip.setPixelColor(2, rpi_ws281x.Color(255,255,0))
            ledStrip.setPixelColor(3, rpi_ws281x.Color(0,0,0))
            ledStrip.setPixelColor(4, rpi_ws281x.Color(0,0,0))
            ledStrip.setPixelColor(5, rpi_ws281x.Color(0,0,0))
            ledStrip.show()
        elif turn_status == RIGHT_TURN:
            ledStrip.setPixelColor(0, rpi_ws281x.Color(0,0,0))
            ledStrip.setPixelColor(1, rpi_ws281x.Color(0,0,0))
            ledStrip.setPixelColor(2, rpi_ws281x.Color(0,0,0))
            ledStrip.setPixelColor(3, rpi_ws281x.Color(255,255,0))
            ledStrip.setPixelColor(4, rpi_ws281x.Color(255,255,0))
            ledStrip.setPixelColor(5, rpi_ws281x.Color(255,255,0))
            ledStrip.show()
        else:
            pass
        time.sleep(0.1)


def findline_thread():       #Line tracking mode
    while 1:
        while findline_mode:
            findline.run()
        time.sleep(0.2)


def speech_thread():         #Speech recognition mode
    while 1:
        while speech_mode:
            speech.run()
        time.sleep(0.2)


def auto_thread():           #Ultrasonic tracking mode
    while 1:
        while auto_mode:
            ultra.loop(distance_stay, distance_range)
        time.sleep(0.2)


def dis_scan_thread():       #Get Ultrasonic scan distance
    global dis_data
    while 1:
        while  dis_scan:
            dis_data = ultra.checkDistance()
            time.sleep(0.2)
        time.sleep(0.2)


def ap_thread():             #Set up an AP-Hotspot
    # why is this a thread???? It simply calls os.system and returns
    os.system("sudo create_ap wlan0 eth0 AdeeptCar 12345678")


blinkThreadStatus = 0
BLINK_THREAD_RUNNING = 1
BLINK_THREAD_STOP = 2
BLINK_THREAD_STOPPED = 3

def blinkHeadlightsThread():
    global blinkThreadStatus

    blinkThreadStatus = BLINK_THREAD_RUNNING
    headlights.turn(headlights.BOTH, headlights.OFF)
    while blinkThreadStatus != BLINK_THREAD_STOP:
        headlights.turn(headlights.LEFT, headlights.RED)
        for i in range(10):
            time.sleep(.1)
            if blinkThreadStatus == BLINK_THREAD_STOP:
                blinkThreadStatus = BLINK_THREAD_STOPPED
                return
        headlights.turn(headlights.LEFT, headlights.OFF)
        headlights.turn(headlights.RIGHT, headlights.RED)
        for i in range(10):
            time.sleep(.1)
            if blinkThreadStatus == BLINK_THREAD_STOP:
                blinkThreadStatus = BLINK_THREAD_STOPPED
                return
        headlights.turn(headlights.RIGHT, headlights.OFF)
    blinkThreadStatus = BLINK_THREAD_STOPPED


def connect():
    global ap_status, blinkThreadStatus

    #Start server, and wait for client
    HOST = ''
    PORT = 10223                              #Define port serial 
    ADDR = (HOST, PORT)
    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)                      

    # setup server to accept client connection
    while True:              
        try:
            s =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("1.1.1.1",80))
            ipaddr_check = s.getsockname()[0]
            s.close()
            print("connect: robot's IP address = %s" %str(ipaddr_check))
            wifi_status = 1
        except:
            if ap_status == 0:
                ap_threading = threading.Thread(target = ap_thread)   #Define a thread for wifi hot spot
                ap_threading.setDaemon(True)                      #True means it is a front thread, closes when the mainloop() closes
                ap_threading.start()                                  #Thread starts
                headlights.turn(headlights.BOTH, headlights.YELLOW)
                time.sleep(5)
                wifi_status = 0
            
        if wifi_status == 1:
            # blink headlights to indicate SW is running and waiting for client
            ledBlinkThread = threading.Thread(target = blinkHeadlightsThread)      
            ledBlinkThread.setDaemon(True)                             
            ledBlinkThread.start()                                     #Thread starts
            print('waiting for connection...')
            Socket, addr = tcpSerSock.accept()       #Determine whether to connect
            while blinkThreadStatus != BLINK_THREAD_STOPPED:
                blinkThreadStatus = BLINK_THREAD_STOP
                time.sleep(.1)
            headlights.turn(headlights.BOTH, headlights.GREEN)
            print('...connected from :', addr)
            return Socket, addr
        else:
            headlights.turn(headlights.BOTH, headlights.BLUE)
            print('waiting for connection...')
            Socket, addr = tcpSerSock.accept()       #Determine whether to connect
            headlights.turn(headlights.BOTH, headlights.GREEN)
            print('...connected from :', addr)
            ap_status = 1
            return Socket, addr

    
def startThreads():
    video_threading = threading.Thread(target = opencv_thread)      #Define a thread for FPV and OpenCV
    video_threading.setDaemon(True)                             #'True' means it is a front thread, closes when the mainloop() closes
    video_threading.start()                                     #Thread starts

    ws2812_threading = threading.Thread(target = ws2812_thread)     #Define a thread for ws_2812 leds
    ws2812_threading.setDaemon(True)                            #'True' means it is a front thread, closes when the mainloop() closes
    ws2812_threading.start()                                    #Thread starts

    findline_threading = threading.Thread(target = findline_thread) #Define a thread for line tracking
    findline_threading.setDaemon(True)                          #'True' means it is a front thread, closes when the mainloop() closes
    findline_threading.start()                                  #Thread starts

    speech_threading = threading.Thread(target = speech_thread)     #Define a thread for speech recognition
    speech_threading.setDaemon(True)                            #'True' means it is a front thread, closes when the mainloop() closes
    speech_threading.start()                                    #Thread starts

    auto_threading = threading.Thread(target = auto_thread)         #Define a thread for ultrasonic tracking
    auto_threading.setDaemon(True)                              #'True' means it is a front thread, closes when the mainloop() closes
    auto_threading.start()                                      #Thread starts

    scan_threading = threading.Thread(target = dis_scan_thread)     #Define a thread for ultrasonic scan
    scan_threading.setDaemon(True)                              #'True' means it is a front thread, closes when the mainloop() closes
    scan_threading.start()                                      #Thread starts
    

def setup(clientSocket, clientIpAddress):                 #initialization
    global footage_socket
    
    clientSocket.send(('SET %s' %servos.HEAD_PITCH_MIDDLE + ' %s' %servos.HEAD_PITCH_UP_MAX + ' %s' %servos.HEAD_PITCH_DOWN_MAX + \
                       ' %s' %servos.HEAD_YAW_MIDDLE + ' %s' %servos.HEAD_YAW_LEFT_MAX + ' %s' %servos.HEAD_YAW_RIGHT_MAX + \
                       ' %s' %servos.STEERING_MIDDLE + ' %s' %servos.STEERING_LEFT_MAX + ' %s' %servos.STEERING_RIGHT_MAX + \
                       ' %s' %left_spd + ' %s' %right_spd).encode())
    print('setup: sending SET %s' %servos.HEAD_PITCH_MIDDLE + ' %s' %servos.HEAD_PITCH_UP_MAX + ' %s' %servos.HEAD_PITCH_DOWN_MAX + \
                       ' %s' %servos.HEAD_YAW_MIDDLE + ' %s' %servos.HEAD_YAW_LEFT_MAX + ' %s' %servos.HEAD_YAW_RIGHT_MAX + \
                       ' %s' %servos.STEERING_MIDDLE + ' %s' %servos.STEERING_LEFT_MAX + ' %s' %servos.STEERING_RIGHT_MAX + \
                       ' %s' %left_spd + ' %s' %right_spd)

    #FPV initialization
    context = zmq.Context()
    footage_socket = context.socket(zmq.PUB)
    footage_socket.connect('tcp://%s:5555'%clientIpAddress[0])

    startThreads()
    

def mainLoop(socket):                   
    global led_status, auto_status, opencv_mode, findline_mode, speech_mode, \
           auto_mode, command, ap_status, turn_status, blinkThreadStatus
    
    BUFSIZ = 1024                             #Define buffer size

    while True: 
        command = socket.recv(BUFSIZ).decode()
        print("mainLoop: received %s" %command)
    
        if not command:
            continue

        # strip end-of-cmd off
        if END_OF_CMD in command:
            command = command[:-len(END_OF_CMD)]
        # TODO: add code to handle receiving multiple commands delimited by end-of-cmd
    
        if SOUND in command:
            sounds.playSound(command[len(SOUND):])

        elif SPEAK in command:
            speak.say(command[len(SPEAK):])

        elif VOLUME in command:
            speak.changeVolume(command[len(VOLUME):])

        elif RATE in command:
            speak.changeRate(command[len(RATE):])

        elif SHAKE in command:
            servos.shakeHead()

        elif NOD in command:
            servos.nodHead()

        elif 'exit' in command:
            os.system("sudo shutdown -h now\n")

        elif 'quit' in command:
            print('shutting down')
            return

        elif 'spdset' in command:
            global spd_adj
            spd_adj = float((str(command))[7:])      #Speed Adjustment
            print("speed adjustment set to %s" %str(spd_adj))

        elif 'scan' in command:
            dis_can = servos.scan()              # Start Scanning
            str_list_1 = dis_can                 # Divide the list to make it samller to send 
            str_index = ' '                      # Separate the values by space
            str_send_1 = str_index.join(str_list_1)+' '
            socket.sendall((str(str_send_1)).encode())   # Send Data
            socket.send('finished'.encode())        # Sending 'finished' tell the client to stop receiving the list of dis_can

        elif 'EC1set' in command:                 # pitch Adjustment
            newValue = int((str(command))[7:])
            config.exportConfig('pitch_middle', newValue)
            servos.HEAD_PITCH_MIDDLE = newValue
            servos.headPitch(newValue)

        elif 'LDMset' in command:                 # look down max Adjustment
            newValue = int((str(command))[7:])
            config.exportConfig('look_down_max', newValue)
            servos.HEAD_PITCH_DOWN_MAX = newValue
            servos.headPitch(newValue)

        elif 'LUMset' in command:                 # look up max Adjustment
            newValue = int((str(command))[7:])
            config.exportConfig('look_up_max', newValue)
            servos.HEAD_PITCH_UP_MAX = newValue
            servos.headPitch(newValue)

        elif 'EC2set' in command:                 # yaw Adjustment
            newValue = int((str(command))[7:])
            config.exportConfig('yaw_middle', newValue)
            servos.HEAD_YAW_MIDDLE = newValue
            servos.headYaw(newValue)

        elif 'LLMset' in command:                 # look left max Adjustment
            newValue = int((str(command))[7:])
            config.exportConfig('look_left_max', newValue)
            servos.HEAD_YAW_LEFT_MAX = newValue
            servos.headYaw(newValue)

        elif 'LRMset' in command:                 # look right max Adjustment
            newValue = int((str(command))[7:])
            config.exportConfig('look_right_max', newValue)
            servos.HEAD_YAW_RIGHT_MAX = newValue
            servos.headYaw(newValue)

        elif 'STEERINGset' in command:            #Motor Steering center Adjustment
            newValue = int((str(command))[12:])
            config.exportConfig('turn_middle', newValue)
            servos.STEERING_MIDDLE = newValue
            servos.steerMiddle()

        elif 'SLMset' in command:                 # Steering left max Adjustment
            newValue = int((str(command))[7:])
            config.exportConfig('turn_left_max', newValue)
            servos.STEERING_LEFT_MAX = newValue
            servos.steerFullLeft()

        elif 'SRMset' in command:                 # Steering right max Adjustment
            newValue = int((str(command))[7:])
            config.exportConfig('turn_right_max', newValue)
            servos.STEERING_RIGHT_MAX = newValue
            servos.steerFullRight()

        elif 'EM1set' in command:                 #Motor A Speed Adjustment
            newValue = int((str(command))[7:])
            config.exportConfig('E_M1', newValue)

        elif 'EM2set' in command:                 #Motor B Speed Adjustment
            newValue = int((str(command))[7:])
            config.exportConfig('E_M2', newValue)

        elif 'stop' in command:                   #When server receive "stop" from client,car stops moving
            socket.send('9'.encode())
            motor.motorStop()
            #setup()
            if led_status == 0:
                headlights.turn(headlights.BOTH, headlights.OFF)
            colorWipe(ledStrip, rpi_ws281x.Color(0,0,0))
        
        elif 'lightsON' in command:               #Turn on the LEDs
            headlights.turn(headlights.BOTH, headlights.WHITE)
            led_status = 1
            socket.send('lightsON'.encode())

        elif 'lightsOFF'in command:               #Turn off the LEDs
            headlights.turn(headlights.BOTH, headlights.OFF)
            led_status = 0
            socket.send('lightsOFF'.encode())

        elif 'SteerLeft' in command:              #Turn more to the left
            headlights.turn(headlights.RIGHT, headlights.OFF)
            headlights.turn(headlights.LEFT, headlights.YELLOW)
            servos.turnSteering(servos.LEFT)
            turn_status = LEFT_TURN

        elif 'SteerRight' in command:              #Turn more to the Right
            headlights.turn(headlights.LEFT, headlights.OFF)
            headlights.turn(headlights.RIGHT, headlights.YELLOW)
            servos.turnSteering(servos.RIGHT)
            turn_status = RIGHT_TURN

        elif 'middle' in command:                 #Go straight
            headlights.turn(headlights.BOTH, headlights.BLUE)
            turn_status = NO_TURN
            servos.steerMiddle()
        
        elif 'Left' in command:                   #Turn hard left
            headlights.turn(headlights.RIGHT, headlights.OFF)
            headlights.turn(headlights.LEFT, headlights.YELLOW)
            servos.steerFullLeft()
            turn_status = LEFT_TURN
            socket.send('3'.encode())
        
        elif 'Right' in command:                  #Turn hard right
            headlights.turn(headlights.LEFT, headlights.OFF)
            headlights.turn(headlights.RIGHT, headlights.YELLOW)
            servos.steerFullRight()
            turn_status = RIGHT_TURN
            socket.send('4'.encode())
        
        elif 'backward' in command:               #When server receive "backward" from client,car moves backward
            socket.send('2'.encode())
            motor.move(motor.BACKWARD, right_spd*spd_adj)

        elif 'forward' in command:                #When server receive "forward" from client,car moves forward
            socket.send('1'.encode())
            motor.move(motor.FORWARD, right_spd*spd_adj)

        elif 'l_up' in command:                   #Camera look up
            servos.changePitch(servos.UP)
            socket.send('5'.encode())

        elif 'l_do' in command:                   #Camera look down
            servos.changePitch(servos.DOWN)
            socket.send('6'.encode())

        elif 'l_le' in command:                   #Camera look left
            servos.changeYaw(servos.LEFT)
            socket.send('7'.encode())

        elif 'l_ri' in command:                   #Camera look right
            servos.changeYaw(servos.RIGHT)
            socket.send('8'.encode())

        elif 'ahead' in command:                  #Camera look ahead
            servos.lookAhead()

        elif 'Off' in command:                   #When server receive "Off" from client, Auto Mode switches off
            opencv_mode   = 0
            findline_mode = 0
            speech_mode   = 0
            auto_mode     = 0
            auto_status   = 0
            time.sleep(.3)       # wait for threads to detect the off state
            dis_scan = 1
            socket.send('auto_status_off'.encode())
            motor.motorStop()
            headlights.turn(headlights.BOTH, headlights.OFF)
            servos.steerMiddle()
            turn_status = NO_TURN
        
        elif 'auto' in command:                   #When server receive "auto" from client,start Auto Mode
            if auto_status == 0:
                socket.send('0'.encode())
                auto_status = 1
                auto_mode = 1
                dis_scan = 0

        elif 'opencv' in command:                 #When server receive "auto" from client,start Auto Mode
            if auto_status == 0:
                auto_status = 1
                opencv_mode = 1                  
                socket.send('oncvon'.encode())

        elif 'findline' in command:               #Find line mode start
            if auto_status == 0:
                socket.send('findline'.encode())
                auto_status = 1
                findline_mode = 1

        elif 'voice_3' in command:                #Speech recognition mode start
            if auto_status == 0:
                auto_status = 1
                speech_mode = 1
                socket.send('voice_3'.encode())


def cleanup():
    print("server module: executing cleanup()")
    colorWipe(ledStrip, rpi_ws281x.Color(0,0,0))
    headlights.turn(headlights.BOTH, headlights.OFF)
    GPIO.cleanup()             
    try:
        camera.close()
    except:
        print("cleanup: caught known false picamera exception that it is ignoring")
        pass      # ignore known random exception in picamera library
    print("cleanup: completed")


if __name__ == '__main__':
    timeStamp()
    print("robot server starting...")

    #atexit.register(cleanup)
    
    # LED strip configuration:
    LED_COUNT      = 12      # Number of LED pixels.
    LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    # Create NeoPixel object with appropriate configuration.
    ledStrip = rpi_ws281x.Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    ledStrip.begin()
    
    camera = picamera.PiCamera()              #Camera initialization
    camera.resolution = (640, 480)
    camera.framerate = 7
    rawCapture = PiRGBArray(camera, size=(640, 480))

    colorLower = (24, 100, 100)               #The color that openCV find
    colorUpper = (44, 255, 255)               #USE HSV value NOT RGB

    ap = argparse.ArgumentParser()            #OpenCV initialization
    ap.add_argument("-b", "--buffer", type = int, default = 64, help="max buffer size")
    args = vars(ap.parse_args())
    pts = deque(maxlen = args["buffer"])
    time.sleep(0.1)

    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
       
    speak.say("Roby ready")

    try:
       clientSocket, clientIpAddress = connect()
    except KeyboardInterrupt:
        print("keyboard interrupt...")
        clientSocket = None
        #cleanup()
        
    if clientSocket != None:
        setup(clientSocket, clientIpAddress)
        
        try:
            mainLoop(clientSocket)
        except KeyboardInterrupt:
            print("keyboard interrupt...")
            if ap_status == 1:
                os.system("sudo shutdown -h now\n")
                time.sleep(5)
    cleanup()
    print("robot server stopping...")
