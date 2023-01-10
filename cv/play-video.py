import cv2 as cv2
import time

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

#HIGH_VALUE = 10000

# (Of cause, I tried to set manually all resolutions in next two lines)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, HIGH_VALUE)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HIGH_VALUE)

cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))

# 4:3 ratio
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) #2028 #640 #480
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) #1520 #480 #272
cap.set(cv2.CAP_PROP_FPS, 30)

#width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#print(f"Camera resolution: {width}x{height}") # prints 4056x3040

dim = (640, 360)

while True:
    ret, frame = cap.read()

    if not ret:
        # Here it exit if resolution is 2560x1680 and above
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()