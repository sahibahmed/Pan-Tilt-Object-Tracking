from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)


#pan servo - channel 0, safe range: 0-180 degrees
kit.servo[0].angle = 90

#tilt servo - channel 1, safe range: 0-180 degrees
kit.servo[1].angle = 90