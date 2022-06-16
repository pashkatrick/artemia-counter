import cv2
import numpy as np

img1 = cv2.imread('./images/img5.jpg', 1)
img = cv2.resize(img1, (1080, 810), interpolation=cv2.INTER_LINEAR)
cv2.imshow('img', img)
cv2.waitKey(0)

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

# Show result for testing:
cv2.imshow('img', roi)
cv2.waitKey(0)

# draw filled circle in white on black background as mask
mask = np.zeros_like(img)
mask = cv2.circle(mask, (xc,yc), radius, (255, 255, 255), -1)
result = cv2.bitwise_and(img, mask)

crop = result[yc-radius:yc+radius, xc-radius:xc+radius]

cv2.imshow('masked image', crop)
# cv2.imwrite('./img.png', crop)
cv2.waitKey(0)

# b, g, r = cv2.split(result)
# cv2.imshow('b', b)
# cv2.imshow('g', g)
# cv2.imshow('r', r)
# cv2.waitKey(0)

cv2.destroyAllWindows()
