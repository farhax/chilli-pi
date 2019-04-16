
import grovepi
import math

from grove_rgb_lcd import *

dht_sensor = 3  # The Temp & Hum Sensor goes on digital port 3.
light_sensor = 0  # Grove Light Sensor to analog port A0

grovepi.pinMode(light_sensor, "INPUT")

while True:
    try:
        # blue=0, white=1
        [temp, humidity] = grovepi.dht(dht_sensor, 0)
        setRGB(32, 128, 32)
        if math.isnan(temp) is False and math.isnan(humidity) is False:
            setText("Temp:  %.02f C\nHumid: %.02f%%" % (temp, humidity))
        else:
            setText("Error: no temp \nno humidity")

        time.sleep(2.00)
        setRGB(64, 128, 64)

        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)

        # Calculate resistance of sensor in K
        resistance = (float)(1023 - sensor_value) * 10 / sensor_value
        setText("Light: %d \nResist: %.2fK" % (sensor_value, resistance))
        time.sleep(2.00)

    except IOError:
        print ("Error")
