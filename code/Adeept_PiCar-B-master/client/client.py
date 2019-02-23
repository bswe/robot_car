#!/usr/bin/python
# -*- coding: UTF-8 -*-
# File name   : client.py
# Description : PiCar client  
# Website     : www.adeept.com
# E-mail      : support@adeept.com
# Author      : wcb
# Date        : 1/24/2019

import sys
sys.path.insert(0, "../common")
import config
import socket 
import sys,subprocess
import time
import threading as thread
import tkinter as tk
import math
import speech_recognition as sr
import cv2
import zmq
import base64
import numpy as np
#from tkinter import font


# constants
BUFFER_SIZE      = 1024     
BACKGROUND_COLOR = '#000000'        
TEXT_COLOR       = '#E1F5FE'      
BUTTON_COLOR     = '#212121'       
LINE_COLOR       = '#01579B'      
CANVAS_COLOR     = '#212121'       
OVAL_COLOR       = '#2196F3'      
TARGET_COLOR     = '#FF6D00'
SERVER_PORT      = 10223        #Define port serial 

# global variables
window = tk.Tk()
tcpClicSock = None  #for robot server socket connection

ip_entry = None
labelSpeedStatus = None
labelConnectionStatus = None
labelIpAddress = None
buttonFollow = None
buttonConnect = None
BtnFL = None
buttonHeadlights = None
BtnOCV = None
BtnSR3 = None
labelStatus = None
BtnIP = None
E_C1 = None
E_C2= None
E_M1 = None
E_M2 = None
E_T1 = None
E_T2 = None
var_x_scan = None
var_spd = None
l_VIN = None
BtnVIN = None
Steering = None

led_status      = 0
opencv_status   = 0
auto_status     = 0
speech_status   = 0
findline_status = 0


def processList(code_car):
    dis_list = []
    f_list = []
    list_str = code_car.decode()
    
    while  True:                    #Save scan result in dis_list
        code_car = tcpClicSock.recv(BUFFER_SIZE)
        if 'finished' in str(code_car):
            break
        list_str += code_car.decode()
        labelStatus.config(text='Scanning')
    
    dis_list = list_str.split()       #Save the data as a list
    labelStatus.config(text='Finished')
    
    for i in range (0, len(dis_list)):   #Translate the String-type value in the list to Float-type
        try:
            new_f = float(dis_list[i])
            f_list.append(new_f)
        except:
            continue
    
    dis_list = f_list
    #can_scan.delete(line)
    #can_scan.delete(point_scan)
    # define a canvas
    can_scan_1 = tk.Canvas(window, bg=CANVAS_COLOR, height=250, width=320, highlightthickness=0) 
    can_scan_1.place(x=440,y=330) #Place the canvas
    line = can_scan_1.create_line(0, 62, 320, 62, fill='darkgray')   #Draw a line on canvas
    line = can_scan_1.create_line(0, 124, 320, 124, fill='darkgray') #Draw a line on canvas
    line = can_scan_1.create_line(0, 186, 320, 186, fill='darkgray') #Draw a line on canvas
    line = can_scan_1.create_line(160, 0, 160, 250, fill='darkgray') #Draw a line on canvas
    line = can_scan_1.create_line(80, 0, 80, 250, fill='darkgray')   #Draw a line on canvas
    line = can_scan_1.create_line(240, 0, 240, 250, fill='darkgray') #Draw a line on canvas

    x_range = var_x_scan.get()          #Get the value of scan range from IntVar

    for i in range (0, len(dis_list)):   #Scale the result to the size as canvas
        try:
            len_dis_1 = int((dis_list[i]/x_range)*250)                   #600 is the height of canvas
            pos       = int((i/len(dis_list))*320)                       #740 is the width of canvas
            pos_ra    = int(((i/len(dis_list))*140)+20)                  #Scale the direction range to (20-160)
            len_dis   = int(len_dis_1*(math.sin(math.radians(pos_ra))))  #len_dis is the height of the line

            x0_l, y0_l, x1_l, y1_l = pos, (250-len_dis), pos, (250-len_dis)       #The position of line
            x0, y0, x1, y1 = (pos+3), (250-len_dis+3), (pos-3), (250-len_dis-3)   #The position of arc

            if pos <= 160:                                                      #Scale the whole picture to a shape of sector
                pos = 160-abs(int(len_dis_1*(math.cos(math.radians(pos_ra)))))
                x1_l = (x1_l-math.cos(math.radians(pos_ra))*130)
            else:
                pos = abs(int(len_dis_1*(math.cos(math.radians(pos_ra)))))+160
                x1_l = x1_l+abs(math.cos(math.radians(pos_ra))*130)

            y1_l = y1_l-abs(math.sin(math.radians(pos_ra))*130)              #Orientation of line

            line = can_scan_1.create_line(pos, y0_l, x1_l, y1_l, fill=LINE_COLOR)   #Draw a line on canvas
            #Draw a arc on canvas
            point_scan = can_scan_1.create_oval((pos+3), y0, (pos-3), y1, fill=OVAL_COLOR, outline=OVAL_COLOR) 
        except:
            pass
    can_tex_11 = can_scan_1.create_text((27,178), text='%sm'%round((x_range/4),2), fill='#aeea00')     #Create a text on canvas
    can_tex_12 = can_scan_1.create_text((27,116), text='%sm'%round((x_range/2),2), fill='#aeea00')     #Create a text on canvas
    can_tex_13 = can_scan_1.create_text((27,54), text='%sm'%round((x_range*0.75),2), fill='#aeea00')   #Create a text on canvas


def receiveThread():     # Thread for receiving and processing data from server
    global led_status, findline_status, auto_status, opencv_status, speech_status
    
    while True:
        try:
            code_car = tcpClicSock.recv(BUFFER_SIZE) #Listening,and save the data in 'code_car'
        except Exception:
            print ("got socket exception in code _receive thread, will terminate thread")
            exit()
        if not code_car:
            continue
        labelStatus.config(text=code_car)          #Put the data on the label
        print("recvd from robot: " + str(code_car))

        if 'SET' in str(code_car):
            set_list=code_car.decode()
            set_list=set_list.split()
            s1,s2,s3,s4,s5,s6,s7=set_list[1:]
            E_C1.delete(0, 50)
            E_C2.delete(0, 50)
            E_M1.delete(0, 50)
            E_M2.delete(0, 50)
            E_T1.delete(0, 50)
            E_T2.delete(0, 50)
            Steering.delete(0, 50)

            E_C1.insert ( 0, '%d'%int(s1) ) 
            E_C2.insert ( 0, '%d'%int(s2) ) 
            E_M1.insert ( 0, '%d'%int(s3) ) 
            E_M2.insert ( 0, '%d'%int(s4) )
            E_T1.insert ( 0, '%d'%int(s5) ) 
            E_T2.insert ( 0, '%d'%int(s6) )
            Steering.insert ( 0, '%d'%int(s7) )

        elif 'list' in str(code_car):         # Scan result receiving start
            processList(code_car)

        elif 'voice_3' in str(code_car):         # put this case before the numbers below because of the 3
            BtnSR3.config(fg='#0277BD', bg='#BBDEFB')
            labelStatus.config(text='Sphinx SR')        #Put the text on the label
            speech_status = 1

        elif 'findline' in str(code_car):        #Translate the code to text
            BtnFL.config(text='Finding', fg='#0277BD', bg='#BBDEFB')
            labelStatus.config(text='Find Line') 
            findline_status = 1
        
        elif 'lightsON' in str(code_car):        #Translate the code to text
            buttonHeadlights.config(text='Lights ON', fg='#0277BD', bg='#BBDEFB')
            labelStatus.config(text='Lights On')        #Put the text on the label
            led_status = 1
        
        elif 'lightsOFF' in str(code_car):        #Translate the code to text
            buttonHeadlights.config(text='Lights OFF', fg=TEXT_COLOR, bg=BUTTON_COLOR)
            labelStatus.config(text='Lights OFF')        #Put the text on the label
            led_status = 0

        elif 'oncvon' in str(code_car):
            BtnOCV.config(text='OpenCV ON', fg='#0277BD', bg='#BBDEFB')
            BtnFL.config(text='Find Line', fg=TEXT_COLOR, bg=BUTTON_COLOR)
            labelStatus.config(text='OpenCV ON')
            opencv_status = 1

        elif 'auto_status_off' in str(code_car):
            BtnSR3.config(fg=TEXT_COLOR, bg=BUTTON_COLOR, state='normal')
            BtnOCV.config(text='OpenCV', fg=TEXT_COLOR, bg=BUTTON_COLOR, state='normal')
            BtnFL.config(text='Find Line', fg=TEXT_COLOR, bg=BUTTON_COLOR)
            buttonFollow.config(text='Follow', fg=TEXT_COLOR, bg=BUTTON_COLOR, state='normal')
            findline_status = 0
            speech_status   = 0
            opencv_status   = 0
            auto_status     = 0
            led_status      = 0

        # put these checks for numbers after everthing else because numbers could be in many of these messages
        # TODO; been bitten by this several times, need to change these to something more robust
        elif '0' in str(code_car):               #Translate the code to text
            labelStatus.config(text='Follow Mode On')     #Put the text on the label
            buttonFollow.config(text='Following', fg='#0277BD', bg='#BBDEFB')
            auto_status = 1

        elif '1' in str(code_car):               #Translate the code to text
            labelStatus.config(text='Moving Forward')   #Put the text on the label

        elif '2' in str(code_car):               #Translate the code to text
            labelStatus.config(text='Moving Backward')  #Put the text on the label

        elif '3' in str(code_car):               #Translate the code to text
            labelStatus.config(text='Turning Left')     #Put the text on the label

        elif '4' in str(code_car):               #Translate the code to text
            labelStatus.config(text='Turning Right')    #Put the text on the label

        elif '5' in str(code_car):               #Translate the code to text
            labelStatus.config(text='Look Up')          #Put the text on the label

        elif '6' in str(code_car):               #Translate the code to text
            labelStatus.config(text='Look Down')        #Put the text on the label

        elif '7' in str(code_car):               #Translate the code to text
            labelStatus.config(text='Look Left')        #Put the text on the label

        elif '8' in str(code_car):               #Translate the code to text
            labelStatus.config(text='Look Right')       #Put the text on the label

        elif '9' in str(code_car):               #Translate the code to text
            labelStatus.config(text='Stop')             #Put the text on the label       


def fpvThread():       # thread that displays incoming fpv video
    while True:
        try:
            frame = footage_socket.recv_string()
        except Exception:
            print ("got socket exception in fpvThread, will exit thread")
            time.sleep(1)
            sys.exit()
        img = base64.b64decode(frame)
        npimg = np.frombuffer(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        cv2.imshow("Stream", source)
        cv2.waitKey(1)                


def connectThread():           # Thread that tries to connect with the robot car server
    global tcpClicSock, ip_entry
    
    buttonConnect.config(state='disabled') #Disable the Connect button while trying to connect
    ip_adr=ip_entry.get()    #Get the IP address from Entry

    if ip_adr == '':         #If no input IP address in Entry, try to import a default IP
        ip_adr = config.importConfig('IP')
        if ip_adr == None:
            ip_adr = "0.0.0.0"
        labelConnectionStatus.config(text='Connecting')
        labelConnectionStatus.config(bg='#FF8F00')
        labelIpAddress.config(text='Default:%s'%ip_adr)
    
    for i in range (1,6): # Retry 5 additional times if connection fails
        try:
            print("Connecting to server @ %s:%d..." %(ip_adr, SERVER_PORT))
            address = (ip_adr, SERVER_PORT)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Set connection value for socket
            s.connect(address)               #Connection with the server
        
            print("robot Connected")
            tcpClicSock = s
        
            config.exportConfig('IP', ip_adr)
            labelIpAddress.config(text='IP:%s'%ip_adr)
            labelConnectionStatus.config(text='Connected')
            labelConnectionStatus.config(bg='#558B2F')

            ip_entry.config(state='disabled')      #Disable the Entry
                    
            at=thread.Thread(target=receiveThread) #Define a thread for data receiving
            at.setDaemon(True)                     #True means it is a front thread, will close when mainloop() closes
            at.start()                             #Thread starts

            video_thread=thread.Thread(target=fpvThread) #Define a thread for receiving and displaying fpv video
            video_thread.setDaemon(True)          #True means it is a front thread, will close when mainloop() closes
            print('FPV Connected')
            video_thread.start()                          #Thread starts
            break

        except Exception as e:
            print(e)
            print("Failed to connect to server!")
            print('Tried %d/5 time(s)'%i)
            labelConnectionStatus.config(text='Tried %d/5 time(s)'%i)
            labelConnectionStatus.config(bg='#EF6C00')
            tcpClicSock = None
            time.sleep(1)
            continue

    if tcpClicSock == None:
        labelConnectionStatus.config(text='Disconnected')
        labelConnectionStatus.config(bg='#F44336')
        buttonConnect.config(state='normal') #enable the Connect button


def connect(event=None):       #Call this function to start thread to connect with the robot car server
    sc=thread.Thread(target=connectThread)  #Define a thread for connection
    sc.setDaemon(True)                      #True means it is a front thread, will close when mainloop() closes
    sc.start()                              #Thread starts


def sendForward(event):         #When this function is called, client commands the car to move forward
    tcpClicSock.send(('forward').encode())


def sendBackward(event):            #When this function is called, client commands the car to move backward
    tcpClicSock.send(('backward').encode())


def sendStop(event):            #When this function is called, client commands the car to stop moving
    tcpClicSock.send(('stop').encode())


def sendMiddle(event):          #When this function is called, client commands the car go straight
    tcpClicSock.send(('middle').encode())


def sendLeft(event):            #When this function is called, client commands the car to turn left
    tcpClicSock.send(('Left').encode())


def sendRight(event):           #When this function is called, client commands the car to turn right
    tcpClicSock.send(('Right').encode())


def sendSteerLeft(event):            #When this function is called, client commands the car to turn left
    tcpClicSock.send(('SteerLeft').encode())


def sendSteerRight(event):           #When this function is called, client commands the car to turn right
    tcpClicSock.send(('SteerRight').encode())


def sendLookLeft(event):               #Camera look left
    tcpClicSock.send(('l_le').encode())


def sendLookRight(event):              #Camera look right
    tcpClicSock.send(('l_ri').encode())


def sendLookUp(event):                 #Camera look up
    tcpClicSock.send(('l_up').encode())


def sendLookDown(event):               #Camera look down
    tcpClicSock.send(('l_do').encode())


def sendLookAhead(event):                   #Camera look ahead
    tcpClicSock.send(('ahead').encode())


def sendExit(event):            #When this function is called, client commands the car to shut down
    tcpClicSock.send(('exit').encode())


def sendOff(event):            #When this function is called, client commands the car to switch off auto mode
    tcpClicSock.send(('Off').encode())


def sendScan(event):                 #When this function is called, client commands the ultrasonic to scan
    tcpClicSock.send(('scan').encode())


def sendSpeed():                 #Call this function for speed adjustment
    tcpClicSock.send(('spdset:%s'%var_spd.get()).encode())   #Get a speed value from IntVar and send it to the car
    labelSpeedStatus.config(text='Speed:%s'%var_spd.get())             #Put the speed value on the speed status label


def sendEC1(event):            #Call this function for speed adjustment
    tcpClicSock.send(('EC1set:%s'%E_C1.get()).encode())   #Get a speed value from IntVar and send it to the car


def sendEC2(event):            #Call this function for speed adjustment
    tcpClicSock.send(('EC2set:%s'%E_C2.get()).encode())   #Get a speed value from IntVar and send it to the car


def sendEM1(event):            #Call this function for speed adjustment
    tcpClicSock.send(('EM1set:%s'%E_M1.get()).encode())   #Get a speed value from IntVar and send it to the car


def sendEM2(event):            #Call this function for speed adjustment
    tcpClicSock.send(('EM2set:%s'%E_M2.get()).encode())   #Get a speed value from IntVar and send it to the car


def sendET1(event):            #Call this function for speed adjustment
    tcpClicSock.send(('LUMset:%s'%E_T1.get()).encode())   #Get a speed value from IntVar and send it to the car


def sendET2(event):            #Call this function for speed adjustment
    tcpClicSock.send(('LDMset:%s'%E_T2.get()).encode())   #Get a speed value from IntVar and send it to the car


def sendSteering(event):            #Call this function for steering adjustment
    tcpClicSock.send(('STEERINGset:%s'%Steering.get()).encode())   


def sendFindLine(event):            #Line follow mode
    if findline_status == 0:
        tcpClicSock.send(('findline').encode())
    else:
        tcpClicSock.send(('Stop').encode())


def sendHeadlights(event):               #Turn on the LEDs
    if led_status == 0:
        tcpClicSock.send(('lightsON').encode())
    else:
        tcpClicSock.send(('lightsOFF').encode())


def sendSR3():                     #Start speech recognition mode
    if speech_status == 0:
        tcpClicSock.send(('voice_3').encode())
    else:
        tcpClicSock.send(('Stop').encode())


def sendOpencv():                  #Start OpenCV mode
    if opencv_status == 0:
        tcpClicSock.send(('opencv').encode())
    else:
        tcpClicSock.send(('Stop').encode())


def sendAuto(event):            #When this function is called, client commands the car to start auto mode
    if auto_status == 0:
        tcpClicSock.send(('auto').encode())
    else:
        tcpClicSock.send(('Stop').encode())


def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        #r.record(source, duration=2)
        l_VIN.config(text='Say something!')
        BtnVIN.config(fg='#0277BD', bg='#BBDEFB')
        l_VIN.update_idletasks()      # cause widgets in GUI to update now and display properly
        print("listening!")
        audio = r.listen(source)
    try:
        print("calling sphinx with audio")
        a2t=r.recognize_sphinx(audio, keyword_entries=[('forward', .20),
                                                       ('backward', 1.0),
                                                       ('left turn', 1.0),
                                                       ('right turn', 1.0),
                                                       ('stop', 1.0),
                                                       ('off', 1.0),
                                                       ('find line', 0.50),  # find line
                                                       ('follow', 1),
                                                       ('head lights', 1)])      
        print("sphinx retuned: %s" %str(a2t))
        print("Sphinx thinks you said " + a2t.split()[0])
        return a2t
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    return 'Try again'


def voiceCommand(event):
    v_command=voice_input()
    l_VIN.config(text='%s'%v_command)
    BtnVIN.config(fg=TEXT_COLOR, bg=BUTTON_COLOR)
    if tcpClicSock == None:              # for offline testing
        return
    if  v_command.startswith('forward'):
        sendForward()
    elif v_command.startswith('backward'):
        sendBackward()
    elif v_command.startswith('left'):
        sendLeft()
    elif v_command.startswith('right'):
        sendRight()
    elif v_command.startswith('stop'):
        sendStop()
    elif v_command.startswith('off'):
        sendOff()
    elif v_command.startswith('find'):
        sendFindLine()
    elif v_command.startswith('follow'):
        sendAuto()
    elif v_command.startswith('head'):
        sendHeadlights()
    else:
        pass


def init():
    global ip_entry, labelSpeedStatus, labelConnectionStatus, labelIpAddress, buttonConnect, buttonFollow, BtnFL, buttonHeadlights, BtnOCV, \
           var_x_scan, var_spd, Steering, BtnSR3, labelStatus, BtnIP, E_C1, E_C2, E_M1, E_M2, E_T1, E_T2, l_VIN, BtnVIN

    window.title('Adeept')              #Main window title
    window.geometry('917x630')          #Main window size, middle of the English letter x.
    window.config(bg=BACKGROUND_COLOR)  #Set the background color of root window

    print ("running on " + sys.platform + " platform")
    # adjust some GUI widget widths and positions for raspbian and windows differences
    if "linux" in sys.platform:
        IP_ENTRY_WIDTH = 14
        BTN_WIDTH_1 = 5
        BTN_WIDTH_2 = 12
        INFO_WIDTH = 43
        INFO_X = 247
        IP_WIDTH = 15
        # reducing font size so widgets fit right on Raspbian
        #tf = font.nametofont("TkTextFont")      # used in entry widgets
        #tf.configure(size=8)
        #print ("TkTextFont:")
        #print (tf.actual())
        #tf = font.nametofont("TkDefaultFont")   # used in buttons
        #tf.configure(size=7)
        #print ("TkDefaultFont:")
        #print (tf.actual())
    else:   # for windows
        IP_ENTRY_WIDTH = 16
        BTN_WIDTH_1 = 8
        BTN_WIDTH_2 = 15
        INFO_WIDTH = 39
        INFO_X = 240
        IP_WIDTH = 18
        
    var_spd = tk.StringVar()  #Speed value saved in a StringVar
    var_spd.set(1)            #Set default speed, to change the default speed value in the car,you need to click button 'Set'

    var_x_scan = tk.IntVar()  #Scan range value saved in a IntVar
    var_x_scan.set(2)         #Set a default scan value

    logo =tk.PhotoImage(file = 'logo.png')         #Define the picture of logo,but only supports '.png' and '.gif'
    l_logo=tk.Label(window, image=logo, bg=BACKGROUND_COLOR) #Set a label to show the logo picture
    l_logo.photo = logo
    l_logo.place(x=30,y=13)                        #Place the Label in a right position

    BtnC1 = tk.Button(window, width=BTN_WIDTH_2, text='Camera Ver. Home', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    BtnC1.place(x=785,y=10)
    E_C1 = tk.Entry(window, show=None, width=IP_ENTRY_WIDTH, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
    E_C1.place(x=785,y=45)                             #Define a Entry and put it in position

    BtnC2 = tk.Button(window, width=BTN_WIDTH_2, text='Camera Hor. Home', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    BtnC2.place(x=785,y=100)
    E_C2 = tk.Entry(window, show=None, width=IP_ENTRY_WIDTH, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
    E_C2.place(x=785,y=135)                             #Define a Entry and put it in position

    BtnM1 = tk.Button(window, width=BTN_WIDTH_2, text='Motor A Speed', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    BtnM1.place(x=785,y=190)
    E_M1 = tk.Entry(window, show=None, width=IP_ENTRY_WIDTH, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
    E_M1.place(x=785, y=225)                             #Define a Entry and put it in position

    BtnM2 = tk.Button(window, width=BTN_WIDTH_2, text='Motor B Speed', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    BtnM2.place(x=785 ,y=280)
    E_M2 = tk.Entry(window, show=None, width=IP_ENTRY_WIDTH, bg="#37474F",fg='#eceff1', exportselection=0, justify='center')
    E_M2.place(x=785, y=315)                             #Define a Entry and put it in position

    BtnT1 = tk.Button(window, width=BTN_WIDTH_2, text='Look Up Max', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    BtnT1.place(x=785, y=370)
    E_T1 = tk.Entry(window, show=None, width=IP_ENTRY_WIDTH, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
    E_T1.place(x=785, y=405)                             #Define a Entry and put it in position

    BtnT2 = tk.Button(window, width=BTN_WIDTH_2, text='Look Down Max', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    BtnT2.place(x=785, y=460)
    E_T2 = tk.Entry(window, show=None, width=IP_ENTRY_WIDTH, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
    E_T2.place(x=785, y=495)                             #Define a Entry and put it in position

    E_C1.insert ( 0, 'Default:425' ) 
    E_C2.insert ( 0, 'Default:425' ) 
    E_M1.insert ( 0, 'Default:100' ) 
    E_M2.insert ( 0, 'Default:100' )
    E_T1.insert ( 0, 'Default:662' ) 
    E_T2.insert ( 0, 'Default:295' )

    BtnSteering = tk.Button(window, width=BTN_WIDTH_2, text='Steering Cen.', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    BtnSteering.place(x=785, y=550)
    Steering = tk.Entry(window, show=None, width=IP_ENTRY_WIDTH, bg="#37474F", fg='#eceff1', exportselection=0, justify='center')
    Steering.place(x=785, y=585)                             #Define a Entry and put it in position

    BtnOCV = tk.Button(window, width=BTN_WIDTH_1, text='OpenCV', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge', command=sendOpencv)
    BtnOCV.place(x=30, y=420)

    BtnFL = tk.Button(window, width=BTN_WIDTH_1, text='Find Line', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    BtnFL.place(x=105, y=420)

    BtnSR3 = tk.Button(window, width=BTN_WIDTH_1, text='Sphinx SR', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge', command=sendSR3)
    BtnSR3.place(x=300, y=495)

    can_scan = tk.Canvas(window, bg=CANVAS_COLOR, height=250, width=320, highlightthickness=0) #define a canvas
    can_scan.place(x=440, y=330) #Place the canvas
    line = can_scan.create_line(0, 62, 320, 62, fill='darkgray')   #Draw a line on canvas
    line = can_scan.create_line(0, 124, 320, 124, fill='darkgray') #Draw a line on canvas
    line = can_scan.create_line(0, 186, 320, 186, fill='darkgray') #Draw a line on canvas
    line = can_scan.create_line(160, 0, 160, 250, fill='darkgray') #Draw a line on canvas
    line = can_scan.create_line(80, 0, 80, 250, fill='darkgray')   #Draw a line on canvas
    line = can_scan.create_line(240, 0, 240, 250, fill='darkgray') #Draw a line on canvas
    x_range = var_x_scan.get()
    can_tex_11=can_scan.create_text((27, 178), text='%sm'%round((x_range/4),2), fill='#aeea00')     #Create a text on canvas
    can_tex_12=can_scan.create_text((27,116), text='%sm'%round((x_range/2),2), fill='#aeea00')     #Create a text on canvas
    can_tex_13=can_scan.create_text((27,54), text='%sm'%round((x_range*0.75),2), fill='#aeea00')  #Create a text on canvas

    s1 = tk.Scale(window, label="               < SLOW  Speed Adjustment   FAST >",
    from_=0.9, to=1, orient=tk.HORIZONTAL, length=400,
    showvalue=0.01, tickinterval=0.01, resolution=0.01, variable=var_spd, fg=TEXT_COLOR, bg=BACKGROUND_COLOR, highlightthickness=0)
    s1.place(x=200, y=100)          #Define a Scale and put it in position on linux platform

    s3 = tk.Scale(window, label="< NEAR  Scan Range Adjustment(Meters) FAR >",
    from_=1, to=5, orient=tk.HORIZONTAL, length=300,
    showvalue=1, tickinterval=1, resolution=1, variable=var_x_scan, fg=TEXT_COLOR, bg=BACKGROUND_COLOR, highlightthickness=0)
    s3.place(x=30, y=320)    

    labelStatus=tk.Label(window, width=18, text='Status', fg=TEXT_COLOR, bg=BUTTON_COLOR)
    labelStatus.place(x=30, y=110)                           #Define a Label and put it in position

    labelSpeedStatus=tk.Label(window, width=18, text='Speed:%s'%(var_spd.get()), fg=TEXT_COLOR, bg=BUTTON_COLOR)
    labelSpeedStatus.place(x=30, y=145)                         #Define a Label and put it in position

    label=tk.Label(window, width=10, text='IP Address:', fg=TEXT_COLOR, bg='#000000')
    label.place(x=165, y=15)                         #Define a Label and put it in position

    labelConnectionStatus=tk.Label(window, width=IP_WIDTH, text='Disconnected', fg=TEXT_COLOR, bg='#F44336')
    labelConnectionStatus.place(x=637, y=110)                         #Define a Label and put it in position

    labelIpAddress=tk.Label(window, width=IP_WIDTH, text='Use default IP', fg=TEXT_COLOR, bg=BUTTON_COLOR)
    labelIpAddress.place(x=637, y=145)                         #Define a Label and put it in position

    label=tk.Label(window,
                   width=INFO_WIDTH, anchor=tk.W, justify=tk.LEFT, font='TkFixedFont',
                   text='<-- CAR CONTROLS      HEAD CONTROLS -->\n' \
                        '     W - forward       I - up\n' \
                        '     S - backward      M - down\n' \
                        '     A - max left      J - left\n' \
                        '     D - max right     L - right\n' \
                        '     Q - steer left    K - home\n' \
                        '     E - steer right   H - headlights\n' \
                        '     Z - auto on       F - find line\n' \
                        '     C - auto off      X - scan' ,
                   fg='#212121', bg='#90a4ae')
    label.place(x=INFO_X, y=173)                    #Define a Label and put it in position

    ip_entry = tk.Entry(window, show=None, width=IP_ENTRY_WIDTH, bg="#37474F", fg='#eceff1')
    ip_entry.place(x=170, y=40)                             #Define a Entry and put it in position

    buttonConnect= tk.Button(window, width=8, text='Connect', fg=TEXT_COLOR, bg=BUTTON_COLOR, command=connect, relief='ridge')
    buttonConnect.place(x=300, y=35)                          #Define a Button and put it in position

    BtnVIN = tk.Button(window, width=BTN_WIDTH_2, text='Voice Input', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    BtnVIN.place(x=30, y=495)

    l_VIN=tk.Label(window, width=16, text='Voice commands', fg=TEXT_COLOR, bg=BUTTON_COLOR)
    l_VIN.place(x=30, y=465)      

    #Define buttons and put these in position
    buttonSteerRight = tk.Button(window, width=BTN_WIDTH_1, text='Right', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonSteerRight.place(x=170, y=195)

    buttonSteerLeft = tk.Button(window, width=BTN_WIDTH_1, text='Left', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonSteerLeft.place(x=30, y=195)

    buttonForward = tk.Button(window, width=BTN_WIDTH_1, text='Forward', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonForward.place(x=100, y=195)

    buttonMiddle = tk.Button(window, width=BTN_WIDTH_1, text='Middle', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonMiddle.place(x=100, y=230)

    buttonBackward = tk.Button(window, width=BTN_WIDTH_1, text='Backward', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonBackward.place(x=100, y=265)

    buttonMaxLeft = tk.Button(window, width=BTN_WIDTH_1, text='Max Left', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonMaxLeft.place(x=30, y=230)

    buttonMaxRight = tk.Button(window, width=BTN_WIDTH_1, text='Max Right', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonMaxRight.place(x=170, y=230)

    buttonHeadlights = tk.Button(window, width=BTN_WIDTH_1, text='Headlights', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonHeadlights.place(x=330, y=420)

    buttonOff = tk.Button(window, width=BTN_WIDTH_1, text='Off', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonOff.place(x=255, y=420)

    buttonFollow = tk.Button(window, width=BTN_WIDTH_1, text='Follow', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonFollow.place(x=180, y=420)
    
    buttonHeadLeft = tk.Button(window, width=BTN_WIDTH_1, text='Left', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonHeadLeft.place(x=565, y=230)

    buttonHeadRight = tk.Button(window, width=BTN_WIDTH_1, text='Right', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonHeadRight.place(x=705, y=230)

    buttonHeadDown = tk.Button(window, width=BTN_WIDTH_1, text='Down', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonHeadDown.place(x=635, y=265)

    buttonHeadUp = tk.Button(window, width=BTN_WIDTH_1, text='Up', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonHeadUp.place(x=635, y=195)

    buttonHeadHome = tk.Button(window, width=BTN_WIDTH_1, text='Home', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonHeadHome.place(x=635, y=230)

    buttonExit = tk.Button(window, width=BTN_WIDTH_1, text='Exit', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonExit.place(x=705, y=10)

    buttonSet = tk.Button(window, width=BTN_WIDTH_1, text='Set', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonSet.place(x=535, y=107)

    buttonScan = tk.Button(window, width=BTN_WIDTH_1, text='Scan', fg=TEXT_COLOR, bg=BUTTON_COLOR, relief='ridge')
    buttonScan.place(x=350, y=330)

    # Bind the buttons with the corresponding callback function
    # first bind for button pressing
    buttonSteerRight.bind('<ButtonPress-1>', sendSteerRight)
    buttonSteerLeft.bind('<ButtonPress-1>', sendSteerLeft)
    buttonMiddle.bind('<ButtonPress-1>', sendMiddle)
    buttonForward.bind('<ButtonPress-1>', sendForward)
    buttonBackward.bind('<ButtonPress-1>', sendBackward)
    buttonMaxLeft.bind('<ButtonPress-1>', sendLeft)
    buttonMaxRight.bind('<ButtonPress-1>', sendRight)
    buttonOff.bind('<ButtonPress-1>', sendOff)
    buttonFollow.bind('<ButtonPress-1>', sendAuto)
    buttonHeadLeft.bind('<ButtonPress-1>', sendLookLeft)
    buttonHeadRight.bind('<ButtonPress-1>', sendLookRight)
    buttonHeadDown.bind('<ButtonPress-1>', sendLookDown)
    buttonHeadUp.bind('<ButtonPress-1>', sendLookUp)
    buttonHeadHome.bind('<ButtonPress-1>', sendLookAhead)
    buttonExit.bind('<ButtonPress-1>', sendExit)
    buttonSet.bind('<ButtonPress-1>', sendSpeed)
    buttonScan.bind('<ButtonPress-1>', sendScan)
    BtnC1.bind('<ButtonPress-1>', sendEC1)
    BtnC2.bind('<ButtonPress-1>', sendEC2)
    BtnM1.bind('<ButtonPress-1>', sendEM1)
    BtnM2.bind('<ButtonPress-1>', sendEM2)
    BtnT1.bind('<ButtonPress-1>', sendET1)
    BtnT2.bind('<ButtonPress-1>', sendET2)
    BtnSteering.bind('<ButtonPress-1>', sendSteering)
    BtnFL.bind('<ButtonPress-1>', sendFindLine)
    BtnVIN.bind('<ButtonPress-1>', voiceCommand)
    buttonHeadlights.bind('<ButtonPress-1>', sendHeadlights)

    # bind for button release
    buttonForward.bind('<ButtonRelease-1>', sendStop)
    buttonBackward.bind('<ButtonRelease-1>', sendStop)
    buttonMaxLeft.bind('<ButtonRelease-1>', sendStop)
    buttonMaxRight.bind('<ButtonRelease-1>', sendStop)

    # Bind the keys with the corresponding callback function
    window.bind('<KeyPress-w>', sendForward) 
    window.bind('<KeyPress-a>', sendLeft)
    window.bind('<KeyPress-d>', sendRight)
    window.bind('<KeyPress-s>', sendBackward)
    window.bind('<KeyPress-q>', sendSteerLeft)
    window.bind('<KeyPress-e>', sendSteerRight)

    # When these keys is released,call the function sendstop()
    window.bind('<KeyRelease-w>', sendStop)
    window.bind('<KeyRelease-a>', sendMiddle)
    window.bind('<KeyRelease-d>', sendMiddle)
    window.bind('<KeyRelease-s>', sendStop)
    window.bind('<KeyRelease-h>', sendHeadlights)
    window.bind('<KeyRelease-f>', sendFindLine)
    window.bind('<KeyRelease-v>', voiceCommand)

    # Press these keyss to call the corresponding function()
    window.bind('<KeyPress-c>', sendOff)
    window.bind('<KeyPress-z>', sendAuto) 
    window.bind('<KeyPress-j>', sendLookLeft)
    window.bind('<KeyPress-l>', sendLookRight)
    window.bind('<KeyPress-k>', sendLookAhead)
    window.bind('<KeyPress-m>', sendLookDown)
    window.bind('<KeyPress-i>', sendLookUp)
    window.bind('<KeyPress-x>', sendScan)
    window.bind('<Return>', connect)
    window.bind('<Shift-c>', sendStop)


# Main program body    
if __name__ == '__main__':
    # the following code doesn't seem to be needed so I commented it out for now
    #opencv_socket = socket()
    #opencv_socket.bind(('0.0.0.0', 8080))
    #opencv_socket.listen(0)

    context = zmq.Context()
    footage_socket = context.socket(zmq.SUB)
    footage_socket.bind('tcp://*:5555')
    footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    init()             # Load GUI
    window.mainloop()  # Run the window event processing loop

    if tcpClicSock != None:
        #command the server to quit if it hasn't already been told to exit
        tcpClicSock.send(('quit').encode())
        print ("closing WIFI connection to robot")
        tcpClicSock.close()          # Close socket or it may not connect with the server again

    print ("destroying zmq context")
    # kill the zmq context to cause an exception to be raised in video thread so that
    # it quits and allows the destroyAllWindows to close the FPV window reliably
    context.destroy()
    time.sleep(1)
    print ("destroying FPV window")
    cv2.destroyAllWindows()
    print ("exiting robot client")
