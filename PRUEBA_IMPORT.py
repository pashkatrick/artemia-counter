from OBJETO_ARTEMIAS import motor    
from time import sleep
import cv2 as cv
import numpy as np
import time

camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, 640) #2028
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 480) #1520
camera.set(cv.CAP_PROP_FPS, 30)

save = 0
art_num = 0
art = []

#def capture():
#    if camera.isOpened():
#        ret, img = camera.read()
#        if ret:
#            cv.imwrite('./images/img', img)
#            return img

def count(img):

    # Find circle
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    blurred = cv.medianBlur(gray, 25)  # cv2.bilateralFilter(gray,10,50,50)

    # these work for 640 x 360
    minDist = 100
    param1 = 50
    param2 = 30     # smaller value -> more false circles
    minRadius = 120
    maxRadius = 300

    # docstring of HoughCircles: HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) -> circles
    circles = cv.HoughCircles(blurred, cv.HOUGH_GRADIENT, 1, minDist, param1=param1, param2=param2,
                               minRadius=minRadius, maxRadius=maxRadius)

    xc = 0
    yc = 0
    radius = 0

    roi = img.copy()

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            cv.circle(roi, (i[0], i[1]), i[2], (0, 255, 0), 2)
            xc = i[0]
            yc = i[1]
            radius = round(i[2] * 0.98)
    else:
        return 0

    # draw filled circle in white on black background as mask
    mask = np.zeros_like(img)
    mask = cv.circle(mask, (xc, yc), radius, (255, 255, 255), -1)
    result = cv.bitwise_and(img, mask)

    if yc - radius < 0 or 360 < yc + radius:
        return 0
    if xc - radius < 0 or 640 < xc + radius:
        return 0
    crop = result[yc - radius:yc + radius, xc - radius:xc + radius]

    # MAKE CASE FOR WHEN CIRCLE IS NOT DETECTED

    hsv = cv.cvtColor(crop, cv.COLOR_BGR2HSV)
    # (0, 43, 75), (34, 255, 255)
    artemia = cv.inRange(hsv, (0, 37, 75), (54, 255, 161))

    back = crop.copy()
    back[artemia == 255] = (0, 255, 0)

    back[artemia != 255] = (0, 0, 0)

    kernel = np.ones((4, 4), np.uint8)
    dil = cv.dilate(back, kernel, iterations=1)

    gray2 = cv.cvtColor(dil, cv.COLOR_BGR2GRAY)
    th, threshed = cv.threshold(gray2, 0, 255, cv.THRESH_BINARY)

    cnts = cv.findContours(threshed, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)[-2]

    s1 = 40
    s2 = 200   # 100 x 100 for (1920 x 1080)
    xcnts = []
    for cnt in cnts:
        # if s1 < cv2.contourArea(cnt) < s2:
        area = cv.contourArea(cnt)
        peri = cv.arcLength(cnt, True)
        circularity = 4 * np.pi * (area / peri**2)
        if 0.7 < circularity < 1:
            if s1 < cv.contourArea(cnt) < s2:
                xcnts.append(cnt)

    return len(xcnts)

def gen_frames():
    global art_num
    global art
    global save
    
    while True:
        success, frame = camera.read()
        frame = cv.resize(frame, (640, 360), interpolation=cv.INTER_AREA)
        
        if success:
            
            if (save):
                # cv.imwrite('./test_final_2.jpg', frame)
                art_num = count(frame)
                art.append(art_num)
                
                save = 0
            #    save = 0
            #    fileName = "img11.jpg"
            #    cmd = "raspistill -o " + fileName
            #    subprocess.call(cmd, shell=True)
            #    print('saving')
            #    sleep(4)
            #    print('saved')
            
            try:
                ret, buffer = cv.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
        else:
            pass

def matrix_motion (tipo_pozo,tiempo_foto,check_pozo):
    global save
    global art_num
    global art
    # check_pozo:
    # array de bools de los pozos
    # 0: no seleccionado (no se toma foto)
    # 1: seleccionado (sí se toma foto)
    
    mot_y = motor(19,26,17,3200,0)
    mot_x = motor(12,21,23,3200,1)
    
    mot_x.set_vel_max(2)
    mot_x.set_acel(15)
    mot_x.set_rango(0,11.8)
    mot_y.set_vel_max(2)
    mot_y.set_acel(15)
    mot_y.set_rango(-10.5,0)
    
    # dis_init_x: posición inicial del PRIMER POZO
    
    if tipo_pozo == 1:
        dis_init_x = 1.75
        dis_init_y = -1
        num_x = 2
        num_y = 3
        dist_pozos = 3.75
    elif tipo_pozo == 2:
        dis_init_x = 0.5
        dis_init_y = -0.3
        num_x = 4
        num_y = 6
        dist_pozos = 1.93
    elif tipo_pozo == 3:
        dis_init_x = 0.75
        dis_init_y = -0.3 #-0.275?
        num_x = 4
        num_y = 6
        dist_pozos = 1.93


    mot_x.set_motor()
    mot_y.set_motor()

    
    """
    
    mot_x.run_distance(5)
    mot_x.run_distance(10)
    mot_x.run_distance(1)
    mot_x.run_position(2)
    
    mot_y.run_distance(-5)
    mot_y.run_distance(7)
    mot_y.run_distance(-1)
    mot_y.run_position(-2)
    """
    #mot_x.run_distance(dis_init_x)
    #mot_y.run_distance(dis_init_y)
    
    i = 0
    j = 0
    
    # images = [None] * (num_x * num_y)
    
    while j < num_y:
        mot_y.run_position(-j*dist_pozos + dis_init_y)
        
        while i < num_x:
            # (i+1)-1=i so it starts in 0
            if check_pozo[num_x*(j)+i] == True:
                mot_x.run_position(i*dist_pozos + dis_init_x)
                
                # viewed from the front
                # yellow strip looking north
                # from top to botoom, left to right (no U shape)
                # in normal coords (3x4):
                # A4, B4, C4, A3, B3, C3, A2, etc
                # i+1: column
                # j+1: row
                print("tomando foto: ",i+1," ",j+1)
                
                # cmd: take picture
                # success, frame = cam.read()
                # images[num_x*(j)+i] = frame
                #image_1 = capture()
                #count_1 = count(image_1)
                
                # to avoid motion blur and let the camera locate properly
                time.sleep(0.5)
                save = 1
                
                #print('Artemias: ', count_1)
                #cv.imwrite('./images/final_test.jpg')
                
                time.sleep(tiempo_foto)
            
            # else:
                # images[num_x*(j)+i] = None
            
            i = i + 1
        
        j = j + 1
        i = 0
    
    mot_x.set_motor()
    mot_y.set_motor()
    
    return art

#matrix = [1,0,0,0,0,0] 
#matrix_motion(1,5,matrix)