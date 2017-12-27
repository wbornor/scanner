import cv2
import zbar.misc
import sys

if len(sys.argv) < 2:
    print 'usage: scanner <file>'

for file in sys.argv:
    if "scanner.py" in file:
        continue

    image = cv2.imread(file)
    print(type(image))
    if len(image.shape) == 3:
        image = zbar.misc.rgb2gray(image)
    scanner = zbar.Scanner()
    results = scanner.scan(image)
    for result in results:
        if result.type == 'UPC-A':
            print(result.data, zbar.misc.upca_is_valid(result.data.decode('ascii')), result.quality, file)