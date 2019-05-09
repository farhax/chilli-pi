
import grovepi
import math
import datetime as dt
import logging

from logging.handlers import TimedRotatingFileHandler
from grove_rgb_lcd import *


def log(temp, humidity, moist_value, light_value, switchOn):
    logger.info("temp: %0.2fC, humidity: %0.2f%%, moisture: %d, light-sensor: %d, light-switch: %d" % (temp, humidity, moist_value, light_value, switchOn))


if __name__ == "__main__":

    logger = logging.getLogger('myapp')
    logname = "logs/chilli.log"
    handler = TimedRotatingFileHandler(logname, when="midnight", interval=1)
    handler.suffix = "%Y%m%d"
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    dht_sensor = 3  # The Temp & Hum Sensor goes on digital port 3.
    relay = 4  # Connect the Grove Relay to digital port D4
    light_sensor = 0  # Grove Light Sensor to analog port A0
    moist_sensor = 1  # Funduino - Moisture sensor, A1

    onTime = 5
    offTime = 21

    grovepi.pinMode(light_sensor, "INPUT")
    grovepi.pinMode(relay, "OUTPUT")

    for x in range(5):
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

            setText(firstRow + "\n" + secondRow)

            if x == 0:
                log(temp, humidity, moist_value, light_value, switchOn)

            if x != 4:
                time.sleep(10.00)

        except KeyboardInterrupt:
            grovepi.digitalWrite(relay, 0)
            break
        except IOError:
            logger.error('IO Error')
