import cv2

win_name = 'find'


def hsvimg(val):
    min_hue = cv2.getTrackbarPos('min_hue:', win_name)
    min_sat = cv2.getTrackbarPos('min_sat:', win_name)
    min_val = cv2.getTrackbarPos('min_val:', win_name)
    max_hue = cv2.getTrackbarPos('max_hue:', win_name)
    max_sat = cv2.getTrackbarPos('max_sat:', win_name)
    max_val = cv2.getTrackbarPos('max_val:', win_name)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    artemia = cv2.inRange(hsv,
                          (min_hue, min_sat, min_val),
                          (max_hue, max_sat, max_val))
    cv2.imshow(win_name, artemia)


img = cv2.imread('./no-glare.png')

cv2.namedWindow(win_name)
#cv2.resizeWindow(win_name, 540, 360)

cv2.createTrackbar('min_hue:', win_name, 0, 179, hsvimg)
cv2.createTrackbar('min_sat:', win_name, 0, 255, hsvimg)
cv2.createTrackbar('min_val:', win_name, 0, 255, hsvimg)
cv2.createTrackbar('max_hue:', win_name, 0, 179, hsvimg)
cv2.createTrackbar('max_sat:', win_name, 0, 255, hsvimg)
cv2.createTrackbar('max_val:', win_name, 0, 255, hsvimg)

hsvimg(0)
cv2.waitKey()

cv2.destroyAllWindows()
