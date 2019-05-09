import datetime as dt
import os

from picamera import PiCamera
from time import sleep

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(__file__)) + '/'
    camera = PiCamera()
    camera.resolution = (1024, 768)

    camera.start_preview()
    sleep(5.00)

    camera.capture(path + 'images/%s.jpg' % dt.datetime.now())
    camera.stop_preview()
