
import grovepi
import math
import socket
import datetime as dt

from grove_rgb_lcd import *

dht_sensor = 3  # The Temp & Hum Sensor goes on digital port 3.
relay = 4 # Connect the Grove Relay to digital port D4
light_sensor = 0  # Grove Light Sensor to analog port A0

onTime = 5
offTime = 21

grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(relay, "OUTPUT")

# ugly hack, but get the ip and shows on startup on screen.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

i = 0
while True:
    try:
        hh = dt.datetime.now().hour
        if hh >= onTime && hh < offTime:
            # switch on
            grovepi.digitalWrite(relay, 1)
        else:
            # switch off
            grovepi.digitalWrite(relay, 0)

        # blue=0, white=1
        [temp, humidity] = grovepi.dht(dht_sensor, 0)
        setRGB(32, 128, 32)

        firstRow = ""
        secondRow = ""

        if math.isnan(temp) is False and math.isnan(humidity) is False:
            firstRow = "%dC %d%%" % (temp, humidity)

        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)

        # Calculate resistance of sensor in K
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value

        i = (i + 1) % 10
        if i < 3:
            secondRow = ip
        else:
            secondRow = "%d %d" % (sensor_value, resistance)

        setText(firstRow + "\n" + secondRow)
        print(firstRow + "\n" + secondRow)
        time.sleep(1.00)

    except KeyboardInterrupt:
        grovepi.digitalWrite(relay, 0)
        break
    except IOError:
        print("IO Error")
