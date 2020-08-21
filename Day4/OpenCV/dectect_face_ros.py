import rospy
import numpy as np
import cv2
import datetime
import os
import time
from std_msgs.msg import String

from sensor_msgs.msg import Image

from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

# for more model ref to https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/download_models.py

print("[INFO] loading face detector...")
protoPath = "./face_detection_model/deploy.prototxt"
modelPath = "./face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
detector = cv2.dnn.readNet(protoPath, modelPath)

def callback_facedetection(Image):

	rospy.loginfo(rospy.get_caller_id()+" get image frame")
	img = bridge.imgmsg_to_cv2(Image, "bgr8")
	(h, w) = img.shape[:2]
	print("image size >> (%s,%s)"%(w,h))
	cv2.imshow("Input", img)
	cv2.waitKey(1)
	print("[INFO] computing object detections...")
	imageBlob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300),(104.0, 177.0, 123.0), swapRB=False, crop=False)
	detector.setInput(imageBlob)
	detections = detector.forward()

	face_count = 0
	for i in range(0, detections.shape[2]):

		# extract the confidence (i.e., probability) associated with the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections
		if confidence > 0.88:

			face_count = face_count+1

			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

			(startX, startY, endX, endY) = box.astype("int")

			text = "face-id"+str(face_count)+"> {:.2f}%".format(confidence * 100)

			y = startY - 10 if startY - 10 > 10 else startY + 10

			cv2.rectangle(img, (startX, startY), (endX, endY), (0, 0, 255), 2)
			cv2.putText(img, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
	
	cv2.imshow("Output", img)

	cv2.waitKey(1)
   
def listener():

	rospy.init_node('Image_listener', anonymous=True)
	rospy.Subscriber("/camera0/image_raw", Image, callback_facedetection)
	 # spin() simply keeps python from exiting until this node is stopped
	rospy.spin()
 


if __name__ == '__main__':
	print('-------------------------------------------------------------------------------')	
	print(cv2.__version__)
	print('-------------------------------------------------------------------------------')
	try:
		listener()
	except rospy.ROSInterruptException:
		pass


