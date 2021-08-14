# TODO :
# Setup venv : https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/
# Get image png :  http://192.168.1.13:5000/getimage?cx=1147&cy=31&ch=35&cw=35
# Scan Notification  :
# Above threshhold
# Notify : https://askubuntu.com/questions/616985/how-do-i-send-desktop-notifications-using-python-3
import time
import urllib.request
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import subprocess as s
import requests
from argparse import ArgumentParser
import os.path
import yaml

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    # https://stackoverflow.com/questions/57539233/how-to-open-an-image-from-an-url-with-opencv-using-requests-from-python
    resp = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    return image

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle



def main():
    parser = ArgumentParser(description="Config Selection")
    parser.add_argument("-f", dest="filename", required=True,
                        help="input file with config.yaml", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    config = args.filename
    with open(config, 'r') as f:
        doc = yaml.safe_load(f)

    while True:
        #urllib.request.urlretrieve(f"http://192.168.1.13:5000/getimage?cx=1147&cy=31&ch=35&cw=35", 'images/notify.png')
        #img_rgb = cv.imread('images/notify.png')
        ex_x,ex_y,ex_w,ex_h = (761,253,216,114)

        img_rgb = url_to_image(f"http://192.168.1.13:5000/getimage?cx={ex_x}&cy={ex_y}&cw={ex_w}&ch={ex_h}")

        # img_rgb = cv.imread('images/bell-nonotify.png')
        # img_rgb = cv.imread('images/bell-notify.png')
        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread('images/notify-red.png',0)
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        threshold = 0.8

        # verdict = 'found' if max_val>=threshold else 'not found'
        # print(verdict)

        # x = urllib.request.urlopen('http://192.168.1.13:5000/play')
        # print(x.read())

        if max_val>=threshold:
            s.call(['notify-send','foo','bar'])
            urllib.request.urlopen('http://192.168.1.13:5000/play')
        time.sleep(3)
        # loc = np.where( res >= threshold)
        # points = zip(*loc[::-1])
        # for pt in zip(*loc[::-1]):
        #     cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (255,0,0), 2)
        # cv.imwrite('res.png',img_rgb)
        # cv.imshow('final',img_rgb)

        # cv.waitKey(0) 
        
        # #closing all open windows 
        # cv.destroyAllWindows() 

if __name__ == "__main__":
    main()