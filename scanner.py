import cv2
import zbar.misc
import sys
import hashlib
from time import sleep
from datetime import datetime
from picamera import PiCamera
from PIL import Image
import numpy as np


def scan(file):
    #image = cv2.imread(file)
    image = np.array(Image.open(file).getdata())
    if len(image.shape) == 3:
        image = zbar.misc.rgb2gray(image)
    scanner = zbar.Scanner()
    results = scanner.scan(image)
    for result in results:
        if result.type == 'UPC-A':
            print(result.data, zbar.misc.upca_is_valid(result.data.decode('ascii')), result.quality, file)


if len(sys.argv) >= 2:
    for file in sys.argv:
        if "scanner.py" in file:
            continue
        print file
        scan(file)
else:

    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    # Camera warm-up time
    sleep(2)
    while True:
        sha256 = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
        out = '/tmp/picam/picam.' + sha256 + '.jpg'
        camera.capture(out)
        scan(out)
        sleep(1)