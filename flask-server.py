from flask import Flask, Response, render_template, request, make_response, send_file
from picamera2.picamera2 import *
import numpy as np
import cv2 as cv
import os, sys, time, datetime

app = Flask(__name__,
            static_url_path='',
            static_folder='./web/static',
            template_folder='./web/templates')

camera = cv.VideoCapture(0)
camera.set(cv.CAP_PROP_FRAME_WIDTH, 640) #2028
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 480) #1520
camera.set(cv.CAP_PROP_FPS, 30)

def last_frame():
    success, frame = camera.read()
    #if success:
        # PREPROCESSING GOES HERE
        # NEEDS TO TURN IMAGE AND NUMBER
        #frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        #frame = cv.bitwise_not(frame)
        #pass
    #else:
        # TODO: What does it return if camera fails?
        #pass
    
    ret, buffer = cv.imencode('.jpg', frame)
    frame = buffer.tobytes()
    #return frame
    return (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def gen_frames():
    while True:
        success, frame = camera.read()
        if success:
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
        if request.form.get('count') == 'Count':
            return "204 - No content"
        if request.form.get('save') == 'Save':
            return "204 - No content"
    return render_template('index.html') 

@app.route('/image_result')
def image_result():
    # Look for a better method
    return Response(last_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)