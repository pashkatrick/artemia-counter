from picamera2.picamera2 import *
import cv2
import numpy as np
import time

def count():
    
    # Take 4k image
    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL)

    preview_config = picam2.preview_configuration()
    capture_config = picam2.still_configuration({"size": (4032, 3024)})
    picam2.configure(preview_config)

    picam2.start()
    time.sleep(2)

    picam2.switch_mode(capture_config)
    time.sleep(2)

    img = picam2.capture_array()
    
    # Find circle
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.medianBlur(gray, 25) #cv2.bilateralFilter(gray,10,50,50)

    minDist = 200
    param1 = 30 #500
    param2 = 50 #200 #smaller value-> more false circles
    minRadius = 5
    maxRadius = 200 #10

    # docstring of HoughCircles: HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) -> circles
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

    xc = 0
    yc = 0
    radius = 0

    roi = img.copy()

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            cv2.circle(roi, (i[0], i[1]), i[2], (0, 255, 0), 2)
            xc = i[0]
            yc = i[1]
            radius = round(i[2]*0.98)

    # draw filled circle in white on black background as mask
    mask = np.zeros_like(img)
    mask = cv2.circle(mask, (xc,yc), radius, (255, 255, 255), -1)
    result = cv2.bitwise_and(img, mask)

    crop = result[yc-radius:yc+radius, xc-radius:xc+radius]

    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    # (0, 43, 75), (34, 255, 255)
    artemia = cv2.inRange(hsv, (0, 34, 60), (33, 255, 255))

    back = crop.copy()
    back[artemia == 255] = (0, 255, 0)

    back[artemia != 255] = (0, 0, 0)

    kernel = np.ones((4, 4), np.uint8)
    dil = cv2.dilate(back, kernel, iterations=1)

    gray2 = cv2.cvtColor(dil, cv2.COLOR_BGR2GRAY)
    th, threshed = cv2.threshold(gray2, 0, 255, cv2.THRESH_BINARY)

    cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

    s1 = 0
    s2 = 50
    xcnts = []
    for cnt in cnts:
        if s1 < cv2.contourArea(cnt) < s2:
            xcnts.append(cnt)

    print('Dots number: {}'.format(len(xcnts)))
    
    cv2.imwrite('full_res.jpg', np_array)
