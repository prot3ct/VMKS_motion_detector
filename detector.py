from picamera.array import PiRGBArray
from picamera import PiCamera
from email_sender import send_email, TempImage
import argparse
import datetime
import time
import cv2

client = None

camera = PiCamera()
camera.resolution = tuple([640, 480])
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=tuple([640, 480]))

time.sleep(10)
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0

for f in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	frame = f.array
	timestamp = datetime.datetime.now()
	is_occupied = False

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, tuple([21, 21]), 0)

	if avg is None:
		print "Started up"
		avg = gray.copy().astype("float")
		rawCapture.truncate(0)
		continue

	for c in cnts:
            if cv2.contourArea(c) < 5000:
                continue

            is_occupied = True
	if is_occupied:
            cv2.imwrite("/tmp/talkingraspi_{}.jpg".format(motionCounter), frame);
            if (timestamp - lastUploaded).seconds >= 0.5:
                motionCounter += 1;
                if motionCounter >= 8:
                    print("Sending email")
                    send_email()
                    time.sleep(10)
                    print("Email sent.")
                    lastUploaded = timestamp
                    motionCounter = 0
	else:
	    motionCounter = 0
	
        rawCapture.truncate(0)
