#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import rospy
from std_msgs.msg import String

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + " I will go to %s", data.data)
    
def listener():
 
	rospy.init_node('Speechlistener', anonymous=True) 
	rospy.Subscriber("TalktoROS", String, callback)
	  
	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
	  
if __name__ == '__main__':
	 listener()

