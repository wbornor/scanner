#!/usr/bin/python3

import time
import RPi.GPIO as GPIO

__pin__ = 22


def buzz(pitch, duration):  # create the function “buzz” and feed it the pitch and duration)

    if (pitch == 0):
        time.sleep(duration)
        return
    period = 1.0 / pitch  # in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
    delay = period / 2  # calcuate the time for half of the wave
    cycles = int(duration * pitch)  # the number of waves to produce is the duration times the frequency

    for i in range(cycles):  # start a loop from 0 to the variable “cycles” calculated above
        GPIO.output(__pin__, GPIO.HIGH)  # set pin 18 to high
        time.sleep(delay)  # wait with pin 18 high
        GPIO.output(__pin__, GPIO.LOW)  # set pin 18 to low
        time.sleep(delay)  # wait with pin 18 low


def main():
    # set up GPIO output channel
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(__pin__, GPIO.IN)
    GPIO.setup(__pin__, GPIO.OUT)

    while True:
        buzz(500, 0.1)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
