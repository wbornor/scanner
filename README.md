# scanner for Raspberry Pi

Use [Picamera](https://picamera.readthedocs.io/en/release-1.13/index.html) to capture an image and scan it for any legible barcodse or QR codes using [zbar](https://pypi.python.org/pypi/zbar-py/1.0.4).

Successfully scanning a barcode publishes the encoded information to AWS SNS. It will also illuminate the activity LED (gpio16) on the board.
