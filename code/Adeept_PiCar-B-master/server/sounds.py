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
import time
import atexit
from pygame import mixer
from os import path

BYE_BYE       = 'Bye Bye'
CARTOON_BIRDS = 'Birds'
CHA_CHING     = 'Cha Ching'
COW_MOO       = 'Cow Moo'
CRAFT_LANDING = 'Craft Landing'
DIAL_TONE     = 'Dial Tone'
DOG_PANTING   = 'Dog Panting'
EVIL_LAUGH    = 'Evil Laugh'
FIRE_TRUCK    = 'Fire Truck'
I_AM_A_ROBOT  = 'I am a robot'
I_LOVE_YOU    = 'I Love You'
MAGIC         = 'Magic'
PEW_PEW       = 'Pew Pew'
R2D2          = 'R2D2'

soundKeys = {BYE_BYE,
             CARTOON_BIRDS,
             CHA_CHING,
             COW_MOO,
             CRAFT_LANDING,
             DIAL_TONE,
             DOG_PANTING,
             EVIL_LAUGH,
             FIRE_TRUCK,
             I_AM_A_ROBOT,
             I_LOVE_YOU,
             MAGIC,
             PEW_PEW,
             R2D2}

channel = None
sounds = None


def playSound(key):
    global channel
    while (channel != None) and (channel.get_busy()):
        time.sleep(.1)
    channel = sounds[key].play()


def cleanup():
    print("sounds module: executing cleanup()")


def init():
    global sounds
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
