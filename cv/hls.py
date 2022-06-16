import cv2

title_window = 'hsl'


def on_trackbar(val):
    imgHLS = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
    Lchannel = imgHLS[:, :, 1]
    mask = cv2.inRange(Lchannel, val, 255)
    res = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow(title_window, res)


img = cv2.imread('img.png')

cv2.namedWindow(title_window)

trackbar_name = 'hsl:'
cv2.createTrackbar(trackbar_name, title_window, 0, 255, on_trackbar)

on_trackbar(0)

cv2.waitKey(0)
cv2.destroyAllWindows()
