import socket


class MagicHomeDevice():
    def __init__(self, ipaddr, port=5577, setup="RGBW"):
        self.ipaddr = ipaddr
        self.port = port
        self.setup = setup

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        self.socket.connect((self.ipaddr, self.port))
        self.socket.settimeout(None)


    def __del__(self):
        self.socket.close()


    def turnOn(self, on=True):
        if on:
            msg = bytearray([0x71, 0x23, 0x0f])
        else:
            msg = bytearray([0x71, 0x24, 0x0f])

        self.__write(msg)


    def turnOff(self):
        self.turnOn(False)


    def setRgb(self, colour, persist=True):
        if persist:
            msg = bytearray([0x31])
        else:
            msg = bytearray([0x41])
        if (self.setup == "GRB" or self.setup == "GRBW" or self.setup == "GRBWW"):
            msg.append(colour[1])
            msg.append(colour[0])
            msg.append(colour[2])
        if (self.setup == "RGB" or self.setup == "RGBW" or self.setup == "RGBWW"):
            msg.append(colour[0])
            msg.append(colour[1])
            msg.append(colour[2])
        if (self.setup == "RGBWW" or self.setup == "GRBWW"):
            msg.append(0x00)
        msg.append(0x00)
        msg.append(0xf0)
        msg.append(0x0f)
        self.__write(msg)


    def __writeRaw(self, bytes):
        self.socket.send(bytes)


    def __write(self, bytes):
        # Calculate the checksum of the byte array and add to the end
        csum = sum(bytes) & 0xFF
        bytes.append(csum)
        self.__writeRaw(bytes)
