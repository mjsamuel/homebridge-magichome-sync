import logging, threading, time
from mh_device import MagicHomeDevice
from PIL import ImageGrab


class StoppableThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


def sync_screen():
    led_strip = MagicHomeDevice(ipaddr="192.168.2.129", setup="RGBWW")
    led_strip.connect()

    # Resolution of scaled down image
    rx = 64
    ry = 36
    total_pixels = rx * ry

    prev_colour = None

    while threading.current_thread().stopped() is False:
        img = ImageGrab.grab()
        img = img.resize((rx, ry))

        red = green = blue = 0
        for y in range(0, img.size[1]):
            for x in range(0, img.size[0]):
                pixel = img.getpixel((x,y))
                red = red + pixel[0]
                green = green + pixel[1]
                blue = blue + pixel[2]
        red = int(red / total_pixels)
        green = int(green / total_pixels)
        blue = int(blue / total_pixels)

        colour = (red, green, blue)
        if colour != prev_colour:
            led_strip.setRgb(colour)
            prev_colour = colour
            logging.info("RGB %3d %3d %3d Sent" % colour)
        else:
            logging.info("Same colour not sent")

        time.sleep(1)

    led_strip.turnOff()
    led_strip.disconnect()
