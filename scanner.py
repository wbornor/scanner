import zbar.misc
import sys, os
import hashlib
from time import sleep
from datetime import datetime
from picamera import PiCamera
import RPi.GPIO as GPIO
from PIL import Image
import numpy as np

__last_seen_seconds__ = 30


def ledon():
    # On
    GPIO.output(16, GPIO.LOW)


def ledoff():
    # On
    GPIO.output(16, GPIO.HIGH)


def scan(image):
    image = zbar.misc.rgb2gray(image)
    scanner = zbar.Scanner()
    results = scanner.scan(image)
    if(len(results) == 0):
        ledoff()
        return None
    for result in results:
        if result.type == 'UPC-A':
            print(result.data, zbar.misc.upca_is_valid(result.data.decode('ascii')), result.quality)
            ledon()
            return result.data.decode('ascii')

def publish(upc):
    print "*** publish " + upc

def main():
    # set up GPIO output channel
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    codes = {}

    if len(sys.argv) >= 2:
        for file in sys.argv:
            if "scanner.py" in file:
                continue
            imagefile = Image.open(file)
            print('opening file')
            data = imagefile.getdata()
            print('building numpy array')
            image = np.array(data, np.uint8)
            print('reshaping ')
            image = image.reshape(imagefile.size[1], imagefile.size[0], 3)
            scan(image)
    else:
        camera = PiCamera()
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        while True:
            #sha256 = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
            stream = np.empty((240, 320, 3), dtype=np.uint8)
            camera.capture(stream, format='rgb', resize=(320,240))
            upc = scan(stream)
            if upc is not None:
                if codes.has_key(upc):
                    #subtract the time, if more than n seconds since last seen, act again
                    now = datetime.now()
                    then = codes[upc]
                    if (now - then).total_seconds() >= __last_seen_seconds__:
                        publish(upc)
                else:
                    codes[upc] = datetime.now()
                    publish(upc)


if __name__ == '__main__':
    main()
