from ctypes import Structure, windll, c_uint, sizeof, byref
from flask import Flask,request
from PIL import ImageGrab
import cv2
from numpy import array
import time
from flask import send_file
from waitress import serve

import logging
from logging.handlers import RotatingFileHandler

import winsound
import mouse
import sys

logger = logging.getLogger()
logging.basicConfig(
        handlers=[RotatingFileHandler('./logs/my_log.log', maxBytes=100000, backupCount=2)],
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')


app = Flask(__name__)
class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

@app.route("/idle")
def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return str(millis / 1000.0)


@app.route("/")
def helloworld():
    return "<p>Hello, World!</p>"

@app.route("/alive")
def alive():
    return "alive"

@app.route("/play")
def playworld():
    #https://voicemaker.in/
    winsound.PlaySound("Sounds/student-waiting.wav", winsound.SND_ALIAS | winsound.SND_ASYNC)
    return "<p>Hello, World!</p>"


@app.route("/mouse")
def mouseworld():
    bar = request.args.to_dict()
    _x,_y = (0,0)
    if len(bar)>=2:
        a = [int(v) for k,v in bar.items() if k[0]=='c']
        a = a[:2]
        _x,_y = a
    logger.debug(f"final sie: {a}")
    mouse.move(_x, _y, absolute=True, duration=0.1)
    mouse.click('left')
    return "<p>Hello, World!</p>"

@app.route("/getimage")
def GetScreeshot():
    bar = request.args.to_dict()
    
    if len(bar)>=4:
        a = [int(v) for k,v in bar.items() if k[0]=='c']
        a = a[:4]
        a = a[:2] + [x1+x2 for x1,x2 in zip(a[:2],a[2:])]
        box = tuple(a)
        logger.debug(f"final sie: {box}")
        #logger.info('o')
        #box= (1,1,100,100)
    else:
        box=None
    filepath = 'my_image.png'
    #(left_x, top_y, right_x, bottom_y)
    screenshot = ImageGrab.grab(bbox=box)
    screenshot.save(filepath, 'PNG')  # Equivalent to `screenshot.save(filepath, format='PNG')`
    return send_file(filepath, mimetype='image/png')   

@app.route("/site-map")
def site_map():
    return("site-map getimage mouse play alive")
    
# https://www.techcoil.com/blog/how-to-use-nssm-to-run-a-python-3-application-as-a-windows-service-in-its-own-python-3-virtual-environment/
serve(app, host='0.0.0.0', port=5000, threads=1) #WAITRESS!
