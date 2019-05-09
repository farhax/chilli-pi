import datetime as dt

from picamera import PiCamera
from time import sleep

if __name__ == "__main__":
    camera = PiCamera()
    camera.resolution = (1024, 768)

    camera.start_preview()
    sleep(5.00)

    camera.capture('images/%s.jpg' % dt.datetime.now())
    camera.stop_preview()
