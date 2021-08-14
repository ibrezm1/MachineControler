import time
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import subprocess as s
import requests
from argparse import ArgumentParser
import os.path
import yaml
import logging
import sys

import signal
import sys

from operator import xor

def signal_handler(signal, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def url_to_image(url):
    resp = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    return image

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')  # return an open file handle


class Bot:
    def __init__(self, url,threshold):
        self.serverurl = url
        self.threshold = threshold

    def botObserve(self,region,image):
        self.region = region
        ex_x,ex_y,ex_w,ex_h = region
        img_rgb = url_to_image(f"{self.serverurl}/getimage?cx={ex_x}&cy={ex_y}&cw={ex_w}&ch={ex_h}")

        img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
        template = cv.imread(image,0)
        w, h = template.shape[::-1]
        self.res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(self.res)
        return max_val>=self.threshold


    def botNotify(self):
        requests.get(f"{self.serverurl}/play")

    def botAct(self):
        ex_x,ex_y,ex_w,ex_h = self.region
        loc = np.where( self.res >= self.threshold)
        for pt in zip(*loc[::-1]):
            rl_x, rl_y = ( pt[0] + int(w/2), pt[1] + int(h/2) )
            cx_x, cx_y = ex_x + rl_x,ex_y + rl_y
            cur_time = time.strftime("%m/%d/%Y, %H:%M:%S")
            print(f"Found OK {cx_x} {cx_y} at {cur_time}")
            requests.get(f"{self.serverurl}/mouse?cx={cx_x}&cy={cx_y}")

   

def main():
    parser = ArgumentParser(description="Config Selection")
    parser.add_argument("-f", dest="filename", required=True,
                        help="input file with config.yaml", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    args = parser.parse_args()
    config = args.filename.name
    
    with open(config, 'r') as f:
        conf = yaml.safe_load(f)

    bot1 = Bot(conf['server'], conf['threshold'])
    while True:
        for regions in conf['monitor']['points']:
            if not xor(regions['match']=='match' , bot1.botObserve(regions['region'],regions['matchimage'])):
                if regions['notify'] == 'true' : bot1.botNotify()   
                if regions['click'] == 'true' : bot1.botAct()                
        time.sleep(conf['delay'])

if __name__ == "__main__":
    main()

