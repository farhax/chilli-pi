# To run this on startup
# add run script to /etc/rc.local right before exit 0
# sudo python3 /home/pi/Development/chilli-pi/ip_lcd.py &

import socket


# Automatically called whenever the shadow is updated.
def getIp():
    # ugly hack, but get the ip and shows on startup on screen.
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()

    return ip


if __name__ == "__main__":
    ip = getIp()
    print(ip)
