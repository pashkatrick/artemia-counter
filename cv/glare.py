import cv2
import numpy as np
from skimage import morphology

img = cv2.imread('img.png')

imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
Lchannel = imgHLS[:, :, 1]

mask = cv2.inRange(Lchannel, 95, 255)
dst = cv2.bitwise_and(img, img, mask=mask)
bgr = cv2.cvtColor(dst, cv2.COLOR_HLS2BGR)
grayscale = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
binarized = np.where(grayscale > 0.1, 1, 0)

cv2.imshow('hsl', dst)
cv2.waitKey(0)

cv2.imshow('gray', grayscale)
cv2.waitKey(0)

pro = morphology.remove_small_objects(binarized.astype(bool), min_size=20, connectivity=10).astype(int)
mask_x, mask_y = np.where(pro == 0)
dst[mask_x, mask_y, :3] = 0

cv2.imshow('after', dst)
cv2.waitKey(0)

gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

cv2.imshow('mask', mask)
cv2.waitKey(0)

deglare = cv2.inpaint(img, mask, 25, cv2.INPAINT_TELEA)

cv2.imshow('deglare', deglare)
# cv2.imwrite('./no-glare.png', deglare)
cv2.waitKey(0)

cv2.destroyAllWindows()
