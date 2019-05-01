# To run this on startup
# add run script to /etc/rc.local right before exit 0
# sudo python3 /home/pi/Development/chilli-pi/ip_lcd.py &

import grovepi
import socket

from grove_rgb_lcd import *


# ugly hack, but get the ip and shows on startup on screen.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = s.getsockname()[0]
s.close()

print(ip)

try:
    setRGB(128, 255, 128)

    ips = ip.split('.')
    setText(ips[0] + '.' + ips[1] + "\n" + ips[2] + '.' + ips[3])
    time.sleep(5.00)

except IOError:
    print("IO Error")
