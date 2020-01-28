#importing modules
import time as t
import cv2   
import numpy as np

#capturing video through webcam
#cap=cv2.VideoCapture(0)
ipwebcam_url = "http://192.168.225.125:8080/video"
#video_capture = cv2.VideoCapture("/home/user/Videos/V_20180104_095243.mp4")
cap = cv2.VideoCapture(ipwebcam_url)

while(1):
	_, img = cap.read()
	#img = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
	#converting frame(img i.e BGR) to HSV (hue-saturation-value)

	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	#definig the range of red color
	red_lower=np.array([136,87,111],np.uint8)
	red_upper=np.array([180,255,255],np.uint8)

	#finding the range of red color in the image
	red=cv2.inRange(hsv, red_lower, red_upper)
	
	#Morphological transformation, Dilation  	
	kernal = np.ones((5 ,5), "uint8")

	red=cv2.dilate(red, kernal)
	res=cv2.bitwise_and(img, img, mask = red)

	#Tracking the Red Color
	(_,contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area>400):
			
			x,y,w,h = cv2.boundingRect(contour)	
			img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
			cv2.putText(img,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))

	#cv2.imshow("Redcolour",red)
	cv2.imshow("Color Tracking",img)
	#cv2.imshow("red",res) 	
	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		cv2.destroyAllWindows()
		break  
          

    
