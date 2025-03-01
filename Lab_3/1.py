import ipaddress
import struct

class IP:
    def __init__ (self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # ip адресса, понятные человек
        self.scr.address = ipaddress.ip_address(self.scr)
        self.dst_address = ipaddress.ip_address(self.scr)

        #сопоставляем константы протокола с их гназваниями
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
