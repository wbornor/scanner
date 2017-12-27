import zbar.misc
import sys, os
import hashlib
from time import sleep
from datetime import datetime
from picamera import PiCamera
from PIL import Image
import numpy as np

tmpdir = '/tmp/picam'

def scan(file):
    imagefile = Image.open(file)
    print('opening ' + file)
    image = np.array(imagefile.getdata(), np.uint8).reshape(imagefile.size[1], imagefile.size[0], 3)
    print('prepping ' + file)
    if len(image.shape) == 3:
        image = zbar.misc.rgb2gray(image)
    	print('grayscale ' + file)
    scanner = zbar.Scanner()
    results = scanner.scan(image)
print('count of results: ' + len(results))
    for result in results:
        if result.type == 'UPC-A':
            print(result.data, zbar.misc.upca_is_valid(result.data.decode('ascii')), result.quality, file)


def main():
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    if len(sys.argv) >= 2:
        for file in sys.argv:
            if "scanner.py" in file:
                continue
            print(file)
            scan(file)
    else:
        camera = PiCamera()
        camera.resolution = (1024, 768)
        camera.start_preview()
        # Camera warm-up time
        sleep(2)
        while True:
            sha256 = hashlib.sha256(str(datetime.now()).encode('utf-8')).hexdigest()
            out = tmpdir + '/picam.' + sha256 + '.jpg'
            print('capturing...')
            camera.capture(out)
            scan(out)


if __name__ == '__main__':
    main()
