"""Source: Murtaza's Workshop -Robotics and AI
Real time Shape Detection using Contours [9] | OpenCV Python Tutorials for Beginners 2020

Source: Pysource - Simple Color recognition with Opencv and Python

"""


import cv2
import numpy as np
import pyttsx3
import time

#CREATES VIDEO
width = 640
height = 480

capture = cv2.VideoCapture(-1)
capture.set(3, width)
capture.set(4, height)

#INITIALIZES TEXT TO SPEECH WHICH SAYS THE SHAPE AND COLOR OF THE OBJECT

def say_object(first_string_to_say, second_string_to_say):
    speech = pyttsx3.init()
    speech.say(first_string_to_say)
    speech.say(second_string_to_say)
    speech.runAndWait()



frame_hsv = np.zeros((250, 500, 3), np.uint8)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
#cv2.createTrackbar("Threshold1","Parameters",23,255,empty)
#cv2.createTrackbar("Threshold2","Parameters",20,255,empty)

#TESTING PURPOSES. CAN COMPARE MULTIPLE VIDEOS IN ONE 
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

#FINDS CONTOUR OF SHAPE
def getContours(img,imgContour):
    shape ="Undefined"
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 2500:
            cv2.drawContours(imgContour, contour, -1, (255,0,255),7)
            perimeter = cv2.arcLength(contour,True)
            approx = cv2.approxPolyDP(contour, 0.02*perimeter, True)
            print(len(approx))
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),5)
            if len(approx) >= 6:
                shape = "Circle"
                cv2.putText(imgContour, shape, (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
            elif len(approx) == 3:
                shape = "Triangle"
                cv2.putText(imgContour, shape, (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
            elif len(approx) == 4:
                shape = "Quadrilateral"
                cv2.putText(imgContour, shape, (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)
            elif len(approx) == 5:
                shape = "Pentagon"
                cv2.putText(imgContour, shape, (x+w+20, y+20), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,255,0),2)  
    return shape
#SHOW VIDEO WITH CODE
timer = 100
while True:
    time.sleep(0.01)
    success, img = capture.read()
    imgContour = img.copy()
    blur = cv2.GaussianBlur(img,(7,7),1)
    gray = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY)

    #threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    #threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(gray,23,20)
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=0)

    getContours(imgDil,imgContour)
    
    imgStack = stackImages(0.8,([imgContour]))
    cv2.imshow("Result",imgStack)
    
    
    #COLOR CODE
    _, img = capture.read()
    hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    height, width, _ = img.shape
    
    cx = int(width / 2)
    cy = int(height / 2)
    
    #Pixel Value For Color Detection
    pixel_center = hsv_img[cy,cx]
    hue_value = pixel_center[0]
    
    #SHOWS COLOR ON VIDEO SCREEN
    color = 'Undefined'
    if hue_value <5:
        color = "RED"
    elif hue_value <22:
        color = 'ORANGE'
    elif hue_value < 33:
        color = 'YELLOW'
    elif hue_value < 78:
        color = 'GREEN'
    elif hue_value <131:
        color = 'BLUE'
    elif hue_value < 170:
        color = 'VIOLET'
    else:
        color = 'RED'
    
    print(pixel_center)
    
    pixel_center_bgr = img[cy,cx]
    b, g, r = int(pixel_center_bgr[0]), int(pixel_center_bgr[1]), int(pixel_center_bgr[2])
    cv2.putText(img, color, (10,70), 0, 1.5, (b,g,r),2)
    cv2.circle(img, (cx,cy),5, (25,25,25),3)
    
    cv2.imshow('img', img)
    
    
    #SAYS CODE EVERY TIME THE TIMER REACHES 0
    if timer == 0:
        shape = getContours(imgDil,imgContour)
        say_object(shape, color)
        timer = 100
    timer -= 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
