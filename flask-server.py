from flask import Flask, Response, render_template, request, make_response, send_file
from picamera2.picamera2 import *
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

dir = "/home/pi/Desktop/Biomet/images/"

def gen_frames():
    global save
    
    while True:
        success, frame = camera.read()
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

@app.route('/page3')
def index3():
    return render_template('page3.html')

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