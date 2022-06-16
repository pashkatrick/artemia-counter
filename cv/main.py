import cv2
import numpy as np

### LOAD CAMERA
img1 = cv2.imread('./images/img5.jpg', 1)

### DETECT CIRCLES
img = cv2.resize(img1, (1080, 810), interpolation=cv2.INTER_LINEAR)
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

### REMOVE GLARE

imgHLS = cv2.cvtColor(crop, cv2.COLOR_BGR2HLS)
Lchannel = imgHLS[:, :, 1]

mask = cv2.inRange(Lchannel, 95, 255)
dst = cv2.bitwise_and(img, img, mask=mask)
bgr = cv2.cvtColor(dst, cv2.COLOR_HLS2BGR)
grayscale = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
binarized = np.where(grayscale > 0.1, 1, 0)

pro = morphology.remove_small_objects(binarized.astype(bool), min_size=20, connectivity=10).astype(int)
mask_x, mask_y = np.where(pro == 0)
dst[mask_x, mask_y, :3] = 0

gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

deglare = cv2.inpaint(img, mask, 25, cv2.INPAINT_TELEA)

### DETECT ARTEMIA

hsv = cv2.cvtColor(deglare, cv2.COLOR_BGR2HSV)
# (0, 43, 75), (34, 255, 255)
artemia = cv2.inRange(hsv, (0, 34, 60), (33, 255, 255))

back = img.copy()
back[artemia == 255] = (0, 255, 0)

back[artemia != 255] = (0, 0, 0)

kernel = np.ones((4, 4), np.uint8)
dil = cv2.dilate(back, kernel, iterations=1)

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

cv2.waitKey()