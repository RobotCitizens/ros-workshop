#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Publish a captured image usb camera 0 as ROS messages.
"""


import numpy as np
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
bridge = CvBridge()
def main():
	# Set up node.
	rospy.init_node("usb_camera0_publisher", anonymous=True)
	img_pub = rospy.Publisher("/camera0/image_raw", Image, queue_size=10)
	rate = rospy.Rate(5)
	# Open video.
	video = cv2.VideoCapture(0)

	while not rospy.is_shutdown():
		message = "Capture image at %s" % rospy.get_time()
		rospy.loginfo(message)
		ret, img = video.read()
		#cv2.imshow('Frame',img)
		#cv2.waitKey(1)
		img_msg = bridge.cv2_to_imgmsg(img,"bgr8")
		img_msg.header.stamp = rospy.Time.now()
		img_pub.publish(img_msg)
		rate.sleep()

	print(" Cv2 Capture is done")
	video.release()
	cv2.destroyAllWindows()  
	    

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
