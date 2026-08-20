#GOAL
#To detect an colored object

import cv2
from picamera2 import Picamera2
import time
import numpy as np
#from adafruit_servokit import ServoKit

"""
kit = ServoKit(channels=16)

pan_angle = 90
tilt_angle = 90

kit.servo[0].angle = pan_angle
kit.servo[1].angle = tilt_angle
"""

picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()  #store preview mode
picam2.configure(preview_config) #configure in preview mode (preview mode set)
picam2.start() #avoiding using showpreview=True as I am using SSH

time.sleep(1)
array = picam2.capture_array("main") #capture in preview mode and store to array

array = cv2.cvtColor(array, cv2.COLOR_RGBA2BGR) #convert Picamera2 RGB to OpenCV BGR'
array = cv2.cvtColor(array, cv2.COLOR_BGR2HSV) #convert to HSV format for color detection

# standard value for detecting the color blue 
lower_limit = np.array([100, 50, 50])
upper_limit = np.array([130, 255, 255])

mask = cv2.inRange(array, lower_limit, upper_limit) #defined range for blue 

array = cv2.bitwise_and(array, array, mask=mask) #only 



"""
print(type(array))
print(array.shape) # printed results : (480, 640, 4) 
"""

height = array.shape[0] # 480 height 
width = array.shape[1] # 640 width

center_x = int(width/2) 
center_y = int(height/2)

"""
print(center_x)
print(center_y)
"""

cv2.circle(array, (center_x, center_y), 4, (0,0,255), -1)


cv2.imwrite("camera_frame.jpg", array) #create image file to view the captured image

picam2.stop()


