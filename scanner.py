import zbar.misc
import sys, os
import hashlib
from time import sleep
from datetime import datetime
from picamera import PiCamera
from PIL import Image
import numpy as np

tmpdir = '/tmp/picam'


def scan(image):
    image = zbar.misc.rgb2gray(image)
    scanner = zbar.Scanner()
    results = scanner.scan(image)
    print('count of results: ' + str(len(results)))
    for result in results:
        if result.type == 'UPC-A':
            print(result.data, zbar.misc.upca_is_valid(result.data.decode('ascii')), result.quality)


def main():
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

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
            sha256 = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
            #out = tmpdir + '/picam.' + sha256 + '.jpg'
            print('capturing...')
            stream = np.empty((240, 320, 3), dtype=np.uint8)
            camera.capture(stream, format='rgb', resize=(320,240))
            scan(stream)


if __name__ == '__main__':
    main()
