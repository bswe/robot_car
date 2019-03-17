#!/usr/bin/python3

import pyttsx3
import sys, os

def say(phrase):
    print("say: " + phrase)
    engine.say(phrase)
    engine.runAndWait()


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
