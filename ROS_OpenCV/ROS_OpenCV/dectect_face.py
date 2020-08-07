
import numpy as np
import cv2
import datetime
import os
import time
from PIL import ImageFont, ImageDraw, Image

# for more model ref to https://github.com/opencv/opencv_extra/blob/master/testdata/dnn/download_models.py

print("[INFO] loading face detector...")
protoPath = "./face_detection_model/deploy.prototxt"
modelPath = "./face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
detector = cv2.dnn.readNet(protoPath, modelPath)
b,g,r,a = 0,255,0,0
def facedetection(img):


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
            fontpath = "./THSarabun.ttf"   
            font = ImageFont.truetype(fontpath, 32)
            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            draw.text((50, 80),  "เหมือนจะเจอคนเลย", font = font, fill = (b, g, r, a))
            img = np.array(img_pil)
            #
            cv2.putText(img, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    cv2.imshow("Output", img)

   
 


if __name__ == '__main__':
    print('-------------------------------------------------------------------------------')	
    print(cv2.__version__)
    print('-------------------------------------------------------------------------------')
    cap = cv2.VideoCapture(0)
    print('In loop ....')
    while(1):
        ret, img = cap.read()
        if ret == True :
            print('Processing image frame')
            facedetection(img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

