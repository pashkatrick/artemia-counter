from flask import Flask, Response, render_template, request, make_response, send_file
#from picamera2.picamera2 import *
from PRUEBA_IMPORT import matrix_motion
from time import sleep
import numpy as np
import cv2 as cv
import os, sys, time, datetime
import subprocess

app = Flask(__name__,
            static_url_path='',
            static_folder='./web/static',
            template_folder='./web/templates')

camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, 640) #2028
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 480) #1520
camera.set(cv.CAP_PROP_FPS, 30)

save = 0

dir = "/home/pi/Biomet/images/"

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

    # draw filled circle in white on black background as mask
    mask = np.zeros_like(img)
    mask = cv.circle(mask, (xc, yc), radius, (255, 255, 255), -1)
    result = cv.bitwise_and(img, mask)


    crop = result[yc - radius:yc + radius, xc - radius:xc + radius]

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
    global save
    
    while True:
        success, frame = camera.read()
        frame = cv.resize(frame, (640, 360), interpolation=cv.INTER_AREA)
        
        if success:
            
            #if (save):
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

@app.route('/requests', methods=['POST','GET'])
def tasks():
    if request.method == 'POST':
        if request.form.get('action') == 'Count':
            # do "pass" instead?
            return "204 - No content"
        elif request.form.get('action') == 'Save':
            print('works')
            global save
            save = 1
            print(save)
            return "204 - No content"
        #else: pass
    #elif request.method == 'GET':
    #    return render_template('index.html')
    
    return render_template('index.html') 

#@app.route('/image_result')
#def image_result():
#    # Look for a better method
#    return Response(last_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

def coords(row, clm):
    letters = ['A', 'B', 'C', 'D']
    rows = letters[0:row]
    newrow = [i+str(j) for i in rows for j in range(1,clm+1)]
    return newrow
        
@app.route('/page2')
def index2():
    global my_var
    global dim
    my_var = int(request.args.get('my_var', None))
    if my_var == 1:
        dim = coords(2,3)
    elif my_var == 2:
        dim = coords(3,4) 
    elif my_var == 3:
        dim = coords(4,6)
    else:
        dim = ['A1']
    return render_template('page2.html', dim=dim)

@app.route('/page3', methods=['GET', 'POST'])
def index3():
    if request.method == 'GET':
        return render_template('page3.html')
    else:
        if my_var == 1:
            y = 3
        elif my_var == 2:
            y = 4
        elif my_var == 3:
            y = 6
        bools = request.get_json(force=True)
        pre = [int(e) for e in bools]
        A = np.reshape(pre, (-1,y))
        B = np.flip(A, axis=1)
        C = np.transpose(B)
        D = C.flatten()
        images = matrix_motion(my_var,2,D,camera)
        
        # IMAGES NEED TO MATCH LOCATIONS
        
        counts = []
        # use [A1, A2, ] matrix thing here
        for img in images:
            if img is not None:
                counts.append(count(img))
            else:
                counts.append(None)
        
        return render_template('page3.html', D=D, counts=counts, dim=dim)

@app.route('/test')
def test():
    global camera
    print('releasing camera')
    camera.release()
    cv.destroyAllWindows()
    print('works')
    fileName = "./img11.jpg"
    cmd = "raspistill -o " + fileName
    subprocess.call(cmd, shell=True)
    print('saving')
    sleep(4)
    print('saved')
    return "204 - No content"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)