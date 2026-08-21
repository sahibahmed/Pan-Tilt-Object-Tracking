import cv2
from picamera2 import Picamera2
import time
import numpy as np
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

pan_angle = 90
tilt_angle = 90

kit.servo[0].angle = pan_angle
kit.servo[1].angle = tilt_angle


picam2 = Picamera2()
preview_config = picam2.create_preview_configuration()  #store preview mode
picam2.configure(preview_config) #configure in preview mode (preview mode set)
picam2.start() #avoiding using showpreview=True as I am using SSH
time.sleep(1)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('Tracking_test.mp4', fourcc, 20.0, (640, 480))

start_time = time.time()


while True:
    array = picam2.capture_array("main") #capture in preview mode and store to array

    #Calculate frame center and center mark
    height = array.shape[0] # 480 height 
    width = array.shape[1] # 640 width

    center_x = int(width/2) 
    center_y = int(height/2)

    cv2.circle(array, (center_x, center_y), 4, (0, 0, 255), -1) #frame center in BLUE


    #Conversions
    array = cv2.cvtColor(array, cv2.COLOR_RGBA2BGR) #convert Picamera2 RGB to OpenCV BGR'
    hsv = cv2.cvtColor(array, cv2.COLOR_BGR2HSV) #convert to HSV format for color detection AND make a HSV copy of array 

    # standard value for detecting the color blue 
    lower_limit = np.array([100, 50, 50])
    upper_limit = np.array([130, 255, 255])

    #separates the blue object from everything else in frame 
    mask = cv2.inRange(hsv, lower_limit, upper_limit) #defined range for blue 

    #Uncomment to display only the detected blue object 
    #array = cv2.bitwise_and(array, array, mask=mask) 


    #finding all blue objects on frame using contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    print("Number of contours found = " + str(len(contours)))


    if len(contours) > 0: #conditional statemnet to prevent false boundaries
    
        #drawing boundary round the contours found (red color bounds)
        largest_contour = max(contours, key=cv2.contourArea)  # select the biggest contour
        x, y, w, h = cv2.boundingRect(largest_contour) #calculate the four corners of the rectangle
        cv2.rectangle(array, (x, y), (x+w, y+h), (0, 0, 255), 4) # draw RED ractangle using the four coordinates

        # determine the center of bounding rectangle
        object_center_x = int(x+w/2)
        object_center_y = int(y+h/2)

        #draw the center in RED
        cv2.circle(array, (object_center_x, object_center_y), 4, (0,0,255), -1)

        
        #identify how far off object center is from frame center
        horizontal_error = (object_center_x - center_x)
        dead_zone_x = 15

        if horizontal_error < -dead_zone_x:
            pan_angle += 3
        elif horizontal_error > dead_zone_x:
            pan_angle -= 3
        else: 
            print("Object is centered!")

        pan_angle = max(0, min(180, pan_angle)) #servo constraint
        kit.servo[0].angle = pan_angle
        

        vertical_error = (object_center_y - center_y)
        dead_zone_y = 15
        
        if vertical_error < -dead_zone_y:
            tilt_angle -= 3
        elif vertical_error > dead_zone_y:
            tilt_angle += 3
        else:
            print("Object is centered!")


        tilt_angle = max(0, min(180, tilt_angle))
        kit.servo[1].angle = tilt_angle




    video.write(array)

    #10 second video
    if time.time() - start_time > 10:
        break


video.release()
picam2.stop()