import numpy as np
import cv2
import serial
import struct

#Serial object for communication with Arduino
ser = serial.Serial('COM5',9600)

#Capture from external USB webcam instead of the in-built webcam (shitty quality)
cap = cv2.VideoCapture(1)


#kernel window for morphological operations
kernel = np.ones((5,5),np.uint8)

#resize the capture window to 640 x 480
ret = cap.set(3,640)
ret = cap.set(4,480)

#upper and lower limits for the color yellow in HSV color space


    

lower_yellow = np.array([20,100,100]) 
upper_yellow = np.array([30,255,255])
lower_orange= np.array([3,100,100])
upper_orange= np.array([13,255,255])
lower_RED = np.array([132,100,100])
upper_RED = np.array([264,255,255])

couleur = ser.readline()




h=True
#begin capture

while(True):
    ret, frame1 = cap.read()

    #Smooth the frame
    #frame = cv2.GaussianBlur(frame,(11,11),0)
    frame = cv2.flip(frame1,1)
   

    #Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #Mask to extract just the yellow pixels
    mask = cv2.inRange(hsv,lower_orange,upper_orange)

    #morphological opening
    mask = cv2.erode(mask,kernel,iterations=2)
    mask = cv2.dilate(mask,kernel,iterations=2)

    #morphological closing
    mask = cv2.dilate(mask,kernel,iterations=2)
    mask = cv2.erode(mask,kernel,iterations=2)

    #Detect contours from the mask
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)[-2]

    if(len(cnts) > 0):
        #Contour with greatest area
        c = max(cnts,key=cv2.contourArea)
        #Radius and center pixel coordinate of the largest contour
        circles = [cv2.minEnclosingCircle(c) for c in cnts]
        for (x,y),radius in circles :

            if radius > 5:
            #Draw an enclosing circle
                cv2.circle(frame,(int(x), int(y)), int(radius),(0, 255, 255), 2)

            #Draw a line from the center of the frame to the center of the contour
                cv2.line(frame,(320,240),(int(x), int(y)),(0, 0, 255), 1)
            #Reference line
                cv2.line(frame,(320,0),(320,480),(0,255,0),1)

            radius = int(radius)
            

            #distance of the 'x' coordinate from the center of the frame
            #wdith of frame is 640, hence 320
            length = ((640/2)-(int(x)))



            
            if length>=0.9:
                a='S'
                ser.write(a.encode())
            
        

    #display the image
    cv2.imshow('frame',frame)
   
    #Mask image
    cv2.imshow('mask',mask)
    #Quit if user presses 'q'
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

#Release the capture
cap.release()
cv2.destroyAllWindows()

