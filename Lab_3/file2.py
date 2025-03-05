import ipaddress
import struct

class IP:
    def __init__ (self, buff=None):
        header = struct.unpack('<BBHHHI', buff)

        self.type = header[1]
        self.code = header[2]
        self.sum = header[3]
        self.id = header[4]
        self.num = header[5]
        self.data= header[6]


