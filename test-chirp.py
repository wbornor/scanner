#!/usr/bin/python3

from time import sleep
import RPi.GPIO as GPIO


def chirp():
    GPIO.output(22, GPIO.HIGH)
    sleep(0.2)
    GPIO.output(22, GPIO.LOW)


def main():
    # set up GPIO output channel
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)

    while True:
        chirp()


if __name__ == '__main__':
    main()
