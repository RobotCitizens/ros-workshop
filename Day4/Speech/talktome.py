#!/usr/bin/env python
# -*- coding: utf-8 -*-

import speech_recognition as sr
from playsound import playsound

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Record Audio
r = sr.Recognizer()
m = sr.Microphone()

#set threhold level
print(' Quiet Please ')
with m as source: r.adjust_for_ambient_noise(source)
print("Set minimum energy threshold to {}".format(r.energy_threshold))

# Speech recognition using Google Speech Recognition
while (True):
    playsound("./speak_after.mp3")
    playsound("./signal.mp3")
    print("Say something!")
    with sr.Microphone() as source:
        audio = r.listen(source, phrase_time_limit=3)
        playsound("./signal.mp3")
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use  key="GOOGLE_SPEECH_RECOGNITION_API_KEY"
        text_recognized = r.recognize_google(audio,  language='th-TH')
        print("Google Speech Recognition >> you said >>" + text_recognized)
        text_recognized.strip()
        if ( "สวัสดี" in text_recognized ):
            playsound("./nictomeet.mp3")
        elif ( 'ชื่อ' in text_recognized ):
            playsound("./angus.mp3")  
        elif ( 'ข่าว' in text_recognized ):
            playsound("./covid.mp3") 
        elif ( 'เพลง' in text_recognized ):
            playsound("./unknown.mp3")   
        elif ( 'จบการทำงาน' in text_recognized ):
            break 
        else:
            playsound("./dontknow.mp3")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))



