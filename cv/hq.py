from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (4056, 3040)
sleep(5)
camera.capture('/home/pi/Desktop/Biomet/cv/test1.jpg')