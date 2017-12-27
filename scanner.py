import cv2
import zbar.misc

file = './test.jpeg'

#image = mpimage.imread('/Users/wesleybornor/Desktop/UPC-A.png')
image = cv2.imread(file)
print(type(image))
if len(image.shape) == 3:
    image = zbar.misc.rgb2gray(image)
scanner = zbar.Scanner()
results = scanner.scan(image)
for result in results:
    print(result)
    if result.type == 'UPC-A':
        print(result.data, zbar.misc.upca_is_valid(result.data.decode('ascii')))