#!/usr/bin/python3

# Capture a JPEG while still running in the preview mode.

from picamera2.picamera2 import *
import cv2
import time

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)

preview_config = picam2.preview_configuration()
capture_config = picam2.still_configuration({"size": (4032, 3024)})
picam2.configure(preview_config)

picam2.start()
time.sleep(20)

picam2.switch_mode(capture_config)
time.sleep(2)

np_array = picam2.capture_array()
cv2.imwrite('full_res.jpg', np_array)