#!/usr/bin/python3

import pyttsx3
import sys, os

def say(phrase):
    print("say: " + phrase)
    engine.say(phrase)
    engine.runAndWait()


def changeVolume(change):
    volume = engine.getProperty('volume')
    if change == "+":
        engine.setProperty('volume', volume+.1)
    else:
        engine.setProperty('volume', volume-.1)


def changeRate(change):
    rate = engine.getProperty('rate')
    if change == "+":
        engine.setProperty('rate', rate+20)
    else:
        engine.setProperty('rate', rate-20)


engine = pyttsx3.init()
engine.setProperty('voice', "english-us")
engine.runAndWait()

if __name__ == '__main__':

    print(engine.getProperty('voice'))
    say("testing")
    """
    voices = engine.getProperty('voices')
    print(voices)
    for voice in voices:
        print(voice)
        engine.setProperty('voice', voice.id)
        print(engine.getProperty('voice'))
        #rate = engine.getProperty('rate')
        #engine.setProperty('rate', rate-20)
        engine.say("test of voices.")
        engine.runAndWait()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-40)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.5)
    engine.say("testing.")
    engine.runAndWait()
    """
