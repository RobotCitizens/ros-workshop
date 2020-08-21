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

print("[INFO] loading objects detector...")
protoPath = "./object_detection_model/MobileNetSSD_deploy.prototxt"
modelPath = "./object_detection_model/MobileNetSSD_deploy.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

ssd_classes = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

COLORS = np.random.uniform(0, 255, size=(len(ssd_classes), 3))

def callback_facedetection(Image):

	rospy.loginfo(rospy.get_caller_id()+" get image frame")
	img = bridge.imgmsg_to_cv2(Image, "bgr8")
	(h, w) = img.shape[:2]
	print("image size >> (%s,%s)"%(w,h))
	cv2.imshow("Input", img)
	cv2.waitKey(1)
	print("[INFO] computing object detections...")
	imageBlob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
	detector.setInput(imageBlob)
	detections = detector.forward()

	obj_count = 0
	for i in range(0, detections.shape[2]):

		# extract the confidence (i.e., probability) associated with the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections
		if confidence > 0.8:

			obj_count = obj_count+1
			class_id = detections[0 , 0, i, 1]
			print(class_id)
			class_name = ssd_classes[int(class_id)]

			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

			(startX, startY, endX, endY) = box.astype("int")

			text = "obj-id"+str(obj_count)+"> {:.2f}%".format(confidence * 100)
			text = text + "> %s"%(class_name)

			y = startY - 10 if startY - 10 > 10 else startY + 10

			cv2.rectangle(img, (startX, startY), (endX, endY), COLORS[int(class_id)], 2)
			cv2.putText(img, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, COLORS[int(class_id)], 2)
	
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


