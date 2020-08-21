#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import speech_recognition as sr
from playsound import playsound
import rospy
from std_msgs.msg import String

# Record Audio
r = sr.Recognizer()
m = sr.Microphone()

pub = rospy.Publisher('TalktoROS', String, queue_size=10)
rospy.init_node('SpeechTalker', anonymous=True)
rate = rospy.Rate(1) # 1hz

#set threhold level
print(' Quiet Please ')
with m as source: r.adjust_for_ambient_noise(source)
print("Set minimum energy threshold to {}".format(r.energy_threshold))

# Speech recognition using Google Speech Recognition
while (True):
    playsound("./location.mp3")
    playsound("./signal.mp3")
    print("Say something!")
    with sr.Microphone() as source:
        audio = r.listen(source, phrase_time_limit=3)
        playsound("./signal.mp3")
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        text_recognized = r.recognize_google(audio,  language='th-TH')
        print("Google Speech Recognition >> you said >>  " + text_recognized)
        if ( 'สวัสดี' in text_recognized ):
            playsound("./nictomeet.mp3")
        elif ( 'ชื่อ' in text_recognized ):
            playsound("./angus.mp3")  
        elif ( 'ข่าว' in text_recognized ):
            playsound("./covid.mp3") 
        elif ( 'ห้องรับแขก' in text_recognized ):
            playsound("./ok.mp3") 
            playsound("./rooma.mp3")   
            hello_str = 'ROOM A'
            break
        elif ( 'ห้องครัว' in text_recognized ):
            playsound("./ok.mp3") 
            playsound("./roomb.mp3")   
            hello_str = 'ROOM B'
            break
        elif ( 'ห้องนอน' in text_recognized ):
            playsound("./ok.mp3") 
            playsound("./roomc.mp3") 
            hello_str = 'ROOM C'
            break
        else:
            playsound("./dontknow.mp3")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        
print('Publish Location !')

while not rospy.is_shutdown():
    rospy.loginfo(hello_str)
    pub.publish(hello_str)
    rate.sleep()

