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
    # TODO: add exception handling so thread is more robust
    channel = None
    while True:
        while (channel != None) and (channel.get_busy()):
            time.sleep(.1)
        if not fifo.empty():
            channel = sounds[fifo.get()].play()


mixer.init()
sounds = dict.fromkeys(soundKeys, None)

bye_bye = mixer.Sound('sounds/bye-bye.wav')
sounds[BYE_BYE] = bye_bye

birds = mixer.Sound('sounds/cartoon-birds.wav')
sounds[CARTOON_BIRDS] = birds

cha_ching = mixer.Sound('sounds/cha-ching.wav')
sounds[CHA_CHING] = cha_ching

cow_moo = mixer.Sound('sounds/cow-moo.wav')
sounds[COW_MOO] = cow_moo

craft_landing = mixer.Sound('sounds/craft-landing.wav')
sounds[CRAFT_LANDING] = craft_landing

dial_tone = mixer.Sound('sounds/dial-tone.wav')
sounds[DIAL_TONE] = dial_tone

dog_panting = mixer.Sound('sounds/dog-panting.wav')
sounds[DOG_PANTING] = dog_panting

evil_laugh = mixer.Sound('sounds/evil-laugh.wav')
sounds[EVIL_LAUGH] = evil_laugh

fire_truck = mixer.Sound('sounds/fire-truck-horn.wav')
sounds[FIRE_TRUCK] = fire_truck

front_desk_bell = mixer.Sound('sounds/front-desk-bell.wav')
sounds[FRONT_DESK_BELL] = front_desk_bell

funny_voices = mixer.Sound('sounds/funny-voices.wav')
sounds[FUNNY_VOICES] = funny_voices

glass_ping = mixer.Sound('sounds/glass-ping.wav')
sounds[GLASS_PING] = glass_ping

happy_ping = mixer.Sound('sounds/happy-ping.wav')
sounds[HAPPY_PING] = happy_ping

i_am_a_robot = mixer.Sound('sounds/i-am-a-robot.wav')
sounds[I_AM_A_ROBOT] = i_am_a_robot

i_love_you = mixer.Sound('sounds/i-love-you.wav')
sounds[I_LOVE_YOU] = i_love_you

magic = mixer.Sound('sounds/magic.wav')
sounds[MAGIC] = magic

martian_death_ray = mixer.Sound('sounds/martian-death-ray.wav')
sounds[MARTIAN_DEATH_RAY] = martian_death_ray

pew_pew = mixer.Sound('sounds/pew-pew.wav')
sounds[PEW_PEW] = pew_pew

phone_vibrating = mixer.Sound('sounds/phone-vibrating.wav')
sounds[PHONE_VIBRATING] = phone_vibrating

r2d2 = mixer.Sound('sounds/r2d2.wav')
sounds[R2D2] = r2d2

robot_blip = mixer.Sound('sounds/robot-blip.wav')
robot_blip.set_volume(.40)
sounds[ROBOT_BLIP] = robot_blip

small_dog_barking = mixer.Sound('sounds/small-dog-barking.wav')
sounds[SMALL_DOG_BARKING] = small_dog_barking

toilet_flush = mixer.Sound('sounds/toilet-flush.wav')
sounds[TOILET_FLUSH] = toilet_flush

t = threading.Thread(target = playSoundThread)  # Define a thread for playing sounds
t.setDaemon(True)                               # True means it is a front thread, closes when the mainloop() closes
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
