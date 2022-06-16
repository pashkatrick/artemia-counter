import cv2
import numpy as np


def thresh_demo(val):
    thresh1 = cv2.getTrackbarPos('thresh:', 'slider')
    thresh2 = cv2.getTrackbarPos('converted:', 'slider')
    dst = cv2.threshold(gray, thresh1, thresh2, cv2.THRESH_BINARY)[1]
    cv2.imshow('slider', dst)


img = cv2.imread('no-glare.png')

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# (0, 43, 75), (34, 255, 255)
artemia = cv2.inRange(hsv, (0, 34, 60), (33, 255, 255))

# hsv[:, :, 1] = artemia

# back = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

back = img.copy()
back[artemia == 255] = (0, 255, 0)

cv2.imshow('test', back)
cv2.waitKey(0)

back[artemia != 255] = (0, 0, 0)

cv2.imshow('only', back)
cv2.waitKey(0)

kernel = np.ones((4, 4), np.uint8)
dil = cv2.dilate(back, kernel, iterations=1)

cv2.imshow('dilate', dil)
cv2.waitKey(0)

gray = cv2.cvtColor(dil, cv2.COLOR_BGR2GRAY)
th, threshed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)

cv2.imshow('thr', threshed)
cv2.waitKey(0)

cnts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

s1 = 0
s2 = 50
xcnts = []
for cnt in cnts:
    if s1 < cv2.contourArea(cnt) < s2:
        xcnts.append(cnt)

print('Dots number: {}'.format(len(xcnts)))

# threshold grayscale image to extract glare

# cv2.namedWindow('slider')
#
# cv2.createTrackbar('thresh:', 'slider', 0, 255, thresh_demo)
# cv2.createTrackbar('converted:', 'slider', 0, 255, thresh_demo)

# mask2 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]
#
# cv2.imshow('masked image', mask2)

# thresh_demo(0)
cv2.waitKey()
