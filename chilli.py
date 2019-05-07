
import grovepi
import math
import socket
import datetime as dt
import logging

from logging.handlers import TimedRotatingFileHandler
from picamera import PiCamera
from grove_rgb_lcd import *

logger = logging.getLogger('myapp')
# hdlr = logging.FileHandler('/var/tmp/myapp.log')
logname = "logs/chilli.log"
handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
handler.suffix = "%Y%m%d"
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def log(temp, humidity, moist_value, light_value, switchOn):
    logger.info("temp: %0.2fC, humidity: %0.2f%%, moisture: %d, light-sensor: %d, light-switch: %d" % (temp, humidity, moist_value, light_value, switchOn))


def captureImage():
    camera.resolution = (1024, 768)
    camera.capture('images/%s.jpg' % dt.datetime.now())


dht_sensor = 3  # The Temp & Hum Sensor goes on digital port 3.
relay = 4  # Connect the Grove Relay to digital port D4
light_sensor = 0  # Grove Light Sensor to analog port A0
moist_sensor = 1 # Funduino - Moisture sensor, A1

onTime = 5
offTime = 21

grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(relay, "OUTPUT")

# ugly hack, but get the ip and shows on startup on screen.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

print("starting chilli-pi, waiting for camera")
camera = PiCamera()
camera.start_preview()
time.sleep(5.00)


i = 0
while True:
    try:
        hh = dt.datetime.now().hour
        if hh >= onTime and hh < offTime:
            # switch on
            grovepi.digitalWrite(relay, 1)
            switchOn = True
        else:
            # switch off
            grovepi.digitalWrite(relay, 0)
            switchOn = False

        # blue=0, white=1
        [temp, humidity] = grovepi.dht(dht_sensor, 0)
        setRGB(32, 128, 32)

        firstRow = ""
        secondRow = ""

        if math.isnan(temp) is False and math.isnan(humidity) is False:
            firstRow = "%dC %d%%" % (temp, humidity)

        # Get sensor values
        light_value = grovepi.analogRead(light_sensor)
        moist_value = grovepi.analogRead(moist_sensor)

        secondRow = "%d %d" % (light_value, moist_value)

        if i % 10 == 0:  # log every 10s
            log(temp, humidity, moist_value, light_value, switchOn)

        if i == 0 or i == 1800:  # capture image every hour
            captureImage()

        i = (i + 1) % 3600

        setText(firstRow + "\n" + secondRow)
        print(firstRow + "\n" + secondRow)
        time.sleep(1.00)

    except KeyboardInterrupt:
        grovepi.digitalWrite(relay, 0)
        camera.stop_preview()
        break
    except IOError:
        logger.error('IO Error')
        print("IO Error")
