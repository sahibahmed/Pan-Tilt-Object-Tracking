#GOAL
#To capture image usng Pi Camera and store it in array

import cv2
from picamera2 import Picamera2
import time
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

print(type(array))
print(array.shape) 

picam2.capture_file("camera_frame.jpg") #create image file to view the captured image

picam2.stop()


