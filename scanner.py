#!/usr/bin/python3

import zbar.misc
import sys, json
from time import sleep
from datetime import datetime
from picamera import PiCamera
import RPi.GPIO as GPIO
from PIL import Image
import numpy as np
import boto3

__last_seen_seconds__ = 30
__sns_topic_arn__ = 'arn:aws:sns:us-east-1:796019718156:upc-capture'


def ledon():
    # On
    GPIO.output(16, GPIO.LOW)


def ledoff():
    # On
    GPIO.output(16, GPIO.HIGH)


def chirp():
    GPIO.output(22, GPIO.HIGH)
    sleep(0.2)
    GPIO.output(22, GPIO.LOW)


def scan(image):
    image = zbar.misc.rgb2gray(image)
    scanner = zbar.Scanner()
    results = scanner.scan(image)
    if len(results) == 0:
        ledoff()
        return None
    for result in results:
        if result.type == 'UPC-A':
            upca = result.data.decode('ascii')
            print(result.data, zbar.misc.upca_is_valid(upca), result.quality)
            ledon()
            return upca


def publish(upc):
    msg = {'upc_a': upc}
    msg = json.dumps({"default": json.dumps(msg)})
    print("publish: " + msg)
    client = boto3.Session(profile_name='default').client('sns')

    response = client.publish(
        TopicArn=__sns_topic_arn__,
        Message=msg,
        Subject='upc-capture',
        MessageStructure='json'
    )
    print('publish response: ' + str(response))


def main():
    # set up GPIO output channel
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
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
            upc = scan(image)
            if upc is not None:
                publish(upc)
    else:
        camera = PiCamera()
        camera.resolution = (1024, 768)
        camera.color_effects = (128, 128)  # turn camera to black and white
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        while True:
            # sha256 = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
            stream = np.empty((240, 320, 3), dtype=np.uint8)
            camera.capture(stream, format='rgb', resize=(320, 240))
            upc = scan(stream)
            if upc is not None:
                if upc in codes:
                    # subtract the time, if more than n seconds since last seen time, publish again
                    now = datetime.now()
                    then = codes[upc]
                    if (now - then).total_seconds() >= __last_seen_seconds__:
                        codes[upc] = now
                        publish(upc)
                else:
                    codes[upc] = datetime.now()
                    publish(upc)


if __name__ == '__main__':
    main()
