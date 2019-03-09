#!/usr/bin/python3
# File name   : sounds.py
# Description : module to support producing sounds
# Website     : github.com/bswe
# E-mail      : billbollenba@yahoo.com
# Author      : WCB
# Date        : 3/7/2019

import sys
sys.path.insert(0, "../common")
import config
from comunication import *
import time
import atexit
import queue
import threading
from pygame import mixer

fifo = queue.Queue()

def playSound(key):
    print("playSound: " + key)
    fifo.put(key)


def playSoundThread():
    channel = None
    while True:
        while (channel != None) and (channel.get_busy()):
            time.sleep(.1)
        if not fifo.empty():
            channel = sounds[fifo.get()].play()


def cleanup():
    print("sounds module: executing cleanup()")


mixer.init()
sounds = dict.fromkeys(soundKeys, None)

bye_bye = mixer.Sound('sounds/bye-bye.wav')
bye_bye.set_volume(.40)
sounds[BYE_BYE] = bye_bye

birds = mixer.Sound('sounds/cartoon-birds.wav')
birds.set_volume(.40)
sounds[CARTOON_BIRDS] = birds

cha_ching = mixer.Sound('sounds/cha-ching.wav')
cha_ching.set_volume(.40)
sounds[CHA_CHING] = cha_ching

cow_moo = mixer.Sound('sounds/cow-moo.wav')
cow_moo.set_volume(.40)
sounds[COW_MOO] = cow_moo

craft_landing = mixer.Sound('sounds/craft-landing.wav')
craft_landing.set_volume(.40)
sounds[CRAFT_LANDING] = craft_landing

fire_truck = mixer.Sound('sounds/fire-truck-horn.wav')
fire_truck.set_volume(.40)
sounds[FIRE_TRUCK] = fire_truck

i_am_a_robot = mixer.Sound('sounds/i-am-a-robot.wav')
i_am_a_robot.set_volume(.40)
sounds[I_AM_A_ROBOT] = i_am_a_robot

i_love_you = mixer.Sound('sounds/i-love-you.wav')
i_love_you.set_volume(.40)
sounds[I_LOVE_YOU] = i_love_you

pew_pew = mixer.Sound('sounds/pew-pew.wav')
pew_pew.set_volume(.40)
sounds[PEW_PEW] = pew_pew

r2d2 = mixer.Sound('sounds/r2d2.wav')
r2d2.set_volume(.40)
sounds[R2D2] = r2d2

atexit.register(cleanup)

t = threading.Thread(target = playSoundThread)   # Define a thread for playing sounds
t.setDaemon(True)               # True means it is a front thread, closes when the mainloop() closes
t.start()                                 


if __name__ == '__main__':
    #playSound(BYE_BYE)
    playSound(CARTOON_BIRDS)
    playSound(CHA_CHING)
    playSound(COW_MOO)
    playSound(CRAFT_LANDING)
    #playSound(FIRE_TRUCK)
    #playSound(I_AM_A_ROBOT)
    #playSound(I_LOVE_YOU)
    #playSound(PEW_PEW)
    #playSound(R2D2)
